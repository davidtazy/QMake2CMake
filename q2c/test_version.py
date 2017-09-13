from unittest import TestCase
from .cmake_writer import Version



class TestVersion(TestCase):
    def test_toString(self):

        version = Version("3.0.0")
        str = version.toString()
        self.assertTrue(str == "3.0.0")

