#!/usr/bin/env python3
"""Validate the published skill and local references without external dependencies."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'cicero-machine'


def validate():
    errors = []
    text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
    match = re.match(r'\A---\nname: ([a-z0-9]+(?:-[a-z0-9]+)*)\ndescription: ([^\n]+)\n---\n', text)
    if not match or match[1] != SKILL.name:
        errors.append('Expected name and single-line description frontmatter')
    elif not 1 <= len(match[2]) <= 1024:
        errors.append('Description must have 1–1024 characters')
    if len(text.splitlines()) > 500:
        errors.append('SKILL.md exceeds 500 lines')
    for path in ROOT.rglob('*.md'):
        if '.git' in path.parts:
            continue
        body = path.read_text(encoding='utf-8')
        body = re.sub(r'```.*?```', '', body, flags=re.S)
        body = re.sub(r'`[^`\n]+`', '', body)
        for href in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)', body):
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (path.parent / unquote(parsed.path)).resolve()
            if not target.is_relative_to(ROOT) or not target.exists():
                errors.append(f'{path.relative_to(ROOT)}: missing/escaping reference {href}')
    for name in ('roles.md', 'report-template.md', 'runtime-adapters.md', 'upstream.md'):
        if f'(references/{name})' not in text:
            errors.append(f'SKILL.md does not link references/{name}')
    if (ROOT / 'LICENSE').read_bytes() != (SKILL / 'LICENSE').read_bytes():
        errors.append('Bundled license differs from repository license')
    metadata = (SKILL / 'agents' / 'openai.yaml').read_text(encoding='utf-8')
    for href in re.findall(r'icon_(?:small|large):\s*"([^"]+)"', metadata):
        if not (SKILL / href).is_file():
            errors.append(f'Missing icon: {href}')
    if '$cicero-machine' not in metadata:
        errors.append('Default prompt does not invoke the skill')
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'PASS: frontmatter, {len(text.splitlines())} skill lines, local links, references, license and UI metadata')
    return 0


if __name__ == '__main__':
    sys.exit(validate())
