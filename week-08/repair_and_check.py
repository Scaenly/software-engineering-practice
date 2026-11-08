#!/usr/bin/env python3
"""Apply the two reviewed repairs after the real chat comparison; save actual runs.

Usage from week-08/: py repair_and_check.py
After editing the report: py repair_and_check.py --sync-only
This helper never creates SKILL.md, assistant answers, screenshots or a conclusion.
"""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / 'lab-report.md'
ENV = {**os.environ, 'NO_COLOR': '1', 'FORCE_COLOR': '0'}


def run(args, cwd=ROOT):
    return subprocess.run(args, cwd=cwd, env=ENV, text=True, encoding='utf-8', errors='replace',
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def checker():
    result = run([sys.executable, 'tests/check_debugging.py', '--json'])
    return json.loads(result.stdout)


def section(number, body):
    text = REPORT.read_text(encoding='utf-8')
    pattern = r'(?ms)(^#{2,3} ' + re.escape(number) + r'(?:\.)? [^\n]*\n)(.*?)(?=^#{2,3} \d+\.|\Z)'
    match = re.search(pattern, text)
    if not match:
        raise SystemExit('Missing report section ' + number)
    REPORT.write_text(text[:match.start(2)] + '\n' + body.rstrip() + '\n\n' + text[match.end(2):], encoding='utf-8')


def git_commit(message):
    result = run(['git', 'add', 'week-08'], ROOT.parent)
    if result.returncode:
        raise SystemExit(result.stdout)
    result = run(['git', 'commit', '-m', message], ROOT.parent)
    print(result.stdout)
    if result.returncode:
        raise SystemExit('Commit failed. Fix Git identity/configuration before proceeding.')


def save_run(name, args):
    result = run(args, ROOT / 'app')
    (ROOT / 'evidence' / name).write_text(result.stdout, encoding='utf-8')
    print(result.stdout)
    return result


def sync():
    result = checker()
    bad = [row for row in result['rows'] if row['verdict'] != 'PASS']
    rows = '\n'.join('| ' + row['id'] + ' | ' + row['message'].replace('|', '/') + ' |' for row in bad)
    section('9.1', 'Current real checker results; unfinished work is declared below.\n\n'
            '| Check | Why it stays |\n| --- | --- |\n' + (rows or '| none | No FAIL or ERROR in the current run. |'))
    result = checker()
    (ROOT / 'evidence/checker-last.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    path = ROOT / 'submission.yml'
    text = path.read_text(encoding='utf-8')
    values = result['counts']
    for key, verdict in [('pass', 'PASS'), ('fail', 'FAIL'), ('error', 'ERROR')]:
        text = re.sub(r'(?m)^  ' + key + r':.*$', '  ' + key + ': ' + str(values[verdict]), text)
    commit = run(['git', 'rev-parse', '--short', 'HEAD'], ROOT.parent)
    if commit.returncode:
        raise SystemExit(commit.stdout)
    text = re.sub(r'(?m)^  commit:.*$', '  commit: "' + commit.stdout.strip() + '"', text)
    bad_ids = [row['id'] for row in result['rows'] if row['verdict'] != 'PASS']
    text = re.sub(r'(?m)^  known_fails:.*$', '  known_fails: [' + ', '.join(bad_ids) + ']', text)
    measured = result['measured']
    facts = {'tests_final': measured.get('tests_final'),
             'buggy_failed': (measured.get('buggy_run') or {}).get('failed'),
             'defects_logged': measured.get('defects_logged'),
             'lines_changed': measured.get('lines_changed')}
    for key, value in facts.items():
        if value is not None:
            text = re.sub(r'(?m)^  ' + key + r':.*$', '  ' + key + ': ' + str(value), text)
    path.write_text(text, encoding='utf-8')
    for command, filename in [(['tests/check_debugging.py'], 'checker-last.txt'),
                               (['tests/validate_submission.py'], 'validator-last.txt')]:
        check = run([sys.executable] + command)
        (ROOT / 'evidence' / filename).write_text(check.stdout, encoding='utf-8')
        print(check.stdout)
    print('Counts and known_fails now match the files. Read every remaining failure.')


def repair():
    branch = run(['git', 'branch', '--show-current'], ROOT.parent)
    if branch.stdout.strip() != 'week-08':
        raise SystemExit('Switch to branch week-08 first.')
    required = {'K1', 'K2', 'K3', 'K4', 'K5', 'K6', 'K7', 'L3', 'L4', 'L5', 'L6'}
    missing = [row['id'] for row in checker()['rows']
               if row['id'] in required and row['verdict'] != 'PASS']
    if missing:
        raise SystemExit('No patch applied. Complete the handwritten skill, ZIP, actual fresh-chat answers '
                         'and comparison first. Incomplete checks: ' + ', '.join(missing))
    # These are the only two permitted edits to the provided function.
    path = ROOT / 'app/src/booking.ts'
    code = path.read_text(encoding='utf-8')
    old_a = '    if (start <= b.end && end >= b.start) return false;'
    new_a = '    if (start < b.end && end > b.start) return false;'
    old_b = '  bookings.push({ start, end });\n'
    if old_a not in code and new_a not in code:
        raise SystemExit('Unexpected canBook body. No patch applied.')
    cli = ROOT / 'app/node_modules/vitest/vitest.mjs'
    if not cli.is_file():
        raise SystemExit('Vitest is not installed. Run npm ci inside week-08/app first. No patch applied.')
    command = ['node', str(cli), 'run']
    preflight = run(['node', str(cli), '--version'], ROOT / 'app')
    if preflight.returncode:
        raise SystemExit(preflight.stdout + '\nVitest could not start. No patch applied.')
    if old_a in code:
        git_commit('week-08: record skill and controlled diagnosis comparison')
        path.write_text(code.replace(old_a, new_a, 1), encoding='utf-8', newline='\n')
        diff = run(['git', 'diff', '--', 'app/src/booking.ts']).stdout
        targeted = save_run('04-fix-A-targeted.txt', command + ['-t', 'BUG-A'])
        full = save_run('05-fix-A-full.txt', command)
        section('8.1', 'The helper applied the reviewed one-line BUG-A patch. The full run still exposes BUG-B.\n\n'
                '```diff\n' + diff.rstrip() + '\n```\n\n```text\n' + targeted.stdout.rstrip()
                + '\n```\n\n```text\n' + full.stdout.rstrip() + '\n```')
        if targeted.returncode or not full.returncode:
            raise SystemExit('Unexpected BUG-A verification result. Inspect the saved logs before committing.')
        git_commit('week-08: fix BUG-A')
    code = path.read_text(encoding='utf-8')
    if old_b in code:
        path.write_text(code.replace(old_b, '', 1), encoding='utf-8', newline='\n')
        diff = run(['git', 'diff', '--', 'app/src/booking.ts']).stdout
        targeted = save_run('06-fix-B-targeted.txt', command + ['-t', 'BUG-B'])
        full = save_run('07-final-suite.txt', command)
        section('8.2', 'The helper deleted the single bookings.push line for BUG-B. Actual targeted and full runs follow.\n\n'
                '```diff\n' + diff.rstrip() + '\n```\n\n```text\n' + targeted.stdout.rstrip()
                + '\n```\n\n```text\n' + full.stdout.rstrip() + '\n```')
        if targeted.returncode or full.returncode:
            raise SystemExit('BUG-B verification failed. Inspect the logs before committing.')
        usage_path = ROOT / 'AI_USAGE.md'
        usage = usage_path.read_text(encoding='utf-8')
        usage = usage.replace('no — no repair has been applied yet. If repair_and_check.py is used, disclose that the Codex-authored helper applies and commits the two reviewed one-line changes.',
                              'no — after the diagnostic replies and comparison, the Codex-authored repair_and_check.py applied the reviewed strict-comparison change for BUG-A and deleted only bookings.push for BUG-B. Each change has its own targeted/full runs and separate commit; the comment was retained.')
        usage_path.write_text(usage, encoding='utf-8', newline='\n')
        description = ROOT / 'PR_DESCRIPTION.md'
        body = description.read_text(encoding='utf-8')
        match = re.search(r'(?ms)(^## What I built\n)(.*?)(?=^## |\Z)', body)
        if match:
            summary = ('\nContinued the actual Week 07 Smart Campus app, preserving all 27 tests and adding BUG-A and BUG-B regressions. '
                       'The provided unchanged function failed 9/27 original tests and 11/29 after adding both regressions. '
                       'Recorded the two fresh diagnostic chats on identical inputs, using a declared prompt-only simulation for the skill. '
                       'Applied one line per bug in separate commits, with actual targeted and full runs saved in report section 8. '
                       'The final full Vitest run passed; the personal report sections and final checker results must be reviewed before submission.\n\n')
            body = body[:match.start(2)] + summary + body[match.end(2):]
        body = body.replace('The controlled diagnostic chats are not yet performed.',
                            'The controlled diagnostic chats were completed; the skill environment was a prompt-only simulation.')
        description.write_text(body, encoding='utf-8', newline='\n')
        git_commit('week-08: fix BUG-B')
    # The supplied checker inspects physical folders, including ignored dependencies.
    # Dependencies are reproducible with npm ci and must not be in the export.
    dependencies = ROOT / 'app/node_modules'
    if dependencies.is_dir():
        shutil.rmtree(dependencies)
    sync()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sync-only', action='store_true')
    args = parser.parse_args()
    os.chdir(ROOT)
    sync() if args.sync_only else repair()
