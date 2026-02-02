"""Rules for ty type checking."""

from dataclasses import dataclass
from typing import Iterable

from pants.core.goals.check import CheckRequest, CheckResult, CheckResults
from pants.core.util_rules.external_tool import DownloadedExternalTool, ExternalToolRequest
from pants.core.util_rules.source_files import SourceFiles, SourceFilesRequest
from pants.engine.fs import Digest, MergeDigests
from pants.engine.platform import Platform
from pants.engine.process import FallibleProcessResult, Process
from pants.engine.rules import Get, MultiGet, collect_rules, rule
from pants.engine.target import FieldSet
from pants.engine.unions import UnionRule
from pants.util.logging import LogLevel

from pants_baseline.subsystems.baseline import BaselineSubsystem
from pants_baseline.subsystems.ty import TySubsystem
from pants_baseline.targets import BaselineSourcesField, SkipTypecheckField


@dataclass(frozen=True)
class TyFieldSet(FieldSet):
    """Field set for ty type checking."""

    required_fields = (BaselineSourcesField,)

    sources: BaselineSourcesField
    skip_typecheck: SkipTypecheckField


class TyCheckRequest(CheckRequest):
    """Request to run ty type checking."""

    field_set_type = TyFieldSet
    tool_name = "ty"


@rule(desc="Type check with ty", level=LogLevel.DEBUG)
async def run_ty_check(
    request: TyCheckRequest,
    ty_subsystem: TySubsystem,
    baseline_subsystem: BaselineSubsystem,
    platform: Platform,
) -> CheckResults:
    """Run ty type checker on Python files."""
    if not baseline_subsystem.enabled:
        return CheckResults(
            results=[
                CheckResult(
                    exit_code=0,
                    stdout="",
                    stderr="",
                    partition_description=None,
                )
            ],
            checker_name="ty",
        )

    # Filter out skipped targets
    field_sets = [fs for fs in request.field_sets if not fs.skip_typecheck.value]

    if not field_sets:
        return CheckResults(
            results=[
                CheckResult(
                    exit_code=0,
                    stdout="No targets to type check",
                    stderr="",
                    partition_description=None,
                )
            ],
            checker_name="ty",
        )

    # Download ty and get source files in parallel
    downloaded_ty, sources = await MultiGet(
        Get(DownloadedExternalTool, ExternalToolRequest, ty_subsystem.get_request(platform)),
        Get(
            SourceFiles,
            SourceFilesRequest(
                sources_fields=[fs.sources for fs in field_sets],
                for_sources_types=(BaselineSourcesField,),
            ),
        ),
    )

    if not sources.files:
        return CheckResults(
            results=[
                CheckResult(
                    exit_code=0,
                    stdout="No files to type check",
                    stderr="",
                    partition_description=None,
                )
            ],
            checker_name="ty",
        )

    # Merge the ty binary with the source files
    input_digest = await Get(
        Digest,
        MergeDigests([downloaded_ty.digest, sources.snapshot.digest]),
    )

    # Build ty command
    strict_arg = ["--strict"] if ty_subsystem.strict else []
    output_format_arg = [f"--output-format={ty_subsystem.output_format}"]

    argv = [
        downloaded_ty.exe,
        "check",
        f"--python-version={baseline_subsystem.python_version}",
        *strict_arg,
        *output_format_arg,
        *sources.files,
    ]

    process = Process(
        argv=argv,
        input_digest=input_digest,
        description=f"Run ty type check on {len(sources.files)} files",
        level=LogLevel.DEBUG,
    )

    result = await Get(FallibleProcessResult, Process, process)

    return CheckResults(
        results=[
            CheckResult(
                exit_code=result.exit_code,
                stdout=result.stdout.decode(),
                stderr=result.stderr.decode(),
                partition_description=None,
            )
        ],
        checker_name="ty",
    )


def rules() -> Iterable:
    """Return all type check rules."""
    return [
        *collect_rules(),
        UnionRule(CheckRequest, TyCheckRequest),
    ]
