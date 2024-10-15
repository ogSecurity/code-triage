import unittest

from output.vars import OUTPUT_HEADERS_DEFAULTS


class TestOutputHeadersDefaults(unittest.TestCase):
    def test_keys_are_dicts(self):
        for key, value in OUTPUT_HEADERS_DEFAULTS.items():
            self.assertIsInstance(value, dict, f"The value for key '{key}' is not a dictionary")

    def test_required_keys(self):
        required_keys = {'default', 'type', 'label'}
        for key, value in OUTPUT_HEADERS_DEFAULTS.items():
            self.assertTrue(required_keys.issubset(value.keys()),
                            f"The dictionary for key '{key}' is missing required keys")

    def test_type_key(self):
        valid_types = {bool, str, int}
        for key, value in OUTPUT_HEADERS_DEFAULTS.items():
            self.assertIn(value['type'], valid_types, f"The 'type' for key '{key}' is not one of {valid_types}")

    def test_label_is_string_and_not_blank(self):
        for key, value in OUTPUT_HEADERS_DEFAULTS.items():
            self.assertIsInstance(value['label'], str, f"The 'label' for key '{key}' is not a string")
            self.assertTrue(value['label'], f"The 'label' for key '{key}' is blank")

    def test_default_value_matches_type(self):
        for key, value in OUTPUT_HEADERS_DEFAULTS.items():
            self.assertIsInstance(value['default'], value['type'],
              f"The 'default' value for key '{key}' does not match the specified type")

    def test_key_name_is_lowecase_with_underscores(self):
        for key in OUTPUT_HEADERS_DEFAULTS.keys():
            self.assertTrue(key.islower(), f"Key '{key}' is not all lowercase")
            self.assertTrue(all([c.isalnum() or c == '_' for c in key]), f"Key '{key}' contains invalid characters")
            self.assertTrue(key[0].isalpha(), f"Key '{key}' does not start with a letter")