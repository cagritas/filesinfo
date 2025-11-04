import unittest

from filesinfo import file_info_expert, get_extensions_for_platform


class FileInfoExpertTests(unittest.TestCase):
    def test_windows_extension_returns_windows_machines(self):
        self.assertEqual(file_info_expert("payload.exe"), ["windows"])

    def test_linux_extension_returns_linux_machine(self):
        self.assertEqual(file_info_expert("installer.run"), ["linux"])

    def test_multi_segment_extension_prefers_specific_match(self):
        self.assertEqual(file_info_expert("libexample.so.0"), ["linux"])

    def test_unknown_extension_defaults_to_windows(self):
        with self.assertLogs("filesinfo.core", level="WARNING") as cm:
            self.assertEqual(file_info_expert("archive.unknownext"), ["windows"])
        self.assertTrue(
            any("No file metadata was found" in message for message in cm.output)
        )

    def test_list_extensions_for_platform(self):
        extensions = get_extensions_for_platform("windows", include_cross_platform=False)
        self.assertIn(".exe", extensions)

    def test_platform_alias_support(self):
        extensions = get_extensions_for_platform("win10", include_cross_platform=False)
        self.assertIn(".exe", extensions)

    def test_cross_platform_toggle(self):
        with_cross = get_extensions_for_platform("linux", include_cross_platform=True)
        without_cross = get_extensions_for_platform("linux", include_cross_platform=False)

        self.assertIn(".pyc", with_cross)
        self.assertNotIn(".pyc", without_cross)

    def test_external_dataset_integration(self):
        platforms = file_info_expert("model.123")
        self.assertEqual(platforms, ["cross-platform"])


if __name__ == "__main__":
    unittest.main()
