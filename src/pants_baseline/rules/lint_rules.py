"""Rules for Ruff linting."""

from dataclasses import dataclass
from typing import Iterable

from pants.core.goals.lint import LintResult, LintTargetsRequest
from pants.core.util_rules.external_tool import download_external_tool
from pants.core.util_rules.partitions import PartitionerType
from pants.core.util_rules.source_files import SourceFiles, SourceFilesRequest
from pants.engine.fs import MergeDigests
from pants.engine.internals.selectors import concurrently
from pants.engine.intrinsics import merge_digests, execute_process
from pants.engine.platform import Platform
from pants.engine.process import Process
from pants.engine.rules import collect_rules, implicitly, rule
from pants.engine.target import FieldSet, Target
from pants.util.logging import LogLevel

from pants_baseline.subsystems.baseline import BaselineSubsystem
from pants_baseline.subsystems.ruff import RuffSubsystem
from pants_baseline.targets import BaselineSourcesField, SkipLintField


@dataclass(frozen=True)
class RuffLintFieldSet(FieldSet):
    """Field set for Ruff linting."""

    required_fields = (BaselineSourcesField,)

    sources: BaselineSourcesField
    skip_lint: SkipLintField

    @classmethod
    def opt_out(cls, tgt: Target) -> bool:
        """Allow targets to opt out of linting."""
        return tgt.get(SkipLintField).value


class RuffLintRequest(LintTargetsRequest):
    """Request to run Ruff linting."""

    field_set_type = RuffLintFieldSet
    tool_subsystem = RuffSubsystem
    partitioner_type = PartitionerType.DEFAULT_SINGLE_PARTITION


@rule(desc="Lint with Ruff", level=LogLevel.DEBUG)
async def run_ruff_lint(
    request: RuffLintRequest.Batch,
    ruff_subsystem: RuffSubsystem,
    baseline_subsystem: BaselineSubsystem,
    platform: Platform,
) -> LintResult:
    """Run Ruff linter on Python files."""
    if not baseline_subsystem.enabled:
        return LintResult(
            exit_code=0,
            stdout="",
            stderr="",
            linter_name="ruff",
            partition_description=None,
        )

    field_sets = request.elements

    if not field_sets:
        return LintResult(
            exit_code=0,
            stdout="No targets to lint",
            stderr="",
            linter_name="ruff",
            partition_description=None,
        )

    # Download ruff and get source files in parallel using new intrinsics
    downloaded_ruff_get = download_external_tool(ruff_subsystem.get_request(platform))
    sources_get = SourceFilesRequest(
        sources_fields=[fs.sources for fs in field_sets],
        for_sources_types=(BaselineSourcesField,),
    )

    downloaded_ruff, sources = await concurrently(
        downloaded_ruff_get,
        implicitly(sources_get, SourceFiles),
    )

    if not sources.files:
        return LintResult(
            exit_code=0,
            stdout="No files to lint",
            stderr="",
            linter_name="ruff",
            partition_description=None,
        )

    # Merge the ruff binary with the source files
    input_digest = await merge_digests(
        MergeDigests([downloaded_ruff.digest, sources.snapshot.digest]),
    )

    # Build Ruff command
    select_args = [f"--select={','.join(ruff_subsystem.select)}"] if ruff_subsystem.select else []
    ignore_args = [f"--ignore={','.join(ruff_subsystem.ignore)}"] if ruff_subsystem.ignore else []

    argv = [
        downloaded_ruff.exe,
        "check",
        f"--target-version=py{baseline_subsystem.python_version.replace('.', '')}",
        f"--line-length={baseline_subsystem.line_length}",
        *select_args,
        *ignore_args,
        "--output-format=text",
        *sources.files,
    ]

    process = Process(
        argv=argv,
        input_digest=input_digest,
        description=f"Run Ruff lint on {len(sources.files)} files",
        level=LogLevel.DEBUG,
    )

    result = await execute_process(process)

    return LintResult(
        exit_code=result.exit_code,
        stdout=result.stdout.decode(),
        stderr=result.stderr.decode(),
        linter_name="ruff",
        partition_description=request.partition_metadata,
    )


def rules() -> Iterable:
    """Return all lint rules."""
    return [
        *collect_rules(),
        *RuffLintRequest.rules(),
    ]
