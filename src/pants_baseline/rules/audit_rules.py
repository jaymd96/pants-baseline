"""Rules for uv security auditing."""

from dataclasses import dataclass
from typing import Iterable

from pants.core.util_rules.external_tool import download_external_tool
from pants.engine.fs import MergeDigests, PathGlobs
from pants.engine.internals.selectors import concurrently
from pants.engine.intrinsics import merge_digests, execute_process, path_globs_to_digest
from pants.engine.platform import Platform
from pants.engine.process import Process
from pants.engine.rules import collect_rules, implicitly, rule
from pants.util.logging import LogLevel

from pants_baseline.subsystems.uv import UvSubsystem


@dataclass(frozen=True)
class AuditResult:
    """Result of running uv audit."""

    exit_code: int
    stdout: str
    stderr: str
    vulnerabilities_found: int


@dataclass(frozen=True)
class UvAuditRequest:
    """Request to run uv audit."""

    lock_file: str
    ignore_vulns: tuple[str, ...]
    output_format: str


@rule(desc="Audit dependencies with uv", level=LogLevel.DEBUG)
async def run_uv_audit(
    request: UvAuditRequest,
    uv_subsystem: UvSubsystem,
    platform: Platform,
) -> AuditResult:
    """Run uv audit on dependencies."""
    # Download uv and get lock files in parallel using new intrinsics
    downloaded_uv_get = download_external_tool(uv_subsystem.get_request(platform))
    lock_file_digest_get = path_globs_to_digest(
        PathGlobs([request.lock_file, "pyproject.toml", "requirements.txt"])
    )

    downloaded_uv, lock_file_digest = await concurrently(
        downloaded_uv_get,
        lock_file_digest_get,
    )

    # Merge the uv binary with lock files
    input_digest = await merge_digests(
        MergeDigests([downloaded_uv.digest, lock_file_digest]),
    )

    # Build ignore args
    ignore_args = []
    for vuln in request.ignore_vulns:
        ignore_args.extend(["--ignore", vuln])

    argv = [
        downloaded_uv.exe,
        "pip",
        "audit",
        f"--output-format={request.output_format}",
        *ignore_args,
    ]

    process = Process(
        argv=argv,
        input_digest=input_digest,
        description="Run uv security audit",
        level=LogLevel.DEBUG,
    )

    result = await execute_process(process, **implicitly())

    stdout = result.stdout.decode()
    stderr = result.stderr.decode()

    # Parse vulnerability count from output (simplified)
    vulnerabilities_found = 0
    if result.exit_code != 0:
        # Count lines that look like vulnerability reports
        for line in stdout.split("\n"):
            if "vulnerability" in line.lower() or "CVE-" in line or "GHSA-" in line:
                vulnerabilities_found += 1

    return AuditResult(
        exit_code=result.exit_code,
        stdout=stdout,
        stderr=stderr,
        vulnerabilities_found=vulnerabilities_found,
    )


def rules() -> Iterable:
    """Return all audit rules."""
    return collect_rules()
