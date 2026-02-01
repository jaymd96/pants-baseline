"""Rules for Ruff formatting."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from pants.core.goals.fmt import FmtResult, FmtTargetsRequest
from pants.core.util_rules.source_files import SourceFiles, SourceFilesRequest
from pants.engine.fs import Digest, Snapshot
from pants.engine.process import FallibleProcessResult, Process
from pants.engine.rules import Get, collect_rules, rule
from pants.engine.target import FieldSet
from pants.engine.unions import UnionRule
from pants.util.logging import LogLevel

from pants_baseline.subsystems.baseline import BaselineSubsystem
from pants_baseline.subsystems.ruff import RuffSubsystem
from pants_baseline.targets import BaselineSourcesField, SkipFormatField


@dataclass(frozen=True)
class RuffFmtFieldSet(FieldSet):
    """Field set for Ruff formatting."""

    required_fields = (BaselineSourcesField,)

    sources: BaselineSourcesField
    skip_fmt: SkipFormatField


class RuffFmtRequest(FmtTargetsRequest):
    """Request to run Ruff formatting."""

    field_set_type = RuffFmtFieldSet
    tool_name = "ruff"


@rule(desc="Format with Ruff", level=LogLevel.DEBUG)
async def run_ruff_fmt(
    request: RuffFmtRequest,
    ruff_subsystem: RuffSubsystem,
    baseline_subsystem: BaselineSubsystem,
) -> FmtResult:
    """Run Ruff formatter on Python files."""
    if not baseline_subsystem.enabled:
        return FmtResult(
            input=request.snapshot,
            output=request.snapshot,
            stdout="",
            stderr="",
            formatter_name="ruff",
        )

    # Filter out skipped targets
    field_sets = [fs for fs in request.field_sets if not fs.skip_fmt.value]

    if not field_sets:
        return FmtResult(
            input=request.snapshot,
            output=request.snapshot,
            stdout="No targets to format",
            stderr="",
            formatter_name="ruff",
        )

    # Get source files
    source_files_request = SourceFilesRequest(
        sources_fields=[fs.sources for fs in field_sets],
        for_sources_types=(BaselineSourcesField,),
    )
    sources = await Get(SourceFiles, {SourceFilesRequest: source_files_request})

    if not sources.files:
        return FmtResult(
            input=request.snapshot,
            output=request.snapshot,
            stdout="No files to format",
            stderr="",
            formatter_name="ruff",
        )

    # Build Ruff format command
    argv = [
        "ruff",
        "format",
        f"--target-version={baseline_subsystem.get_python_target_version()}",
        f"--line-length={baseline_subsystem.line_length}",
        f"--quote-style={ruff_subsystem.quote_style}",
        f"--indent-style={ruff_subsystem.indent_style}",
        *sources.files,
    ]

    process = Process(
        argv=argv,
        input_digest=sources.snapshot.digest,
        output_files=sources.files,
        description=f"Run Ruff format on {len(sources.files)} files",
        level=LogLevel.DEBUG,
    )

    result = await Get(FallibleProcessResult, {Process: process})

    output_snapshot = await Get(Snapshot, {Digest: result.output_digest})

    return FmtResult(
        input=sources.snapshot,
        output=output_snapshot,
        stdout=result.stdout.decode(),
        stderr=result.stderr.decode(),
        formatter_name="ruff",
    )


def rules() -> Iterable:
    """Return all format rules."""
    return [
        *collect_rules(),
        UnionRule(FmtTargetsRequest, RuffFmtRequest),
    ]
