import unittest
from main import Polynomial


class PolynomialTest(unittest.TestCase):
    def test_add_simple(self):
        first = Polynomial([1, 0.5, 5])
        second = Polynomial([-1, 0, 5])

        result = first + second

        self.assertAlmostEqual(result.coefficients[0], 0, 6, "first coefficient is not correct")
        self.assertAlmostEqual(result.coefficients[1], 0.5, 6, "second coefficient is not correct")
        self.assertAlmostEqual(result.coefficients[2], 10, 6, "third coefficient is not correct")

    def test_add_diff_lng_first_greater(self):
        first = Polynomial([0, 0, 1])
        second = Polynomial([-1])

        result = first + second

        self.assertAlmostEqual(result.coefficients[0], -1, 6, "first coefficient is not correct")
        self.assertAlmostEqual(result.coefficients[1], 0, 6, "second coefficient is not correct")
        self.assertAlmostEqual(result.coefficients[2], 1, 6, "third coefficient is not correct")

    def test_add_diff_lng_second_greater(self):
        first = Polynomial([0, 1])
        second = Polynomial([-1, -1, 0.1])

        result = first + second

        self.assertAlmostEqual(result.coefficients[0], -1, 6, "first coefficient is not correct")
        self.assertAlmostEqual(result.coefficients[1], 0, 6, "second coefficient is not correct")
        self.assertAlmostEqual(result.coefficients[2], 0.1, 6, "third coefficient is not correct")

    def test_multiply_simple(self):
        first = Polynomial([1, 5])
        second = Polynomial([2])

        result = first * second

        self.assertAlmostEqual(result.coefficients[0], 2, 6, "first coefficient is not correct")
        self.assertAlmostEqual(result.coefficients[1], 10, 6, "second coefficient is not correct")

    def test_multiply_zero(self):
        first = Polynomial([1, 5])
        second = Polynomial([0])

        result = first * second

        self.assertEqual(len(result.coefficients), 0, "coefficients are not empty")

    def test_multiply_binom(self):
        first = Polynomial([1, 5])
        second = Polynomial([1, 5])

        result = first * second

        self.assertAlmostEqual(result.coefficients[0], 1, 6, "first coefficient is not correct")
        self.assertAlmostEqual(result.coefficients[1], 10, 6, "second coefficient is not correct")
        self.assertAlmostEqual(result.coefficients[2], 25, 6, "third coefficient is not correct")


if __name__ == '__main__':
    unittest.main()
