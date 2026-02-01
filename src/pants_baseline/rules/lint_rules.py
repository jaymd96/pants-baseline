"""Rules for Ruff linting."""

from dataclasses import dataclass
from typing import Iterable

from pants.core.goals.lint import LintResult, LintTargetsRequest
from pants.core.util_rules.external_tool import DownloadedExternalTool, ExternalToolRequest
from pants.core.util_rules.source_files import SourceFiles, SourceFilesRequest
from pants.engine.fs import Digest, MergeDigests
from pants.engine.platform import Platform
from pants.engine.process import FallibleProcessResult, Process
from pants.engine.rules import Get, MultiGet, collect_rules, rule
from pants.engine.target import FieldSet, Target
from pants.engine.unions import UnionRule
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


class RuffLintRequest(LintTargetsRequest):
    """Request to run Ruff linting."""

    field_set_type = RuffLintFieldSet
    tool_name = "ruff"


@dataclass(frozen=True)
class RuffLintResult:
    """Result of running Ruff lint."""

    exit_code: int
    stdout: str
    stderr: str


@rule(desc="Lint with Ruff", level=LogLevel.DEBUG)
async def run_ruff_lint(
    request: RuffLintRequest,
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

    # Filter out skipped targets
    field_sets = [fs for fs in request.field_sets if not fs.skip_lint.value]

    if not field_sets:
        return LintResult(
            exit_code=0,
            stdout="No targets to lint",
            stderr="",
            linter_name="ruff",
            partition_description=None,
        )

    # Get source files
    source_files_request: SourceFilesRequest = SourceFilesRequest(
        sources_fields=[fs.sources for fs in field_sets],
        for_sources_types=(BaselineSourcesField,),
    )
    sources = await Get(SourceFiles, SourceFilesRequest, source_files_request)

    if not sources.files:
        return LintResult(
            exit_code=0,
            stdout="No files to lint",
            stderr="",
            linter_name="ruff",
            partition_description=None,
        )

    # Build Ruff command
    select_args = [f"--select={','.join(ruff_subsystem.select)}"] if ruff_subsystem.select else []
    ignore_args = [f"--ignore={','.join(ruff_subsystem.ignore)}"] if ruff_subsystem.ignore else []

    argv = [
        "ruff",
        "check",
        f"--target-version={baseline_subsystem.get_python_target_version()}",
        f"--line-length={baseline_subsystem.line_length}",
        *select_args,
        *ignore_args,
        "--output-format=text",
        *sources.files,
    ]

    process: Process = Process(
        argv=argv,
        input_digest=sources.snapshot.digest,
        description=f"Run Ruff lint on {len(sources.files)} files",
        level=LogLevel.DEBUG,
    )

    result = await Get(FallibleProcessResult, Process, process)

    return LintResult(
        exit_code=result.exit_code,
        stdout=result.stdout.decode(),
        stderr=result.stderr.decode(),
        linter_name="ruff",
        partition_description=None,
    )


def rules() -> Iterable:
    """Return all lint rules."""
    return [
        *collect_rules(),
        UnionRule(LintTargetsRequest, RuffLintRequest),
    ]
