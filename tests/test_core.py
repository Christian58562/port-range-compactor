"""Tests for the port range compactor core module."""

import unittest

from port_range_compactor import compact


class TestCompact(unittest.TestCase):
    def test_empty_input_returns_empty_string(self):
        self.assertEqual(compact([]), "")

    def test_single_port_returns_itself(self):
        self.assertEqual(compact([8080]), "8080")

    def test_two_consecutive_ports_are_not_collapsed(self):
        self.assertEqual(compact([8000, 8001]), "8000,8001")

    def test_three_consecutive_ports_are_collapsed(self):
        self.assertEqual(compact([8000, 8001, 8002]), "8000-8002")

    def test_mixed_ranges_and_individual_ports(self):
        self.assertEqual(
            compact([1, 2, 3, 5, 6, 8, 10, 11, 12, 15]),
            "1-3,5,6,8,10-12,15",
        )

    def test_duplicate_ports_are_ignored(self):
        self.assertEqual(compact([80, 80, 443, 443, 443]), "80,443")

    def test_unsorted_input_is_sorted_in_output(self):
        self.assertEqual(compact([443, 80, 81, 82]), "80-82,443")

    def test_large_range_at_upper_boundary(self):
        self.assertEqual(compact([65533, 65534, 65535]), "65533-65535")

    def test_lower_boundary_is_respected(self):
        self.assertEqual(compact([1, 2, 3]), "1-3")

    def test_zero_is_rejected(self):
        with self.assertRaises(ValueError):
            compact([0])

    def test_port_above_65535_is_rejected(self):
        with self.assertRaises(ValueError):
            compact([65536])

    def test_negative_port_is_rejected(self):
        with self.assertRaises(ValueError):
            compact([-1])

    def test_non_integer_is_rejected(self):
        with self.assertRaises(ValueError):
            compact(["80"])  # type: ignore[list-item]

    def test_all_ports_are_collapsed_into_one_range(self):
        self.assertEqual(compact(range(1, 65536)), "1-65535")

    def test_generator_input_is_supported(self):
        self.assertEqual(compact(iter([22, 23, 24])), "22-24")

    def test_tuple_input_is_supported(self):
        self.assertEqual(compact((22, 23, 24, 25)), "22-25")


if __name__ == "__main__":
    unittest.main()
