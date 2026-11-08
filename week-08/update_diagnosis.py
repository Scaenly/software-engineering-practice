#!/usr/bin/env python3
"""Merge the student's two actual chat replies into the report; do not repair code.

Run from week-08 after reading your own SKILL.md:
    py update_diagnosis.py --skill-reviewed
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent


def replace_section(text, number, body):
    pattern = r'(?ms)(^#{2,3} ' + re.escape(number) + r'(?:\.)? [^\n]*\n)(.*?)(?=^#{2,3} \d+\.|\Z)'
    match = re.search(pattern, text)
    if not match:
        raise SystemExit('Missing report section ' + number + '; no report written.')
    return text[:match.start(2)] + '\n' + body.rstrip() + '\n\n' + text[match.end(2):]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skill-reviewed', action='store_true',
                        help='Student confirms having personally read the complete SKILL.md once.')
    args = parser.parse_args()
    if not args.skill_reviewed:
        raise SystemExit('Read your complete SKILL.md once, then run with --skill-reviewed. No code is changed.')
    required = ['lab-report.md', 'AI_USAGE.md', 'submission.yml', 'skills/bug-detector/SKILL.md',
                'skills/bug-detector.zip', 'evidence/install.png',
                'evidence/without-skill-answer.md', 'evidence/with-skill-answer.md',
                'prompts/01-without-skill.txt', 'prompts/02-with-skill.txt']
    missing = [p for p in required if not (ROOT / p).is_file()]
    if missing:
        raise SystemExit('Missing files: ' + ', '.join(missing))
    skill_bytes = (ROOT / 'skills/bug-detector/SKILL.md').read_bytes()
    skill = skill_bytes.decode('utf-8-sig').replace('\r\n', '\n')
    reference = (ROOT / 'README.md').read_text(encoding='utf-8')
    reference = re.search(r'```text\n(---\nname: bug-detector\n.*?)```', reference, re.S)
    if not reference or skill.strip() != reference.group(1).strip():
        raise SystemExit('SKILL.md differs from the prescribed deck text; review it before continuing.')
    with zipfile.ZipFile(ROOT / 'skills/bug-detector.zip') as archive:
        entry = next((n for n in archive.namelist() if n.replace('\\', '/') == 'bug-detector/SKILL.md'), None)
        if entry is None:
            raise SystemExit('The ZIP must contain bug-detector/SKILL.md inside its top-level folder.')
        if archive.read(entry) != skill_bytes:
            raise SystemExit('The ZIP skill differs from your saved SKILL.md. Recreate the ZIP first.')
        listing = '\n'.join(f'{i.filename} ({i.file_size} bytes)' for i in archive.infolist())
    sent = [(ROOT / 'prompts' / p).read_text(encoding='utf-8').strip()
            for p in ['01-without-skill.txt', '02-with-skill.txt']]
    if sent[0].split('\n\n', 1)[1] != sent[1].split('\n\n', 1)[1]:
        raise SystemExit('The two prepared inputs differ beyond the question. Review what was actually sent.')
    answers = [(ROOT / 'evidence' / p).read_text(encoding='utf-8').rstrip('\n')
               for p in ['without-skill-answer.md', 'with-skill-answer.md']]
    report_path = ROOT / 'lab-report.md'
    report = report_path.read_text(encoding='utf-8')
    backup = ROOT / 'evidence/lab-report-before-diagnosis.md'
    if not backup.exists():
        backup.write_bytes(report_path.read_bytes())
    report = report.replace('Student-only activities remain explicitly incomplete; no fresh-chat comparison or skill installation is claimed.',
                            'The student subsequently supplied two fresh-chat diagnostic replies and a screenshot of the acknowledged prompt-only simulation. The comparison is an AI-assisted draft for student review; no installed skill is claimed.')
    report = report.replace('ChatGPT / Codex for preparation; two controlled diagnostic chats pending',
                            'ChatGPT for both fresh diagnostic chats; Codex assisted preparation and report drafting')
    report = report.replace('Not installed; prompt-only simulation planned, not yet performed',
                            'Prompt-only simulation in a separate ChatGPT chat; no installed skill')
    report = report.replace('Personal pre-AI hypothesis was not captured. The test failure is recorded; student review is still needed.',
                            'Personal pre-AI hypothesis was not captured. AI-reviewed cause: inclusive comparisons count endpoint equality as a conflict; AC4 requires strict comparisons.')
    report = report.replace('Personal pre-AI hypothesis was not captured. The independent non-touching test reaches the mutation; student review is still needed.',
                            'Personal pre-AI hypothesis was not captured. AI-reviewed cause: bookings.push appends a request during an availability check; the non-touching fixture reaches it independently of BUG-A.')
    checks = '''The source file and the committed ZIP were checked locally by update_diagnosis.py. The fourth answer records the student's --skill-reviewed declaration, after personally reading the complete file.

| Check | yes / no |
| --- | --- |
| The file is plain UTF-8 text, named exactly `SKILL.md` (not `SKILL.md.txt`) | yes |
| The first and the closing YAML delimiter are exactly three hyphens: `---` | yes |
| `name` is lowercase with hyphens, and `description` says WHEN to use it | yes |
| I read the whole file once: no passwords, API keys or private student data | yes |

**The contents of `skills/bug-detector.zip`**, read from the actual local ZIP:

```text
''' + listing + '''
```

**Installation.**

<!-- Write below this line -->

The declared environment is a prompt-only simulation, not an installed skill. In a fresh ChatGPT chat, the student first supplied the complete hand-typed procedure with an explicit simulation statement. The assistant acknowledged: "I'll follow the procedure directly without searching for a skill or editing code." The student then sent the prepared diagnostic input. The supplied screenshot is evidence/install.png. No installed-skill badge is shown. An earlier unsuccessful request reported that bug-detector could not be found; it is disclosed in evidence/skill-attempt-note.md and is not used as the controlled simulation response.
'''
    report = replace_section(report, '4', checks)
    for i in range(2):
        body = ('Fresh ChatGPT chat without a loaded bug-detector procedure. ' if i == 0 else
                'A separate fresh ChatGPT chat using the explicitly declared prompt-only procedure. ')
        body += 'The student supplied this complete answer; the exact model is not displayed in the supplied evidence.\n\n'
        body += '**The diagnostic message sent:**\n\n```text\n' + sent[i] + '\n```\n\n'
        body += "**The assistant's answer, pasted unedited:**\n\n````markdown\n" + answers[i] + '\n````\n\n'
        body += 'The corresponding complete reply is also preserved in evidence/' + ('without-skill-answer.md' if i == 0 else 'with-skill-answer.md') + '.\n'
        if i == 1:
            body += '\nDid the environment show that the skill was invoked? **not shown** as an installed skill. The chat explicitly acknowledged the pasted procedure; the declared mode is prompt-only.\n'
        report = replace_section(report, str(5 + i), body)
    comparison = '''AI-assisted comparison draft: each judgement below is checked against the provided code and the existing real test failures. The student must review this table before accepting the patches.

| Criterion | No skill | With skill |
| --- | --- | --- |
| Correct root cause | Correct for both BUG-A/AC4 and BUG-B/AC5. The inclusive overlap condition rejects equality; bookings.push changes the caller's array. The real T01 failure and non-touching BUG-B failure support these explanations. | Correct for the same two defects and the same expressions. The table names evidence separately; it does not identify an additional implementation defect. |
| Reproducible test | Proposes 780–840 with now 540 and existing 600–660. It is a deterministic free slot and isolates mutation from endpoint rejection; it asserts deep equality and exact true. | Proposes 720–780 with the same now and existing booking. This also isolates BUG-B, asserts the preserved array and exact true, and matches the new BUG-B fixture already in the suite. |
| Minimal proposed patch | Strict comparators fix BUG-A. Deleting bookings.push fixes BUG-B, but deleting its comment as well is unnecessary for this lab's one-line-per-bug rule. Modify that proposal: retain the comment and delete only the push. | The same judgement: accept strict comparisons, delete only bookings.push, and retain the comment. The skill does not prevent this unnecessary extra deletion. Do not add a duplicate AC5 test because the committed BUG-B regression already supplies it. |
| Unsupported claims | Reports an isolated JavaScript reproduction, but the supplied reply contains no raw terminal output. Treat that as an assistant claim; only saved project Vitest logs establish project results. No claim that AC6 was verified is made. | States that the function was run in Node, but supplies no raw terminal output for that execution. This does not establish that the project suite passes. It correctly states that AC6 cannot be assessed from the function. |
| Clarity of explanation | Clearly explains that T01 returns early and its first failed assertion masks the later mutation assertion. The small result table illustrates why fixing BUG-A alone exposes BUG-B. | Clearly explains the same masking. The required defect/evidence/root-cause/fix/test columns make the mapping easier to scan, while the technical diagnosis remains the same. |

**Which bugs did each answer find?** Both answers found BUG-A and BUG-B. Neither changed project files as part of the diagnostic reply. The suggested overall verdict is no-difference for diagnostic correctness; the simulation improved the visible structure. This is a single comparison and does not measure a general model-performance improvement.

**Patch review for the next step:** change the one overlap-condition line for BUG-A; delete only the single bookings.push line for BUG-B. The existing 27 Week 07 tests and the two new BUG-A/BUG-B regressions remain unchanged.
'''
    report = replace_section(report, '7', comparison)
    report_path.write_text(report, encoding='utf-8', newline='\n')
    usage_path = ROOT / 'AI_USAGE.md'
    usage = usage_path.read_text(encoding='utf-8')
    usage = usage.replace('This is an INCOMPLETE preparation record, not a signed claim that all lab activities are finished.',
                          'This disclosure records preparation and the actual controlled diagnostic chats. Student self-assessment, personal writing and signature still require completion.')
    usage = usage.replace('| Not yet performed | not displayed | diagnosis without the skill (Task 4)',
                          '| ChatGPT | not displayed | diagnosis without the skill in a fresh chat (Task 4)')
    usage = usage.replace('| Not yet performed | not displayed | diagnosis with bug-detector (Task 5)',
                          '| ChatGPT | not displayed | diagnosis with the supplied bug-detector procedure in a separate fresh chat; prompt-only simulation (Task 5)')
    usage = usage.replace('no — not created yet. The provided deck text must be typed by the student.',
                          'student must answer yes/no accurately — the file and ZIP now exist, and the screenshot records the skill commit 2c6fdf6. The report-update helper does not create or alter the skill.')
    usage = usage.replace('The two fresh chats, skill typing/packaging, screenshot, comparison, personal limitation, conclusion and self-assessment remain incomplete. Update this disclosure with the actual models and activities when completed.',
                          'The two controlled chat replies, the prompt-only screenshot and an AI-assisted comparison draft have now been supplied. An earlier unsuccessful skill request is also disclosed. The student must review the comparison, complete the personal limitation and conclusion, answer the self-assessment fields and sign this disclosure. Raw project terminal evidence is separate from assistant claims of isolated execution.')
    marker = '## Subsequent diagnosis and report assistance'
    if marker not in usage:
        usage += '\n' + marker + '\n\nCodex transcribed the two complete student-supplied diagnostic replies into evidence files and report sections 5–6, drafted the factual comparison in section 7, recorded the earlier failed skill attempt, and prepared update_diagnosis.py. Both replies proposed deleting an unnecessary comment; the reviewed repair retains it so BUG-B changes one line. No independent personal pre-AI hypothesis is claimed. The personal conclusion was not generated.\n'
    usage_path.write_text(usage, encoding='utf-8', newline='\n')
    declaration_path = ROOT / 'submission.yml'
    declaration = declaration_path.read_text(encoding='utf-8')
    declaration = re.sub(r'(?m)^  environment:.*$', '  environment: prompt-only', declaration)
    declaration = re.sub(r'(?m)^  invoked:.*$', '  invoked: not-shown', declaration)
    declaration = re.sub(r'(?m)^  same_input_both_chats:.*$', '  same_input_both_chats: yes', declaration)
    declaration = re.sub(r'(?m)^  skill_helped:.*$', '  skill_helped: no-difference # AI-assisted draft; student reviews section 7.', declaration)
    declaration_path.write_text(declaration, encoding='utf-8', newline='\n')
    print('Actual replies and prompt-only evidence recorded. Review lab-report.md section 7 before repair.')
    print('No booking code changed. Personal sections 9.2 and 10 remain for the student.')
    result = subprocess.run([sys.executable, str(ROOT / 'repair_and_check.py'), '--sync-only'], cwd=ROOT,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
    if result.returncode:
        print(result.stdout)
    else:
        checks = json.loads((ROOT / 'evidence/checker-last.json').read_text(encoding='utf-8'))
        unfinished = [r['id'] for r in checks['rows'] if r['verdict'] != 'PASS']
        print('Current checker counts:', checks['counts'])
        print('Current unfinished checks:', ', '.join(unfinished) or 'none')
        print('Full checker and validator logs are saved in evidence/. Repairs have not been applied by this updater.')
    return result.returncode


if __name__ == '__main__':
    raise SystemExit(main())
