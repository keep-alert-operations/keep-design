"""Check local Markdown targets, fences, catalog sections and decision-register identifiers."""
import json
from pathlib import Path, PurePosixPath
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SIBLING_REPOSITORIES = {
    f'appchi-{name}' for name in (
        'frontend', 'api', 'ingestion', 'processor', 'correlation', 'indexer',
        'domain', 'contracts', 'migrations', 'delivery',
    )
}


def heading_titles(lines):
    """ATX/setext titles outside fenced code, matching appchi-delivery/scripts/context.py."""
    titles, fence, previous = [], None, None
    for line in lines:
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if fence:
            if (marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence)
                    and not marker[2].strip()):
                fence = None
            previous = None
            continue
        if marker:
            fence, previous = marker[1], None
            continue
        atx = re.match(r'^ {0,3}(#{1,6})(?:[ \t]+(.*?)|[ \t]*)$', line)
        if atx:
            titles.append(re.sub(r'[ \t]+#+[ \t]*$', '', atx[2] or ''))
        elif re.match(r'^ {0,3}(=+|-+)\s*$', line) and previous is not None:
            titles.append(previous)
        else:
            previous = line.strip() if line.strip() and not line.startswith(('    ', '\t')) else None
            continue
        previous = None
    return titles


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
# The resolver selects sections by exact heading title. Check design-owned sources
# here so a renamed heading fails in design CI; delivery checks sibling sources.
catalog = json.loads((ROOT / 'context/task-map.json').read_text(encoding='utf-8-sig'))
sections = 0
# Scope sections travel with every partial read of their document, so check them too.
references = [(source_id, source['path'], source['sections'])
              for source_id, source in catalog['sources'].items()]
references += [(f'scope_sections[{path}]', path, titles)
               for path, titles in catalog.get('scope_sections', {}).items()]
for label, path, wanted in references:
    parts = PurePosixPath(path).parts
    if parts[0] != 'appchi-design':
        continue
    target = ROOT.joinpath(*parts[1:])
    if not target.is_file():
        errors.append(f'context/task-map.json: {label} missing {path}')
        continue
    text = target.read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')
    titles = heading_titles(text.splitlines())
    for title in wanted:
        sections += 1
        if (found := titles.count(title)) != 1:
            errors.append(f'context/task-map.json: {label} heading {title!r} must exist '
                          f'exactly once in {path} (found {found})')
register = (ROOT / 'decisions/design-register.md').read_text(encoding='utf-8')
ids = {int(value) for value in re.findall(r'^(?:\|\s*|##\s*)REV-(\d+)', register, re.M)}
if ids != set(range(1, 62)):
    errors.append('Expected REV-01 through REV-61')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'Local document targets, fences, {sections} design-owned catalog sections '
      'and review identifiers passed.')
if deferred:
    print(f'Deferred {len(deferred)} context links to absent sibling checkouts; '
          'run appchi-delivery/qualification/check_context.py in the complete workspace.')
