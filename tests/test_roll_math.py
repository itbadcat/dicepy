from dicepy import single_roll, KeepType, Roll

from unittest import TestCase
import random

class TestSingleRoll(TestCase):
    def setUp(self):
        random.seed(242)

    def test_add(self):
        #roll.dice = [3, 1, 4, 5, 5] = 4
        #roll2.dice = [4, 5, 6, 2, 1] = 11
        roll: Roll = single_roll.parseString('5d6kl2')[0]
        roll2: Roll = single_roll.parseString('5d6kh2')[0]
        self.assertEqual(roll + roll2, 15)

    def test_sub(self):
        roll: Roll = single_roll.parseString('5d6kl2')[0]
        roll2: Roll = single_roll.parseString('5d6kh2')[0]
        self.assertEqual(roll - roll2, -7)
        self.assertEqual(roll2 - roll, 7)

    def test_mul(self):
        roll: Roll = single_roll.parseString('5d6kl2')[0]
        roll2: Roll = single_roll.parseString('5d6kh2')[0]
        self.assertEqual(roll * roll2, 44)

    def test_div(self):
        roll: Roll = single_roll.parseString('5d6kl2')[0]
        roll2: Roll = single_roll.parseString('5d6kh2')[0]
        self.assertEqual(roll / roll2, 4 / 11)
        self.assertEqual(roll2 / roll, 2.75)
