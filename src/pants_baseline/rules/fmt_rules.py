"""Rules for Ruff formatting."""

from dataclasses import dataclass
from typing import Any, Iterable

from pants.core.goals.fmt import FmtResult, FmtTargetsRequest
from pants.core.util_rules.external_tool import DownloadedExternalTool, download_external_tool
from pants.core.util_rules.partitions import PartitionerType
from pants.engine.fs import Digest, MergeDigests
from pants.engine.intrinsics import merge_digests
from pants.engine.platform import Platform
from pants.engine.process import FallibleProcessResult, Process, execute_process_or_raise
from pants.engine.rules import collect_rules, implicitly, rule
from pants.engine.target import FieldSet
from pants.util.logging import LogLevel
from pants.util.meta import classproperty

from pants.backend.python.target_types import PythonSourceField

from pants_baseline.subsystems.baseline import BaselineSubsystem
from pants_baseline.subsystems.ruff import RuffSubsystem


@dataclass(frozen=True)
class RuffFmtFieldSet(FieldSet):
    """Field set for Ruff formatting."""

    required_fields = (PythonSourceField,)

    sources: PythonSourceField


class RuffFmtRequest(FmtTargetsRequest):
    """Request to run Ruff formatting."""

    field_set_type = RuffFmtFieldSet
    tool_subsystem = RuffSubsystem
    partitioner_type = PartitionerType.DEFAULT_SINGLE_PARTITION

    @classproperty
    def tool_name(cls) -> str:
        return "baseline-ruff-fmt"

    @classproperty
    def tool_id(cls) -> str:
        return "baseline-ruff-fmt"


@rule(desc="Format with Ruff", level=LogLevel.DEBUG)
async def run_ruff_fmt(
    request: RuffFmtRequest.Batch[RuffFmtFieldSet, Any],
    ruff_subsystem: RuffSubsystem,
    baseline_subsystem: BaselineSubsystem,
    platform: Platform,
) -> FmtResult:
    """Run Ruff formatter on Python files."""
    if ruff_subsystem.skip:
        return FmtResult.skip(request, formatter_name="baseline-ruff-fmt")

    if not baseline_subsystem.enabled:
        return FmtResult.skip(request, formatter_name="baseline-ruff-fmt")

    snapshot = request.snapshot
    if not snapshot.files:
        return FmtResult.skip(request, formatter_name="baseline-ruff-fmt")

    # Download ruff
    downloaded_ruff: DownloadedExternalTool = await download_external_tool(
        ruff_subsystem.get_request(platform)
    )

    # Merge the ruff binary with the source files
    input_digest: Digest = await merge_digests(
        MergeDigests([downloaded_ruff.digest, snapshot.digest]),
    )

    # Build Ruff format command
    # Note: quote-style and indent-style are config file options only in ruff 0.9+
    argv = [
        downloaded_ruff.exe,
        "format",
        f"--target-version=py{baseline_subsystem.python_version.replace('.', '')}",
        f"--line-length={baseline_subsystem.line_length}",
        *snapshot.files,
    ]

    result: FallibleProcessResult = await execute_process_or_raise(
        **implicitly(
            Process(
                argv=argv,
                input_digest=input_digest,
                output_files=snapshot.files,
                description=f"Run Ruff format on {len(snapshot.files)} files",
                level=LogLevel.DEBUG,
            )
        )
    )

    # FmtResult.create() is async and takes 2 args in Pants 2.30+
    return await FmtResult.create(request, result)


def rules() -> Iterable:
    """Return all format rules."""
    return [
        *collect_rules(),
        *RuffFmtRequest.rules(),
    ]
