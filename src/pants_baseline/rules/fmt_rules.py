"""Rules for Ruff formatting."""

from dataclasses import dataclass
from typing import Iterable

from pants.core.goals.fmt import FmtResult, FmtTargetsRequest
from pants.core.util_rules.external_tool import DownloadedExternalTool, ExternalToolRequest
from pants.core.util_rules.source_files import SourceFiles, SourceFilesRequest
from pants.engine.fs import Digest, MergeDigests, Snapshot
from pants.engine.platform import Platform
from pants.engine.process import FallibleProcessResult, Process
from pants.engine.rules import Get, MultiGet, collect_rules, rule
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
    platform: Platform,
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

    # Download ruff and get source files in parallel
    downloaded_ruff, sources = await MultiGet(
        Get(DownloadedExternalTool, ExternalToolRequest, ruff_subsystem.get_request(platform)),
        Get(
            SourceFiles,
            SourceFilesRequest(
                sources_fields=[fs.sources for fs in field_sets],
                for_sources_types=(BaselineSourcesField,),
            ),
        ),
    )

    if not sources.files:
        return FmtResult(
            input=request.snapshot,
            output=request.snapshot,
            stdout="No files to format",
            stderr="",
            formatter_name="ruff",
        )

    # Merge the ruff binary with the source files
    input_digest = await Get(
        Digest,
        MergeDigests([downloaded_ruff.digest, sources.snapshot.digest]),
    )

    # Build Ruff format command
    argv = [
        downloaded_ruff.exe,
        "format",
        f"--target-version=py{baseline_subsystem.python_version.replace('.', '')}",
        f"--line-length={baseline_subsystem.line_length}",
        f"--quote-style={ruff_subsystem.quote_style}",
        f"--indent-style={ruff_subsystem.indent_style}",
        *sources.files,
    ]

    process = Process(
        argv=argv,
        input_digest=input_digest,
        output_files=sources.files,
        description=f"Run Ruff format on {len(sources.files)} files",
        level=LogLevel.DEBUG,
    )

    result = await Get(FallibleProcessResult, Process, process)

    output_digest: Digest = result.output_digest
    output_snapshot = await Get(Snapshot, Digest, output_digest)

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
