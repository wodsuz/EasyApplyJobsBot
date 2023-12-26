import unittest

from linkedin import Linkedin as JobProcessor
from models import Job


class test_answered_question_which_does_not_exist_on_backend(unittest.TestCase):
    pass


class test_answered_question_which_exist_on_backend(unittest.TestCase):
    pass


class test_unanswered_question_which_does_not_exist_on_backend(unittest.TestCase):
    pass


class test_unanswered_question_which_exists_on_backend(unittest.TestCase):
    pass


class test_handling_single_line_text_input_answer(unittest.TestCase):
    pass


class test_handling_multi_line_text_input_answer(unittest.TestCase):
    pass


class test_handling_single_choice_answer(unittest.TestCase):
    pass


class test_handling_dropdown_answer(unittest.TestCase):
    pass


class test_handling_write_to_dropdown_answer(unittest.TestCase):
    pass