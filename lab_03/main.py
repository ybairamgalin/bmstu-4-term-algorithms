import matplotlib.pyplot as plot
import numpy as np

from typing import List, Tuple

x_values = [i for i in range(11)]

y_values = [0, 0.496, 0.986, 1.102, 0.972, 0.754, 0.539,
          0.364, 0.236, 0.148, 0.091]


class Polynomial:
    def __init__(self, coefficients: List[float]):
        """Coefficients - [a, b, c, d, ...] for a + bx + cx^2 + dx^3 + ..."""
        self.coefficients = coefficients

    def __add__(self, other):
        if len(self.coefficients) >= len(other.coefficients):
            new_coefficients = self.coefficients

            for i in range(len(other.coefficients)):
                new_coefficients[i] += other.coefficients[i]
        else:
            new_coefficients = other.coefficients

            for i in range(len(self.coefficients)):
                new_coefficients[i] += self.coefficients[i]

        return Polynomial(new_coefficients)

    def __mul__(self, other):
        newPolynomial = Polynomial([0] * (len(self.coefficients) + len(other.coefficients)))

        for i in range(len(self.coefficients)):
            for j in range(len(other.coefficients)):
                newPolynomial.coefficients[i + j] += self.coefficients[i] * other.coefficients[j]

        while len(newPolynomial.coefficients) != 0 and\
                newPolynomial.coefficients[len(newPolynomial.coefficients) - 1] == 0:
            newPolynomial.coefficients.pop()

        return newPolynomial

    def __str__(self):
        result = ""

        if len(self.coefficients) == 0:
            return "Empty polynomial"

        for i in range(len(self.coefficients) - 1):
            result += f"({round(self.coefficients[len(self.coefficients) - 1 - i], 3)})x ^ " \
                      f"{len(self.coefficients) - 1 - i} + "

        result += f"({round(self.coefficients[0], 3)})"

        return result

    def __len__(self):
        return len(self.coefficients)

    def y(self, x: float):
        """Returns value of polynomial function at x"""
        if len(self.coefficients) == 0:
            raise

        result = 0

        for index, coefficient in enumerate(self.coefficients):
            result += coefficient * pow(x, index)

        return result


class Spline:
    def __init__(self, x_vals: List[float], y_vals: List[float]):
        self.polynomials = self.__interpolate(x_vals, y_vals)

    def y(self):
        pass

    def plot(self, drawer, step=1, pointsByPoly=100):
        pass

    @staticmethod
    def __interpolate(x_vals: List[float], y_vals: List[float]):
        lng = len(x_vals)

        xi_coefs = [0 for i in range(lng + 1)]
        nu_coefs = [0 for i in range(lng + 1)]

        for i in range(2, len(x_vals)):
            currH = x_vals[i] - x_vals[i - 1]
            prevH = x_vals[i - 1] - x_vals[i - 2]

            f = 3 * ((y_vals[i] - y_vals[i - 1]) / currH -
                     (y_vals[i - 1] - y_vals[i - 2]) / prevH)

            newXi = -(currH / (prevH * xi_coefs[i] + 2 * (prevH + currH)))
            newNu = (f - prevH * nu_coefs[i]) / (prevH * xi_coefs[i] +
                                                 2 * (prevH + currH))

            xi_coefs[i + 1] = newXi
            nu_coefs[i + 1] = newNu

        c_coefs = [0 for i in range(lng + 1)]

        for i in range(lng - 2, - 1, -1):
            c_coefs[i] = xi_coefs[i + 1] * c_coefs[i + 1] + nu_coefs[i + 1]

        a_coefs = [0]
        b_coefs = [0]
        d_coefs = [0]

        for i in range(1, len(x_vals)):
            currH = x_vals[i] - x_vals[i - 1]

            a_coefs.append(y_vals[i - 1])
            b_coefs.append((y_vals[i] - y_vals[i - 1]) / currH -
                           currH / 3 * (c_coefs[i + 1] + 2 * c_coefs[i]))
            d_coefs.append((c_coefs[i + 1] - c_coefs[i]) / (3 * currH))

        a_coefs.pop(0)
        b_coefs.pop(0)
        c_coefs.pop(0)
        d_coefs.pop(0)

        spline = []

        for index, (a, b, c, d) in enumerate(
                zip(a_coefs, b_coefs, c_coefs, d_coefs)):
            h = 1
            polyH = Polynomial([-x_vals[index], 1])

            poly = Polynomial([a]) + \
                   Polynomial([b]) * polyH + \
                   Polynomial([c]) * polyH * polyH + \
                   Polynomial([d]) * polyH * polyH * polyH

            spline.append(poly)

        return spline


if __name__ == '__main__':
    x = np.array(x_values)
    y = np.array(y_values)
    plot.plot(x, y)

    spline = Spline(x_values, y_values)
    pointsByPoly = 100
    step = 1.0 / pointsByPoly

    newX = []
    newY = []

    for index, poly in enumerate(spline.polynomials):
        for i in range(pointsByPoly):
            x = x_values[index] + i * step
            y = poly.y(x_values[index] + i * step)
            newX.append(x)
            newY.append(y)

    x_numpy = np.array(newX)
    y_numpy = np.array(newY)
    plot.plot(x_numpy, y_numpy)

    plot.show()
