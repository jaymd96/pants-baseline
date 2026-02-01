"""Rules for pytest testing with coverage."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from pants.core.goals.test import TestRequest, TestResult
from pants.core.util_rules.source_files import SourceFiles, SourceFilesRequest
from pants.engine.process import FallibleProcessResult, Process
from pants.engine.rules import Get, collect_rules, rule
from pants.engine.target import FieldSet
from pants.engine.unions import UnionRule
from pants.util.logging import LogLevel

from pants_baseline.subsystems.baseline import BaselineSubsystem
from pants_baseline.targets import (
    BaselineSourcesField,
    BaselineTestSourcesField,
    CoverageThresholdField,
    SkipTestField,
)


@dataclass(frozen=True)
class PytestFieldSet(FieldSet):
    """Field set for pytest testing."""

    required_fields = (BaselineTestSourcesField,)

    sources: BaselineSourcesField
    test_sources: BaselineTestSourcesField
    coverage_threshold: CoverageThresholdField
    skip_test: SkipTestField


class PytestTestRequest(TestRequest):
    """Request to run pytest tests."""

    field_set_type = PytestFieldSet
    tool_name = "pytest"


@rule(desc="Test with pytest", level=LogLevel.DEBUG)
async def run_pytest(
    request: PytestTestRequest,
    baseline_subsystem: BaselineSubsystem,
) -> TestResult:
    """Run pytest on test files with coverage."""
    if not baseline_subsystem.enabled:
        return TestResult(
            exit_code=0,
            stdout="",
            stderr="",
            stdout_digest=None,
            stderr_digest=None,
            address=None,
            output_setting=None,
        )

    # Filter out skipped targets
    field_sets = [fs for fs in request.field_sets if not fs.skip_test.value]

    if not field_sets:
        return TestResult(
            exit_code=0,
            stdout="No targets to test",
            stderr="",
            stdout_digest=None,
            stderr_digest=None,
            address=None,
            output_setting=None,
        )

    # Get test source files
    test_sources = await Get(
        SourceFiles,
        SourceFilesRequest(
            sources_fields=[fs.test_sources for fs in field_sets],
            for_sources_types=(BaselineTestSourcesField,),
        ),
    )

    # Get source files for coverage
    sources = await Get(
        SourceFiles,
        SourceFilesRequest(
            sources_fields=[fs.sources for fs in field_sets],
            for_sources_types=(BaselineSourcesField,),
        ),
    )

    if not test_sources.files:
        return TestResult(
            exit_code=0,
            stdout="No test files found",
            stderr="",
            stdout_digest=None,
            stderr_digest=None,
            address=None,
            output_setting=None,
        )

    # Get coverage threshold from first field set (or use default)
    coverage_threshold = (
        field_sets[0].coverage_threshold.value
        if field_sets
        else baseline_subsystem.coverage_threshold
    )

    # Build pytest command with coverage
    src_root = ",".join(baseline_subsystem.src_roots)

    argv = [
        "pytest",
        "-v",
        "--strict-markers",
        "--strict-config",
        "-ra",
        "--tb=short",
        f"--cov={src_root}",
        "--cov-report=term-missing",
        f"--cov-fail-under={coverage_threshold}",
        "--cov-branch",
        *test_sources.files,
    ]

    process = Process(
        argv=argv,
        input_digest=test_sources.snapshot.digest,
        description=f"Run pytest on {len(test_sources.files)} test files",
        level=LogLevel.DEBUG,
    )

    result = await Get(FallibleProcessResult, Process, process)

    return TestResult(
        exit_code=result.exit_code,
        stdout=result.stdout.decode(),
        stderr=result.stderr.decode(),
        stdout_digest=None,
        stderr_digest=None,
        address=None,
        output_setting=None,
    )


def rules() -> Iterable:
    """Return all test rules."""
    return [
        *collect_rules(),
        UnionRule(TestRequest, PytestTestRequest),
    ]
