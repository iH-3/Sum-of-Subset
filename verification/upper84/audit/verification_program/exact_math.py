"""Small auditable exact-polynomial and rational-certificate kernel.
No eval(), floating point, external libraries, network, or solver is used.
"""
import ast
from fractions import Fraction


class VerificationError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


class Poly:
    """Sparse polynomial, monomials represented by sorted tuples of variables."""
    def __init__(self, terms=None):
        self.terms = {tuple(k): Fraction(v) for k, v in (terms or {}).items() if v}

    @classmethod
    def constant(cls, value):
        return cls({(): value})

    @classmethod
    def variable(cls, name):
        return cls({(name,): 1})

    def __add__(self, other):
        other = other if isinstance(other, Poly) else Poly.constant(other)
        out = dict(self.terms)
        for key, value in other.terms.items():
            out[key] = out.get(key, Fraction(0)) + value
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({key: -value for key, value in self.terms.items()})

    def __sub__(self, other):
        return self + (-other if isinstance(other, Poly) else -Fraction(other))

    def __mul__(self, other):
        other = other if isinstance(other, Poly) else Poly.constant(other)
        out = {}
        for k1, v1 in self.terms.items():
            for k2, v2 in other.terms.items():
                key = tuple(sorted(k1 + k2))
                out[key] = out.get(key, Fraction(0)) + v1 * v2
        return Poly(out)

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, Poly):
            require(set(other.terms) <= {()}, 'Only division by constants is permitted')
            other = other.terms.get((), 0)
        require(other != 0, 'Division by zero')
        return self * (Fraction(1) / other)

    def __pow__(self, exponent):
        require(isinstance(exponent, int) and 0 <= exponent <= 8, 'Unsupported exponent')
        out = Poly.constant(1)
        for _ in range(exponent):
            out = out * self
        return out

    def evaluate(self, values):
        result = Fraction(0)
        for monomial, coefficient in self.terms.items():
            for symbol in monomial:
                require(symbol in values, 'Missing variable: ' + symbol)
                coefficient *= Fraction(values[symbol])
            result += coefficient
        return result

    def univariate(self, symbol='r'):
        require(all(set(key) <= {symbol} for key in self.terms), 'Not univariate')
        degree = max((len(key) for key in self.terms), default=0)
        return [self.terms.get((symbol,) * i, Fraction(0)) for i in range(degree + 1)]


def parse(expression):
    """Parse a restricted arithmetic expression, never arbitrary Python code."""
    def visit(node):
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return Poly.constant(node.value)
        if isinstance(node, ast.Name):
            return Poly.variable(node.id)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -visit(node.operand)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.UAdd):
            return visit(node.operand)
        if isinstance(node, ast.BinOp):
            a, b = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Add):
                return a + b
            if isinstance(node.op, ast.Sub):
                return a - b
            if isinstance(node.op, ast.Mult):
                return a * b
            if isinstance(node.op, ast.Div):
                return a / b
            if isinstance(node.op, ast.Pow):
                require(set(b.terms) <= {()}, 'Nonconstant exponent')
                exponent = b.terms.get((), 0)
                require(exponent.denominator == 1, 'Noninteger exponent')
                return a ** int(exponent)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            require(len(node.args) == 1 and not node.keywords, 'Invalid function call')
            p = visit(node.args[0])
            if node.func.id == 'T':
                return p * (p + 1) / 2
            if node.func.id == 'I':
                return (p - 34) * (p - 35)
        raise VerificationError('Unsupported syntax: ' + ast.dump(node))
    return visit(ast.parse(expression, mode='eval').body)


def equal(left, right):
    require(parse(left).terms == parse(right).terms, 'Polynomial identity failed: ' + left + ' = ' + right)


def quadratic_integer_min(poly, symbol='r'):
    """Global integer minimum using the exact rational vertex and its neighbors."""
    coeffs = poly.univariate(symbol)
    require(len(coeffs) == 3 and coeffs[2] > 0, 'Expected convex quadratic')
    vertex = -coeffs[1] / (2 * coeffs[2])
    floor = vertex.numerator // vertex.denominator
    candidates = [floor, floor + 1]
    values = [(poly.evaluate({symbol: r}), r) for r in candidates]
    minimum = min(value for value, _ in values)
    return minimum, [r for value, r in values if value == minimum]


def verify_linear_certificate(certificate):
    """Check nonnegative rational combination of Ax<=b gives 0<=negative."""
    variables = certificate['variables']
    rows = certificate['rows']
    multipliers = [Fraction(w) for w in certificate['multipliers']]
    require(len(rows) == len(multipliers), 'Certificate row/multiplier count mismatch')
    require(len(set(variables)) == len(variables), 'Duplicate variables')
    total = {variable: Fraction(0) for variable in variables}
    rhs = Fraction(0)
    for row, multiplier in zip(rows, multipliers):
        require(multiplier >= 0, 'Certificate has negative multiplier')
        require(set(row['coefficients']) <= set(variables), 'Unknown certificate variable')
        for variable, coefficient in row['coefficients'].items():
            total[variable] += multiplier * Fraction(coefficient)
        rhs += multiplier * Fraction(row['rhs'])
    require(all(value == 0 for value in total.values()), 'Certificate does not cancel coefficients: ' + str(total))
    require(rhs < 0, 'Certificate does not yield a strict contradiction')
    require(rhs == Fraction(certificate['expected_rhs']), 'Certificate contradiction differs from expected')
    return {'rhs': str(rhs), 'rows': len(rows), 'variables': len(variables)}
