"""Sample tests"""

from django.test import SimpleTestCase # type: ignore

from app import calc

class CalcTests(SimpleTestCase):
    """Test the calc module"""
    def test_add_numbers(self):
        """Test adding number together."""
        res=calc.add(5,6)
        self.assertEqual(res,12)