import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import install


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.targets = install.destinations('all', home=self.root, environ={})
        self.quiet = contextlib.redirect_stdout(io.StringIO())
        self.quiet.__enter__()
        self.addCleanup(self.quiet.__exit__, None, None, None)

    def test_three_host_paths_and_custom_dsh_home(self):
        self.assertEqual([str(x.relative_to(self.root)) for x in self.targets], [
            '.agents/skills/cicero-machine', '.claude/skills/cicero-machine', '.dsh/skills/cicero-machine'])
        custom = self.root / 'dsh-home'
        result = install.destinations('deepseek', home=self.root, environ={'DSH_HOME': str(custom)})
        self.assertEqual(result, [custom / 'skills/cicero-machine'])

    def test_project_paths_ignore_user_override(self):
        result = install.destinations('deepseek', 'project', self.root, environ={'DSH_HOME': '/unused'})
        self.assertEqual(result, [self.root / '.dsh/skills/cicero-machine'])

    def test_install_and_idempotence(self):
        install.install(self.targets)
        for path in self.targets:
            self.assertEqual(install.manifest(path), install.manifest(install.SOURCE))
        self.assertTrue(all(action == 'unchanged' for _, action in install.install(self.targets)))

    def test_dry_run_writes_nothing(self):
        install.install(self.targets, dry_run=True)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_conflict_preflight_does_not_partially_install(self):
        last = self.targets[-1]
        last.mkdir(parents=True)
        (last / 'SKILL.md').write_text('custom skill')
        with self.assertRaises(ValueError):
            install.install(self.targets)
        self.assertFalse(self.targets[0].exists())
        self.assertEqual((last / 'SKILL.md').read_text(), 'custom skill')

    def test_replace_keeps_full_backup_outside_discovery_root(self):
        dest = self.targets[0]
        dest.mkdir(parents=True)
        (dest / 'SKILL.md').write_text('old version')
        (dest / 'notes.txt').write_text('keep this')
        install.install([dest], replace=True)
        backups = list((dest.parent.parent / 'cicero-machine-backups').iterdir())
        self.assertEqual(len(backups), 1)
        self.assertEqual((backups[0] / 'notes.txt').read_text(), 'keep this')
        self.assertEqual(install.manifest(dest), install.manifest(install.SOURCE))

    def test_failed_publish_restores_old_directory(self):
        dest = self.targets[0]
        dest.mkdir(parents=True)
        (dest / 'SKILL.md').write_text('old version')
        original = Path.rename

        def fail_stage(path, target):
            if path.name.startswith('.cicero-stage-'):
                raise OSError('simulated publication failure')
            return original(path, target)

        with patch.object(Path, 'rename', fail_stage), self.assertRaises(OSError):
            install.install([dest], replace=True)
        self.assertEqual((dest / 'SKILL.md').read_text(), 'old version')

    def test_symlink_destination_is_rejected(self):
        dest = self.targets[0]
        dest.parent.mkdir(parents=True)
        try:
            dest.symlink_to(install.SOURCE, target_is_directory=True)
        except OSError:
            self.skipTest('Symlinks unavailable on this host')
        with self.assertRaises(ValueError):
            install.install([dest], replace=True)

    def test_target_inside_source_is_rejected_before_copy(self):
        source = self.root / 'source'
        source.mkdir()
        (source / 'SKILL.md').write_text('fixture')
        target = source / '.dsh/skills/cicero-machine'
        with self.assertRaises(ValueError):
            install.install([target], source=source)
        self.assertEqual(list(source.iterdir()), [source / 'SKILL.md'])


if __name__ == '__main__':
    unittest.main()
