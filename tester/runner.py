from datetime import datetime, timezone
from tester.tests import ALL_TESTS


def run_all():
    results = [t() for t in ALL_TESTS]

    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    total = len(results)
    error_rate = round(failed / total, 3) if total else 0

    latencies = [r["latency_ms"] for r in results if r["latency_ms"] is not None]
    latency_avg = round(sum(latencies) / len(latencies), 2) if latencies else None
    if latencies:
        sorted_lat = sorted(latencies)
        idx = max(0, int(len(sorted_lat) * 0.95) - 1)
        latency_p95 = sorted_lat[idx]
    else:
        latency_p95 = None

    run = {
        "api": "ipify",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "passed": passed,
            "failed": failed,
            "error_rate": error_rate,
            "latency_avg_ms": latency_avg,
            "latency_p95_ms": latency_p95,
        },
        "tests": results,
    }
    return run
