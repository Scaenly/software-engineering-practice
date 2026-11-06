"""Run the three Week 07 mutants against the reviewed, passing suite.

Save this file in week-07/, then run: py week-07\run_mutants.py
Only booking.ts is changed temporarily. Its original bytes are restored in finally.
"""

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
APP = ROOT / "app"
EVIDENCE = ROOT / "evidence"
MODULE = APP / "src" / "booking.ts"
SUITE = APP / "src" / "booking.test.ts"
FIRST = ROOT / "suites" / "first" / "booking.test.ts"
ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")

MUTANTS = (
    ("M1", "end - start > MAX_BOOKING_MINUTES",
     "end - start >= MAX_BOOKING_MINUTES", {"T06"}),
    ("M2", "start < booking.end && booking.start < end",
     "start <= booking.end && booking.start <= end", {"T01", "T08"}),
    ("M3", "if (blocked) return false;",
     "/* M3: blocked-room rejection removed for this trial. */", {"T13"}),
)


def vitest(name):
    result = subprocess.run(
        "npx vitest run", cwd=APP, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    log = EVIDENCE / (name + ".txt")
    log.write_bytes(result.stdout)
    clean = ANSI.sub("", result.stdout.decode("utf-8", errors="replace"))
    summaries = re.findall(r"^\s*Tests\s+(.+)$", clean, re.MULTILINE)
    summary = summaries[-1].strip() if summaries else "No Tests summary found"
    failing_lines = [line.strip() for line in clean.splitlines()
                     if re.search(r"\bFAIL\b", line)]
    ids = sorted(set(re.findall(
        r"\b(?:T\d{2}|AC5|X\d+)\b", "\n".join(failing_lines))))
    data = {
        "returncode": result.returncode,
        "log": "evidence/" + log.name,
        "tests_summary": summary,
        "failing_tests": failing_lines,
        "failing_ids": ids,
        "assertion_failure": "AssertionError" in clean,
    }
    print(name + ": " + summary, flush=True)
    return data


def passing(run):
    return run["returncode"] == 0 and bool(
        re.search(r"\b\d+ passed\b", run["tests_summary"]))


def main():
    for path in (MODULE, SUITE, FIRST):
        if not path.is_file():
            raise RuntimeError("Missing required file: " + str(path))

    original = MODULE.read_bytes()
    source = original.decode("utf-8-sig")
    suite_before = SUITE.read_bytes()
    first_before = FIRST.read_bytes()
    first_count = len(re.findall(rb"\b(?:test|it)\s*\(", first_before))
    final_count = len(re.findall(rb"\b(?:test|it)\s*\(", suite_before))
    if first_count != 17:
        raise RuntimeError("The frozen first suite should contain the original 17 tests. Inspect suites/first/.")
    if b"".join(suite_before.split()) == b"".join(first_before.split()):
        raise RuntimeError("Install the improved suite in app/src before running mutant trials.")
    for name, old, new, expected_ids in MUTANTS:
        if source.count(old) != 1:
            raise RuntimeError(name + ": expected exactly one occurrence of: " + old)

    EVIDENCE.mkdir(exist_ok=True)
    backup = EVIDENCE / "booking-before-mutants.txt"
    if backup.exists() and backup.read_bytes() != original:
        raise RuntimeError("Existing backup differs from booking.ts; keep it and inspect before rerunning.")
    backup.write_bytes(original)

    results = {
        "tests_first": first_count,
        "tests_final": final_count,
        "suite_sha256": hashlib.sha256(suite_before).hexdigest(),
    }
    results["improved"] = vitest("improved-run")
    if not passing(results["improved"]):
        raise RuntimeError("The improved suite must pass before any mutant. See evidence/improved-run.txt")

    try:
        for name, old, new, expected_ids in MUTANTS:
            MODULE.write_bytes(source.replace(old, new, 1).encode("utf-8"))
            try:
                run = vitest(name)
                relevant_assertion = (
                    run["returncode"] != 0
                    and run["assertion_failure"]
                    and bool(expected_ids.intersection(run["failing_ids"]))
                )
                if relevant_assertion:
                    run["outcome"] = "Detected"
                elif run["returncode"] == 0:
                    run["outcome"] = "Survived"
                else:
                    run["outcome"] = "Error: no confirmed relevant assertion failure"
                results[name] = run
                print(name + " outcome: " + run["outcome"] + "; IDs: "
                      + ", ".join(run["failing_ids"]), flush=True)
            finally:
                MODULE.write_bytes(original)
            if SUITE.read_bytes() != suite_before or FIRST.read_bytes() != first_before:
                raise RuntimeError("A suite changed during a mutant trial; stop and inspect.")
    finally:
        MODULE.write_bytes(original)

    results["module_restored"] = MODULE.read_bytes() == original
    results["first_suite_unchanged"] = FIRST.read_bytes() == first_before
    results["final_suite_unchanged_during_trials"] = SUITE.read_bytes() == suite_before
    results["final"] = vitest("final-run")

    probe = subprocess.run(
        ["node", "--input-type=module", "-e",
         "import { canBook } from './src/booking.ts';"
         "console.log(canBook({start:660,end:720,now:540,blocked:false,"
         "bookings:[{start:700,end:650}]}));"],
        cwd=APP, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    (EVIDENCE / "invalid-existing.txt").write_bytes(probe.stdout)
    probe_text = ANSI.sub("", probe.stdout.decode("utf-8", errors="replace"))
    boolean_lines = re.findall(r"^\s*(true|false)\s*$", probe_text, re.MULTILINE)
    if probe.returncode == 0 and boolean_lines:
        results["invalid_existing_booking"] = "returns-" + boolean_lines[-1]
    else:
        results["invalid_existing_booking"] = "probe failed; inspect evidence/invalid-existing.txt"

    results["mutants_detected"] = sum(
        results.get(name, {}).get("outcome") == "Detected"
        for name, _, _, _ in MUTANTS)
    (EVIDENCE / "mutation-summary.json").write_text(
        json.dumps(results, indent=2) + "\n", encoding="utf-8")

    print("booking.ts restored: " + str(results["module_restored"]), flush=True)
    print("First suite unchanged: " + str(results["first_suite_unchanged"]), flush=True)
    print("Mutants detected: " + str(results["mutants_detected"]) + "/3", flush=True)
    print("Invalid existing booking: " + results["invalid_existing_booking"], flush=True)
    print("Full unchanged outputs are saved in week-07/evidence/.", flush=True)
    if not passing(results["final"]) or results["mutants_detected"] != 3:
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, OSError) as error:
        print("STOP: " + str(error), file=sys.stderr)
        sys.exit(1)
