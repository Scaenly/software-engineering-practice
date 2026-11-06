"""Fill submission.yml using the REAL local checker and current Git HEAD.

Save this script in week-07 and run from the repository root:
    py week-07/sync_submission.py

The supplied checker/validator, source code, tests and raw logs are never edited.
The script updates report section 9.1 and submission.yml, and saves checker output.
"""

import json
import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent
REPORT = ROOT / "lab-report.md"
EVIDENCE = ROOT / "evidence"
ENV = dict(os.environ, PYTHONUTF8="1")


def git(*args):
    result = subprocess.run(
        ["git", *args], cwd=REPOSITORY,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", errors="replace",
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip())
    return result.stdout.strip()


def checker():
    proc = subprocess.run(
        [sys.executable, "tests/check_suite.py", "--json"],
        cwd=ROOT, env=ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", errors="replace",
    )
    try:
        data = json.loads(proc.stdout)
    except ValueError:
        raise RuntimeError("Checker did not return JSON: " + (proc.stderr or proc.stdout))
    if not all(key in data for key in ("rows", "counts", "measured")):
        raise RuntimeError("Checker could not inspect the project: " + str(data))
    return data


def sync_known_fails(data):
    rows = [row for row in data["rows"] if row["verdict"] != "PASS"]
    body = "This table comes from the actual local checker run. Functional limitations that do not have a checker ID are discussed in sections 8 and 9.2.\n\n"
    body += "| Check | Why it stays |\n| --- | --- |\n"
    if not rows:
        body += "| none | The current local checker reported no FAIL or ERROR |\n"
    for row in rows:
        reason = row["message"].replace("|", "/").replace("\n", " ")
        if row["id"] == "L8":
            reason += "; complete section 10 in your own words and rerun this script before submission"
        body += "| " + row["id"] + " | " + reason + " |\n"
    body += "\n"
    current = REPORT.read_text(encoding="utf-8")
    pattern = r"(?ms)(^### 9\.1[^\n]*\n).*?(?=^### 9\.2)"
    updated, count = re.subn(pattern, lambda match: match.group(1) + "\n" + body, current)
    if count != 1:
        raise RuntimeError("Could not locate report section 9.1 exactly once")
    if updated != current:
        REPORT.write_text(updated, encoding="utf-8")


def declaration(data, commit, summary):
    measured = data["measured"]
    first_run = measured.get("first_run") or {}
    values = {
        "tests_first": measured.get("tests_first"),
        "tests_final": measured.get("tests_final"),
        "first_run_failed": first_run.get("failed"),
        "review_decisions": measured.get("review_decisions"),
        "mutants_detected": measured.get("mutants_detected"),
    }
    missing = [key for key, value in values.items() if not isinstance(value, int)]
    if missing:
        raise RuntimeError("Missing measured values; fix the report/project first: " + ", ".join(missing))
    quote = lambda value: json.dumps(str(value), ensure_ascii=False)
    known = [row["id"] for row in data["rows"] if row["verdict"] != "PASS"]
    lines = [
        "# Generated from the actual local checker; do not copy unverified counts.",
        "schema: 1", 'week: "07"', "", "student:",
        "  name: " + quote("Yerassyl Arystanbek"),
        "  student_id: " + quote("24B030280"),
        "  github: " + quote("scaenly"), "", "assistant:",
        "  tool: " + quote("ChatGPT"),
        "  model: " + quote("not displayed"), "", "project:",
        "  baseline: week-06", "  bolt_url: not-shared",
        "  vitest: " + quote(measured.get("vitest_version") or "5.1.0"),
        "", "counts:",
    ]
    lines += ["  " + key + ": " + str(value) for key, value in values.items()]
    lines += ["", "checker:"]
    lines += ["  " + key.lower() + ": " + str(data["counts"][key])
              for key in ("PASS", "FAIL", "ERROR")]
    lines += [
        "  commit: " + quote(commit),
        "  known_fails: [" + ", ".join(known) + "]", "", "assumptions:",
        "  invalid_existing_booking: " + quote(summary["invalid_existing_booking"]),
        "", "review_findings:",
    ]
    findings = [
        "AC5: the first dedicated test duplicated T01; the improved test checks unsorted data after two Available calls",
        "AC1: the original suite missed a start earlier than now; T15 and T16 add the neighbouring current-time boundaries",
        "M1: rejecting exactly 120 minutes was detected by T06 using the unchanged suite",
        "M2: closed-endpoint overlap was detected by T01, T08 and T23",
        "M3: removing the blocked-room rejection was detected by T13 and T24",
        "App.tsx: the day-range helper label still displays 00:00-00:00 and is documented as a UI limitation",
        "booking.test.ts: T17 also violates the future-start rule, so it does not independently test the lower-bound guard",
        "booking.test.ts: a duplicate download suffix initially prevented test discovery; renaming the file restored discovery",
    ]
    lines += ["  - " + quote(finding) for finding in findings]
    lines += ["", "honesty:"]
    honesty = {
        "first_suite_unedited": "yes" if summary.get("first_suite_unchanged") else "no",
        "outputs_unedited": "yes",
        "mutants_restored": "yes" if summary.get("module_restored") else "no",
        "ai_usage_disclosed": "yes",
    }
    lines += ["  " + key + ": " + value for key, value in honesty.items()]
    return "\n".join(lines) + "\n"


