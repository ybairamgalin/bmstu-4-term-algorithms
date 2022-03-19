from typing import List, Tuple

xVector = [0.00, 0.15, 0.30, 0.45, 0.60, 0.75, 0.90, 1.05]
yVector = [1.0, 0.838771, 0.655336, 0.450447, 0.225336, -0.018310, -0.278390, -0.552430]
yDerVector = [-1.0, -1.14944, -1.29552, -1.43497, -1.56464, -1.68184, -1.78333, -1.86742]

# xVector = [-0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 1.0]
# yVector = [0.707, 0.924, 1.0, 0.924, 0.707, 0.383, 0]
# yDerVector = [0.0] * 7


class Node:
    def __init__(self, x=None, y=None, derivative=None):
        self.x = x
        self.y = y
        self.derivative = derivative

    def __str__(self):
        return f"Node x = {self.x:.4f}\ty = {self.y:.4f}\ty' = {self.derivative:.4f}"


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
            return "Empty"

        for i in range(len(self.coefficients) - 1):
            result += f"({round(self.coefficients[len(self.coefficients) - 1 - i], 3)}) * x ^ " \
                      f"{len(self.coefficients) - 1 - i} + "

        result += f"({round(self.coefficients[0], 3)})"

        return result

    def y(self, x: float):
        """Returns value of polynomial function at x"""
        if len(self.coefficients) == 0:
            raise

        result = 0

        for index, coefficient in enumerate(self.coefficients):
            result += coefficient * pow(x, index)

        return result


class Function:
    def __init__(self, nodes: List[Node]):
        self.values = nodes

    def closest_node(self, x: float) -> int:
        """Returns index of node closest to x"""
        first_bigger = None

        for index, value in enumerate(self.values):
            if value.x > x:
                first_bigger = index
                break

        if first_bigger is None:
            return len(self.values) - 1

        if first_bigger == 0:
            return 0

        if abs(self.values[first_bigger - 1].x - x) < abs(self.values[first_bigger].x - x):
            return first_bigger - 1

        return first_bigger

    def closest_nodes(self, x: float, number: int) -> Tuple[int, int]:
        """Returns first and last index of 'number' of nodes closest to x"""
        if number <= 0:
            raise

        if number > len(self.values):
            raise

        if len(self.values) == 0:
            raise

        closest_node = self.closest_node(x)

        left = closest_node
        right = closest_node

        while right - left + 1 < number:
            if left == 0:
                right += 1
                continue

            if right == len(self.values) - 1:
                left -= 1
                continue

            if abs(self.values[left - 1].x - x) < abs(self.values[right + 1].x - x):
                left -= 1
            else:
                right += 1

        return left, right

    def separated_differences(self, indexes: Tuple[int, int]):
        if indexes[0] == indexes[1]:
            return self.values[indexes[0]].y

        return (self.separated_differences((indexes[0], indexes[1] - 1)) -
                self.separated_differences((indexes[0] + 1, indexes[1]))) / \
               (self.values[indexes[0]].x - self.values[indexes[1]].x)

    def separated_differences_hermite(self, table, indexes: Tuple[int, int]):
        if indexes[0] == indexes[1] and len(indexes) == 2:
            return table[indexes[0]].y

        if abs(table[indexes[0]].x - table[indexes[1]].x) < 1e-6:
            return table[indexes[0]].derivative

        return (self.separated_differences_hermite(table, (indexes[0], indexes[1] - 1)) -
                self.separated_differences_hermite(table, (indexes[0] + 1, indexes[1]))) / \
               (table[indexes[0]].x - table[indexes[1]].x)

    def differences_list(self, indexes: Tuple[int, int], power: int) -> List[float]:
        result = []

        for i in range(power + 1):
            result.append(self.separated_differences((indexes[0], indexes[0] + i)))

        return result

    def differences_list_hermite(self, indexes: Tuple[int, int], nodes: int):
        result = []
        table = []

        for node in self.values[indexes[0]:(indexes[1] + 1)]:
            table.append(node)
            table.append(node)

        for i in range(nodes * 2):
            result.append(self.separated_differences_hermite(table, (0, i)))

        return result

    def newton_polynomial(self, x: float, power: int) -> Polynomial:
        """Returns polynomial that approximates the given nodes"""
        start_end_nodes = self.closest_nodes(x, power + 1)
        diff_list = self.differences_list(start_end_nodes, power)
        result = Polynomial([])

        for i in range(len(diff_list)):
            new_term = Polynomial([diff_list[i]])

            for j in range(i):
                new_term *= Polynomial([-self.values[start_end_nodes[0] + j].x, 1])

            result += new_term

        print(result)

        return result

    def hermite_polynomial(self, x: float, nodes_to_use: int) -> Polynomial:
        start_end_nodes = self.closest_nodes(x, nodes_to_use)
        diff_list = self.differences_list_hermite(start_end_nodes, nodes_to_use)

        result = Polynomial([])

        for i in range(len(diff_list)):
            new_term = Polynomial([diff_list[i]])

            for j in range(i):
                new_term *= Polynomial([-self.values[start_end_nodes[0] + j // 2].x, 1])

            result += new_term

        print(result)

        return result


def main():
    nodes = []

    for x, y, der in zip(xVector, yVector, yDerVector):
        nodes.append(Node(x, y, der))

    to_approximate = Function(nodes)
    newton = to_approximate.newton_polynomial(0.6, 4)
    hermit = to_approximate.hermite_polynomial(0.6, 3)

    print(f"RESULT: {newton.y(0.6)}")
    print(f"RESULT: {hermit.y(0.6)}")


if __name__ == '__main__':
    main()
