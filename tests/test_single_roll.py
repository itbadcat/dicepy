from dicepy import single_roll, KeepType, Roll

from unittest import TestCase
import random

class TestSingleRoll(TestCase):
    def setUp(self):
        random.seed(242)

    def test_highest_k(self):
        roll: Roll = single_roll.parseString('5d6k2')[0]
        self.assertEqual(roll.value, 10)
        self.assertListEqual(roll.dice, [3, 1, 4, 5, 5])
        self.assertEqual(roll.keep_type, KeepType.keep)
        self.assertEqual(roll.keep_amount, 2)

    def test_highest_kh(self):
        roll: Roll = single_roll.parseString('5d6kh2')[0]
        self.assertEqual(roll.value, 10)
        self.assertListEqual(roll.dice, [3, 1, 4, 5, 5])
        self.assertEqual(roll.keep_type, KeepType.highest)
        self.assertEqual(roll.keep_amount, 2)

    def test_keep_lowest(self):
        roll: Roll = single_roll.parseString('5d6kl2')[0]
        self.assertEqual(roll.value, 4)
        self.assertListEqual(roll.dice, [3, 1, 4, 5, 5])
        self.assertEqual(roll.keep_type, KeepType.lowest)
        self.assertEqual(roll.keep_amount, 2)
