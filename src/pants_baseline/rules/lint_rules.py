"""Rules for Ruff linting."""

from dataclasses import dataclass
from typing import Any, Iterable

from pants.core.goals.lint import LintResult, LintTargetsRequest
from pants.core.util_rules.external_tool import DownloadedExternalTool, download_external_tool
from pants.core.util_rules.partitions import PartitionerType
from pants.core.util_rules.source_files import SourceFiles, SourceFilesRequest, determine_source_files
from pants.engine.fs import Digest, MergeDigests
from pants.engine.intrinsics import execute_process, merge_digests
from pants.engine.platform import Platform
from pants.engine.process import Process
from pants.engine.rules import collect_rules, implicitly, rule
from pants.engine.target import FieldSet
from pants.util.logging import LogLevel
from pants.util.meta import classproperty

from pants.backend.python.target_types import PythonSourceField

from pants_baseline.subsystems.baseline import BaselineSubsystem
from pants_baseline.subsystems.ruff import RuffSubsystem


@dataclass(frozen=True)
class RuffLintFieldSet(FieldSet):
    """Field set for Ruff linting."""

    required_fields = (PythonSourceField,)

    sources: PythonSourceField


class RuffLintRequest(LintTargetsRequest):
    """Request to run Ruff linting."""

    field_set_type = RuffLintFieldSet
    tool_subsystem = RuffSubsystem
    partitioner_type = PartitionerType.DEFAULT_SINGLE_PARTITION

    @classproperty
    def tool_name(cls) -> str:
        return "baseline-ruff"

    @classproperty
    def tool_id(cls) -> str:
        return "baseline-ruff"


@rule(desc="Lint with Ruff", level=LogLevel.DEBUG)
async def run_ruff_lint(
    request: RuffLintRequest.Batch[RuffLintFieldSet, Any],
    ruff_subsystem: RuffSubsystem,
    baseline_subsystem: BaselineSubsystem,
    platform: Platform,
) -> LintResult:
    """Run Ruff linter on Python files."""
    if ruff_subsystem.skip:
        return LintResult.create(request, exit_code=0, stdout="", stderr="", strip_chroot_path=True)

    if not baseline_subsystem.enabled:
        return LintResult.create(request, exit_code=0, stdout="", stderr="", strip_chroot_path=True)

    field_sets = list(request.elements)

    if not field_sets:
        return LintResult.create(request, exit_code=0, stdout="No targets to lint", stderr="", strip_chroot_path=True)

    # Download ruff and get source files
    downloaded_ruff: DownloadedExternalTool = await download_external_tool(
        ruff_subsystem.get_request(platform)
    )
    sources: SourceFiles = await determine_source_files(
        SourceFilesRequest(
            sources_fields=[fs.sources for fs in field_sets],
            for_sources_types=(PythonSourceField,),
        )
    )

    if not sources.files:
        return LintResult.create(request, exit_code=0, stdout="No files to lint", stderr="", strip_chroot_path=True)

    # Merge the ruff binary with the source files
    input_digest: Digest = await merge_digests(
        MergeDigests([downloaded_ruff.digest, sources.snapshot.digest]),
    )

    # Build Ruff command
    select_args = [f"--select={','.join(ruff_subsystem.select)}"] if ruff_subsystem.select else []
    ignore_args = [f"--ignore={','.join(ruff_subsystem.ignore)}"] if ruff_subsystem.ignore else []

    # Build Ruff check command
    # Note: line-length is a config file option only in ruff 0.9+
    argv = [
        downloaded_ruff.exe,
        "check",
        f"--target-version=py{baseline_subsystem.python_version.replace('.', '')}",
        *select_args,
        *ignore_args,
        "--output-format=concise",
        *sources.files,
    ]

    # execute_process returns FallibleProcessResult which LintResult.create accepts directly
    process_result = await execute_process(
        Process(
            argv=argv,
            input_digest=input_digest,
            description=f"Run Ruff lint on {len(sources.files)} files",
            level=LogLevel.DEBUG,
        ),
        **implicitly(),
    )

    # LintResult.create() takes 2 args in Pants 2.30+
    return LintResult.create(request, process_result)


def rules() -> Iterable:
    """Return all lint rules."""
    return [
        *collect_rules(),
        *RuffLintRequest.rules(),
    ]
