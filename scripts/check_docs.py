"""Check local Markdown targets, fences and decision-register identifiers."""
from pathlib import Path
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SIBLING_REPOSITORIES = {
    f'appchi-{name}' for name in (
        'frontend', 'api', 'ingestion', 'processor', 'correlation', 'indexer',
        'domain', 'contracts', 'migrations', 'delivery',
    )
}
errors = []
deferred = set()
for path in ROOT.rglob('*.md'):
    text = path.read_text(encoding='utf-8-sig')
    if len(re.findall(r'^\s*(?:```|~~~)', text, re.M)) % 2:
        errors.append(f'{path.relative_to(ROOT)}: unbalanced fences')
    prose = re.sub(r'^\s*(```|~~~).*?^\s*\1\s*$', '', text, flags=re.M | re.S)
    for link in re.findall(r'\]\(([^\n)]+)\)', prose):
        if re.match(r'[a-z]+:', link) or link.startswith('#'):
            continue
        target = (path.parent / unquote(link.strip('<>').split('#')[0])).resolve()
        # The context graph links real sibling files. A standalone design clone
        # cannot validate those; the full delivery gate must do so after bootstrap.
        try:
            relative = target.relative_to(ROOT.parent)
        except ValueError:
            relative = None
        if (path.is_relative_to(ROOT / 'context') and relative is not None
                and relative.parts and relative.parts[0] in SIBLING_REPOSITORIES
                and not (ROOT.parent / relative.parts[0]).exists()):
            deferred.add(relative.as_posix())
            continue
        if not target.exists():
            errors.append(f'{path.relative_to(ROOT)}: missing {link}')
register = (ROOT / 'decisions/design-register.md').read_text(encoding='utf-8')
ids = {int(value) for value in re.findall(r'^(?:\|\s*|##\s*)REV-(\d+)', register, re.M)}
if ids != set(range(1, 39)):
    errors.append('Expected REV-01 through REV-38')
if errors:
    raise SystemExit('\n'.join(errors))
print('Local document targets, fences and review identifiers passed.')
if deferred:
    print(f'Deferred {len(deferred)} context links to absent sibling checkouts; '
          'run appchi-delivery/qualification/check_context.py in the complete workspace.')
