import pytest
from cool_project import add_some_numbers


class TestAddSomeNumbers:
    """Test cases for the add_some_numbers function using pytest."""
    
    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        result = add_some_numbers(5, 3)
        assert result == 8
    
    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        result = add_some_numbers(-5, -3)
        assert result == -8
    
    def test_add_positive_and_negative(self):
        """Test adding a positive and negative number."""
        result = add_some_numbers(5, -3)
        assert result == 2
    
    def test_add_zero(self):
        """Test adding zero to a number."""
        result = add_some_numbers(5, 0)
        assert result == 5
        
        result = add_some_numbers(0, 5)
        assert result == 5
    
    def test_add_both_zero(self):
        """Test adding zero to zero."""
        result = add_some_numbers(0, 0)
        assert result == 0
    
    def test_add_large_numbers(self):
        """Test adding large numbers."""
        result = add_some_numbers(1000000, 2000000)
        assert result == 3000000
    
    def test_add_small_numbers(self):
        """Test adding small numbers."""
        result = add_some_numbers(1, 1)
        assert result == 2
    
    def test_add_negative_and_positive_result_zero(self):
        """Test adding numbers that result in zero."""
        result = add_some_numbers(5, -5)
        assert result == 0
    
    def test_return_type(self):
        """Test that the function returns an integer."""
        result = add_some_numbers(1, 2)
        assert isinstance(result, int)
    
    def test_commutative_property(self):
        """Test that addition is commutative (a + b = b + a)."""
        a, b = 5, 3
        result1 = add_some_numbers(a, b)
        result2 = add_some_numbers(b, a)
        assert result1 == result2


# Parametrized tests for more comprehensive coverage
@pytest.mark.parametrize("a,b,expected", [
    (1, 1, 2),
    (0, 0, 0),
    (-1, -1, -2),
    (10, -5, 5),
    (100, 200, 300),
    (-10, 10, 0),
    (0, 5, 5),
    (5, 0, 5),
])
def test_add_parametrized(a, b, expected):
    """Parametrized test for various input combinations."""
    result = add_some_numbers(a, b)
    assert result == expected


# Fixture for common test data
@pytest.fixture
def sample_numbers():
    """Fixture providing sample numbers for testing."""
    return {
        'positive': (5, 3),
        'negative': (-5, -3),
        'mixed': (5, -3),
        'zero': (0, 0),
        'large': (1000000, 2000000)
    }


def test_add_with_fixture(sample_numbers):
    """Test using fixture data."""
    pos_a, pos_b = sample_numbers['positive']
    assert add_some_numbers(pos_a, pos_b) == 8
    sample_numbers['negative'] = (-5, -4)
    neg_a, neg_b = sample_numbers['negative']
    assert add_some_numbers(neg_a, neg_b) == -9


# Test with pytest.raises for potential error cases
def test_add_with_invalid_types():
    """Test that function handles type hints correctly."""
    # This test demonstrates that the function works with integers
    # In a real scenario, you might want to test type validation
    result = add_some_numbers(1, 2)
    assert result == 6


# Mark tests for different categories
@pytest.mark.basic
def test_basic_addition():
    """Basic addition test marked for easy filtering."""
    assert add_some_numbers(2, 2) == 4


@pytest.mark.edge_case
def test_edge_case_zero():
    """Edge case test marked for easy filtering."""
    assert add_some_numbers(0, 0) == 0


@pytest.mark.performance
def test_performance_large_numbers():
    """Performance test for large numbers."""
    result = add_some_numbers(999999, 1)
    assert result == 1000000


# Test with custom markers
@pytest.mark.slow
def test_slow_operation():
    """Simulate a slow test operation."""
    # In a real scenario, this might involve more complex operations
    result = add_some_numbers(1, 1)
    assert result == 2


if __name__ == '__main__':
    # Run pytest with specific options
    pytest.main([__file__, '-v', '--tb=short'])
