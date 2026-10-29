#!/usr/bin/env python3
"""Copy the CiceroMachine skill to documented host directories; no network calls."""

import argparse
from datetime import datetime, timezone
import hashlib
import os
from pathlib import Path
import shutil
import tempfile
import uuid

REPO = Path(__file__).resolve().parents[1]
SOURCE = REPO / 'skills' / 'cicero-machine'
HOSTS = {'codex': '.agents', 'claude': '.claude', 'deepseek': '.dsh'}


def destinations(target, scope='user', project=None, home=None, environ=None):
    home = Path.home() if home is None else Path(home)
    environ = os.environ if environ is None else environ
    if scope == 'project':
        if project is None or not Path(project).is_dir():
            raise ValueError('--project must name an existing project root')
        base = Path(project).resolve()
    else:
        if project is not None:
            raise ValueError('--project requires --scope project')
        base = home
    selected = HOSTS if target == 'all' else [target]
    result = []
    for host in selected:
        root = base / HOSTS[host]
        if host == 'deepseek' and scope == 'user' and environ.get('DSH_HOME'):
            root = Path(environ['DSH_HOME']).expanduser()
            if not root.is_absolute():
                raise ValueError('DSH_HOME must be an absolute path')
        dest = root / 'skills' / SOURCE.name
        # Keep the final component unresolved so a pre-existing symlink is detected.
        dest = dest.parent.resolve() / dest.name
        if dest not in result:
            result.append(dest)
    return result


def manifest(root):
    if not root.is_dir() or root.is_symlink():
        raise ValueError(f'Expected a real directory: {root}')
    result = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise ValueError(f'Refusing symlink inside skill: {path}')
        if path.is_file():
            result[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def install(paths, *, source=SOURCE, replace=False, dry_run=False):
    expected = manifest(source)
    if 'SKILL.md' not in expected:
        raise ValueError('Source does not contain SKILL.md')
    plan = []
    for dest in paths:
        if dest.is_symlink() or (dest.exists() and not dest.is_dir()):
            raise ValueError(f'Refusing non-directory or symlink target: {dest}')
        if dest.resolve().is_relative_to(source.resolve()) or source.resolve().is_relative_to(dest.resolve()):
            raise ValueError(f'Source and target must not contain each other: {dest}')
        if dest.exists() and manifest(dest) == expected:
            plan.append((dest, 'unchanged'))
        elif dest.exists() and not replace:
            raise ValueError(f'Different skill already exists: {dest}; use --replace to back it up first')
        else:
            plan.append((dest, 'replace' if dest.exists() else 'install'))
    # Every destination is checked before any filesystem mutation.
    for dest, action in plan:
        print(f'{"DRY RUN " if dry_run else ""}{action}: {dest}')
        if dry_run or action == 'unchanged':
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        stage = Path(tempfile.mkdtemp(prefix='.cicero-stage-', dir=dest.parent))
        backup = None
        try:
            shutil.copytree(source, stage, dirs_exist_ok=True)
            if manifest(stage) != expected:
                raise RuntimeError('Staged copy failed integrity check')
            if action == 'replace':
                stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
                backup = dest.parent.parent / 'cicero-machine-backups' / f'{stamp}-{uuid.uuid4().hex[:8]}'
                backup.parent.mkdir(parents=True, exist_ok=True)
                dest.rename(backup)
            stage.rename(dest)
            if backup:
                print(f'backup: {backup}')
        except BaseException:
            if backup is not None and backup.exists() and not dest.exists():
                backup.rename(dest)
            raise
        finally:
            if stage.exists():
                shutil.rmtree(stage)
    return plan


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', choices=[*HOSTS, 'all'], required=True)
    parser.add_argument('--scope', choices=['user', 'project'], default='user')
    parser.add_argument('--project', type=Path)
    parser.add_argument('--replace', action='store_true', help='Back up a different existing version before replacing it')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        install(destinations(args.target, args.scope, args.project), replace=args.replace, dry_run=args.dry_run)
    except (ValueError, OSError, RuntimeError) as error:
        parser.exit(1, f'Install failed: {error}\n')


if __name__ == '__main__':
    main()
