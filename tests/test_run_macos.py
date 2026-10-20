"""run.py on macOS: the Vulkan manifest handed to the loader names the driver by absolute path."""
from paths import ROOT
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(ROOT))
import run  # noqa: E402


class MacosIcdManifestTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, True)
        self.probe = self.root / 'bin' / 'spartanport-probe'
        self.probe.parent.mkdir()
        self.probe.touch()
        self.out = self.root / 'out'
        self.out.mkdir()

    def write(self, folder, library_path='libvulkan_kosmickrisp.dylib'):
        manifest = folder / 'kosmickrisp_mesa_icd.json'
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(json.dumps({'file_format_version': '1.0.0',
                                        'ICD': {'library_path': library_path,
                                                'api_version': '1.3.0'}}), encoding='utf-8')
        return manifest

    def library(self, target):
        return json.loads(target.read_text(encoding='utf-8'))['ICD']['library_path']

    def test_relative_library_path_is_resolved_beside_its_manifest(self):
        manifest = self.write(self.probe.parent / 'vulkan')
        (manifest.parent / 'libvulkan_kosmickrisp.dylib').touch()
        target = run.macos_icd_manifest(self.probe, self.out)
        self.assertEqual(Path(self.library(target)),
                         (manifest.parent / 'libvulkan_kosmickrisp.dylib').resolve())

    def test_absolute_library_path_is_kept(self):
        library = self.root / 'libvulkan_kosmickrisp.dylib'
        self.write(self.probe.parent, str(library))
        target = run.macos_icd_manifest(self.probe, self.out)
        self.assertEqual(self.library(target), str(library))

    def test_port_without_a_manifest_returns_none(self):
        self.assertIsNone(run.macos_icd_manifest(self.probe, self.out))
