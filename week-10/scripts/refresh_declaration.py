"""Record actual checker results; never certify a student's personal review."""
import json
from pathlib import Path
import re
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
run = subprocess.run(
    [sys.executable, 'tests/check_audit.py', '--json'],
    cwd=root, capture_output=True, text=True, check=False,
)
data = json.loads(run.stdout)
counts, measured = data['counts'], data['measured']
commit = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], cwd=root, text=True).strip()
path = root / 'submission.yml'
text = path.read_text(encoding='utf-8')

def update(section, key, value):
    global text
    start = re.search(rf'(?m)^{re.escape(section)}:\s*$', text)
    if not start:
        raise ValueError(f'Missing section {section}')
    end_match = re.search(r'(?m)^\S', text[start.end():])
    end = start.end() + end_match.start() if end_match else len(text)
    body = text[start.end():end]
    body, number = re.subn(rf'(?m)^  {re.escape(key)}:.*$', f'  {key}: {value}', body)
    if number != 1:
        raise ValueError(f'Expected one {section}.{key}, found {number}')
    text = text[:start.end()] + body + text[end:]

for key, value in [('pass', counts['PASS']), ('fail', counts['FAIL']), ('error', counts['ERROR']), ('commit', commit)]:
    update('checker', key, value)
bad = [row['id'] for row in data['rows'] if row['verdict'] != 'PASS']
update('checker', 'known_fails', '[' + ', '.join(bad) + ']')
for key, value in {
    'claims_challenged': measured['claims_challenged'],
    'risks_registered': measured['risks_registered'],
    'risks_confirmed': measured['risks_confirmed'],
    'tests_final': measured['final_run']['total'],
    'agents_lines_changed': measured['agents_lines_changed'],
}.items():
    update('counts', key, value)
path.write_text(text, encoding='utf-8')
(root / 'evidence/checker-last.json').write_text(run.stdout, encoding='utf-8')
print(f'Recorded actual checker results at {commit}: {counts}; known_fails={bad}')
print('Personal review answers and manual UI observations were not changed.')
