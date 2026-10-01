"""Check local Markdown targets, fences and decision-register identifiers."""
from pathlib import Path
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
errors = []
for path in ROOT.rglob('*.md'):
    text = path.read_text(encoding='utf-8-sig')
    if len(re.findall(r'^\s*(?:```|~~~)', text, re.M)) % 2:
        errors.append(f'{path.relative_to(ROOT)}: unbalanced fences')
    prose = re.sub(r'^\s*(```|~~~).*?^\s*\1\s*$', '', text, flags=re.M | re.S)
    for link in re.findall(r'\]\(([^\n)]+)\)', prose):
        if re.match(r'[a-z]+:', link) or link.startswith('#'):
            continue
        if not (path.parent / unquote(link.strip('<>').split('#')[0])).exists():
            errors.append(f'{path.relative_to(ROOT)}: missing {link}')
register = (ROOT / 'decisions/design-register.md').read_text(encoding='utf-8')
ids = {int(value) for value in re.findall(r'^(?:\|\s*|##\s*)REV-(\d+)', register, re.M)}
if ids != set(range(1, 39)):
    errors.append('Expected REV-01 through REV-38')
if errors:
    raise SystemExit('\n'.join(errors))
print('Local document targets, fences and review identifiers passed.')
