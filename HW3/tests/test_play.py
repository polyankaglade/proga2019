import unittest
from unittest.mock import patch

from HW3.flash_cards.flash_cards import FlashCards

class FlashOperationsrTestCase(unittest.TestCase):
    def setUp(self):
        self.fc = FlashCards('word_set.json')

    def test_add_word(self):
        n = len(self.fc.words)
        self.assertEqual("Succesfully added word 'нож'", self.fc.add_word('нож', 'knife'))
        self.assertIn('нож', self.fc.words)
        self.assertEqual(n + 1, len(self.fc.words))

    def test_add_incorrect_1(self):
        n = len(self.fc.words)
        self.assertEqual("That's not a word", self.fc.add_word(1, ''))
        self.assertNotIn(1, self.fc.words)
        self.assertEqual(n, len(self.fc.words))

    def test_add_incorrect_2(self):
        n = len(self.fc.words)
        self.assertEqual("That's not a word", self.fc.add_word('hi', 1))
        self.assertNotIn(1, self.fc.words)
        self.assertEqual(n, len(self.fc.words))

    def test_add_existing_word(self):
        n = len(self.fc.words)
        self.assertEqual("'яблоко' already in dictionary.", self.fc.add_word('яблоко', 'new_apple'))

    def test_delete_word(self):
        n = len(self.fc.words)
        self.assertEqual("Succesfully deleted word 'хурма'", self.fc.delete_word('хурма'))
        self.assertNotIn('хурма', self.fc.words)
        self.assertEqual(n - 1, len(self.fc.words))

    def test_delete_incorrect(self):
        n = len(self.fc.words)
        self.assertEqual("That's not a word", self.fc.delete_word(1))
        self.assertEqual(n, len(self.fc.words))

    def test_delete_non_existing(self):
        n = len(self.fc.words)
        self.assertEqual("'груша' is not in dictionary", self.fc.delete_word('груша'))
        self.assertEqual(n, len(self.fc.words))

class FlashPlayTestCase(unittest.TestCase):

    def setUp(self):
        self.fc = FlashCards('word_set.json')

    def test_play_wrong_answers(self):
        with unittest.mock.patch('builtins.input', return_value="1"):
            self.assertEqual('Done! 0 out of 2 words correct', self.fc.play())

    def test_play_1_right_answer(self):
        with unittest.mock.patch('builtins.input', return_value="apple"):
            self.assertEqual('Done! 1 out of 2 words correct', self.fc.play())

    @patch('builtins.input', side_effect=['persimmon', 'apple'])
    def test_play_2_right_answers(self, mock_inputs):
        self.assertEqual('Done! 2 out of 2 words correct', self.fc.play())

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)