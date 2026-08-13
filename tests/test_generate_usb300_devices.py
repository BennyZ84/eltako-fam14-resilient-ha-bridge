import csv
import io
import unittest
from tools.generate_usb300_devices import generate, parse_base


class GeneratorTests(unittest.TestCase):
    def test_switch_and_cover(self):
        rows = list(csv.DictReader(io.StringIO(
            "kind,name,sender_suffix,cover_prefix\n"
            "switch,hall,81,\n"
            "cover,office,A1,00:F5\n"
        )))
        text = generate(rows, parse_base("FF:AA:BB:80"))
        self.assertIn("sender = 0xFFAABB81", text)
        self.assertIn("func = 0x38", text)
        self.assertIn("sender = 0xFFAABBA1", text)
        self.assertIn("# move_prefix = 00:F5", text)
        self.assertNotIn("raw_data =", text)

    def test_reject_duplicate_sender(self):
        rows = list(csv.DictReader(io.StringIO(
            "kind,name,sender_suffix,cover_prefix\n"
            "switch,a,81,\n"
            "switch,b,81,\n"
        )))
        with self.assertRaises(ValueError):
            generate(rows, parse_base("FF:AA:BB:80"))


if __name__ == '__main__':
    unittest.main()