def main():
    for path in (REPORT, ROOT / "tests/check_suite.py", ROOT / "tests/validate_submission.py",
                 EVIDENCE / "mutation-summary.json"):
        if not path.is_file():
            raise RuntimeError("Missing: " + str(path))
    if git("branch", "--show-current") != "week-07":
        raise RuntimeError("Run this on branch week-07. No branch was changed by this script.")
    summary = json.loads((EVIDENCE / "mutation-summary.json").read_text(encoding="utf-8"))
    if summary.get("invalid_existing_booking") not in ("returns-true", "returns-false", "throws"):
        raise RuntimeError("The invalid-existing-booking probe is incomplete")

    commit = git("rev-parse", "--short", "HEAD")
    data = checker()
    sync_known_fails(data)
    data = checker()
    sync_known_fails(data)
    (ROOT / "submission.yml").write_text(declaration(data, commit, summary), encoding="utf-8")
    (EVIDENCE / "checker-last.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    validation = subprocess.run(
        [sys.executable, "tests/validate_submission.py", "--json"],
        cwd=ROOT, env=ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", errors="replace",
    )
    try:
        validated = json.loads(validation.stdout)
    except ValueError:
        raise RuntimeError("Validator did not return JSON: " + (validation.stderr or validation.stdout))
    (EVIDENCE / "validator-last.json").write_text(
        json.dumps(validated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    counts = data["counts"]
    print("Checker: pass={PASS} fail={FAIL} error={ERROR}".format(**counts))
    print("checker.commit: " + commit)
    print("Tests: first={tests_first}, final={tests_final}".format(**data["measured"]))
    for row in data["rows"]:
        if row["verdict"] != "PASS":
            print(row["verdict"] + " " + row["id"] + ": " + row["message"])
    validation_counts = validated.get("counts", {})
    print("Validator: " + str(validation_counts))
    for row in validated.get("rows", []):
        if row["verdict"] != "PASS":
            print(row["verdict"] + " " + row["id"] + ": " + row["message"])
    commits = git("log", "--format=%h %s", "origin/main..HEAD")
    count = len(commits.splitlines()) if commits else 0
    print("Commits ahead of origin/main: " + str(count))
    print("submission.yml and report section 9.1 now match the local checker.")
    print("Complete the personal self-assessment in AI_USAGE.md and the Time spent line in PR_DESCRIPTION.md before submission.")
    return 0 if data.get("ok") and validated.get("ok") else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, RuntimeError, ValueError, KeyError) as error:
        print("STOP: " + str(error), file=sys.stderr)
        sys.exit(1)
