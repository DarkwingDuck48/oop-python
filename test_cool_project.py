import unittest
from cool_project import add_some_numbers


class TestAddSomeNumbers(unittest.TestCase):
    """Test cases for the add_some_numbers function."""

    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        result = add_some_numbers(5, 3)
        self.assertEqual(result, 8)
        
    
    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        result = add_some_numbers(-5, -3)
        self.assertEqual(result, -8)
    
    def test_add_positive_and_negative(self):
        """Test adding a positive and negative number."""
        result = add_some_numbers(5, -3)
        self.assertEqual(result, 2)
    
    def test_add_zero(self):
        """Test adding zero to a number."""
        result = add_some_numbers(5, 0)
        self.assertEqual(result, 5)
        
        result = add_some_numbers(0, 5)
        self.assertEqual(result, 5)
    
    def test_add_both_zero(self):
        """Test adding zero to zero."""
        result = add_some_numbers(0, 0)
        self.assertEqual(result, 0)
    
    def test_add_large_numbers(self):
        """Test adding large numbers."""
        result = add_some_numbers(1000000, 2000000)
        self.assertEqual(result, 3000000)
    
    def test_add_small_numbers(self):
        """Test adding small numbers."""
        result = add_some_numbers(1, 1)
        self.assertEqual(result, 2)
    
    def test_add_negative_and_positive_result_zero(self):
        """Test adding numbers that result in zero."""
        result = add_some_numbers(5, -5)
        self.assertEqual(result, 1)
    
    def test_return_type(self):
        """Test that the function returns an integer."""
        result = add_some_numbers(1, 2)
        self.assertIsInstance(result, int)
    
    def test_commutative_property(self):
        """Test that addition is commutative (a + b = b + a)."""
        a, b = 5, 3
        result1 = add_some_numbers(a, b)
        result2 = add_some_numbers(b, a)
        self.assertEqual(result1, result2)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=3)
