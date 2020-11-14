# Author: GerogeLiu

# Elliptic curve Y^2 = X^3 + ax + b
# The discriminant of equation (X^3 + ax + b = 0) is D = (a / 3)^3 + (b / 2)^2
# Let D != 0, so the constraint 4a^3 + 27b^2 != 0
import random
import math

from util import isprime, get_multiplicative_inverse, get_modular_exponentiation_from_left

# Point P and Q in E, plot a straight line through the points. This
# line will necessarily intersect the curve at a third point--R'

# determine whether a elliptic curve equation is singular or not
def is_singular(a, b):
    """ The Elliptic curve equation Y^2 = X^2 + aX + b
        Return True if the equation is singular
        The discriminant of equation: D = (a/3)^3 + (b/2)^2
        if D == 0, the elliptic curve is singular
    """

    discriminant = 4 * pow(a, 3) + 27 * pow(b, 2)
    return discriminant == 0

# By repeated division by 2, write a = 2^s * t, where t is odd
def decompose_integer_by_two(a):
    """ By repeated division by 2, write a = 2^s * t, where t is odd
        Return the s and t in the equation
        params:
            -- a, integer
        return: s, t
    """
    t = a
    s = 0
    while t % 2 == 0:
        t //= 2
        s += 1
    return s, t


# Compute the Legendre(or namely Jacobi) symbol
def legendre_symbol(a, n):
    """
    (a/n) = {
        0, if p | a,
        1, if a mod p is a non-zero square in Z/pZ,
        -1, if x mod p is not a square in Z/pZ
    }
    params:
        -- a, integer
        -- n, integer: odd integer
    return 0, or 1, or -1
    """
    assert n % 2 != 0 and n >= 3, f"{n} is a odd interger greater than 3"
    if a == 0:
        return 0
    if a == 1:
        return 1
    # step3: Write a = 2^e * a1 compute the a1 where is odd
    e, a1 = decompose_integer_by_two(a)
    
    # step4
    if e % 2 == 0:
        s = 1
    else:
        if n % 8 == 1 or n % 8 == 7:
            s = 1
        elif n % 8 == 3 or n % 8 == 5:
            s = -1
    # step5:
    if n % 4 == 3 and a1 % 4 == 3:
        s = -s
    # step6:
    n1 = n % a1
    # step7:
    if a1 == 1:
        return s
    else:
        return s * legendre_symbol(n1, a1)

# compute equal sign of the right part of Elliptic curve equation     
def elliptic_curve_equation(a, b, p, x):
    """
    Return x^3 + ax + b (mod p)
    params:
        -- a, integer
        -- b, integer
        -- p, integer: odd prime number
        -- x, integer: horizontal coordinate
    """
    return (pow(x, 3) + a * x + b) % p

# Computing square roots
def computing_square_roots(a, b, p, x):
    """
    Handbook of Applied cryptography by Menezes -- Algorithm 3.36
    y^2 = x^3 + ax + b (mod p) let equ_right = x^3 + ax + b (mod p)
    OUTPUT: the two square roots of equ_right modulo p, provided equ_right is a quadratic residue modulo p.
    params:
        -- a, integer
        -- b, integer
        -- p, integer: an odd prime 
        -- x, integer: horizontal coordinate 
    return the square roots
    """
    assert p % 2 != 0 and isprime(p), "%d is not a odd prime number!"% p
    equ_right = elliptic_curve_equation(a, b, p, x)
    symbol = legendre_symbol(equ_right, p)
    if symbol == -1:
        print(f"{equ_right} does not have a square root modulo {p}")
        return
    # step2: get b
    b = random.randint(1, p-1)
    while legendre_symbol(b, p) != -1:
        b = random.randint(1, p-1)
    # step3: get s, t
    s, t = decompose_integer_by_two(p - 1)
    # step4: Compute a^-1 mod p
    inver_a = get_multiplicative_inverse(equ_right, p)
    # step5: 
    c = b ** t % p
    r = get_modular_exponentiation_from_left(equ_right, (t+1)//2, p)
    # step6:
    for i in range(1, s):
        d = pow((r ** 2 * inver_a), pow(2, s - i - 1)) % p
        if d % p == -1:
            r = r * c % p
            c = c ** 2 % p
    r = abs(r)
    return (r, p-r)


# Determine whether the given point on the "curve"
def is_point_on_curve(a, b, p, g):
    """
    Return True if the point g in the "curve", or False
    The Elliptic curve equation: y^2 = x^3 + ax + b
    params:
        -- a, integer
        -- b, integer
        -- p, integer: odd prime number
        -- g, tuple: the point which we want to know if that in the curve or not
    return boolean
    """
    try:
        roots = computing_square_roots(a, b, p, g[0])
        return g[1] in roots
    except Exception as e:
        print(e)

# POINT MULTIPLICATION
def point_multiplication(a, b, p, m, g):
    """ Elliptic curve equation Y^2 = X^2 + aX + b (mod m)
        Return [m]G
        params:
            -- a integer
            -- b integer
            -- p integer: modulus, prime number
            -- m integer: multiple, [m]G
            -- g tuple: start point
        return [m]G : tuple
    """
    assert not is_singular(a, b), "This Elliptic Curve(E(%d, %d)) is singular!"%(a, b)
    q = (math.inf, math.inf)
    # from left to right
    m = bin(m)[2:]
    for i in m:
        if q[0] == math.inf:
            q *= 2
        else:
            # Double
            k = (3 * pow(q[0], 2) + a) * get_multiplicative_inverse(2 * q[1], p)
            k %= p
            x = (pow(k, 2) - 2 * q[0]) % p
            y = (k * (q[0] - x) - q[1]) % p
            q = (x, y)
        if i == '1':
            # Addition
            if q[0] == math.inf:
                q = g
            else:
                kk = (q[1] - g[1]) * get_multiplicative_inverse((q[0] - g[0]), p)
                kk %= p
                xx = (pow(kk, 2) - q[0] - g[0]) % p
                yy = (kk * (g[0] - xx) - g[1]) % p
                q = (xx, yy)
    return q


# compute the point G add the point H
def add_two_point(a, b, p, g, h):
    """ Return g + h , g is the generator point, h is [m]g
    The Elliptic curve equation y^2 = x^3 + ax + b (mod p)
    params:
        -- a, integer
        -- b, integer
        -- p, integer: prime number
        -- g, tuple, the point G on E, generator point
        -- h, tuple, the point H on E, [m]g
    return a point R, tuple
    """
    assert is_point_on_curve(a, b, p, g), f"The first point {g} is not on the 'curve'"
    assert is_point_on_curve(a, b, p, h), f"The second point {h} is not on the 'curve'"
    if g == h:
        k = (3 * pow(g[0], 2) + a) * get_multiplicative_inverse(2 * g[1], p) % p
        x = (pow(k, 2) - 2 * g[0]) % p
        y = (k * (g[0] - x) - g[1]) % p
        return (x, y)
    if g[0] == h[0]:
        # point at infinity
        return None
    k = (h[1] - g[1]) * get_multiplicative_inverse((h[0] - g[0]), p) % p
    x = (pow(k, 2) - h[0] - g[0]) % p
    y = (k * (g[0] - x) - g[1]) % p
    return (x, y)
    


# compute the order of the given point on curve E
def order_of_given_point(a, b, p, g, print_detail=False):
    """
    Return the order of point g on E
    Definition: Let g be a point on E, and Let q be the smallest integer
    such that qg = O, where O is the point at infinity.
    Then we say that q is the order of the point g on E

    params:
        -- a, integer
        -- b, integer
        -- p, integer: prime number
        -- g, tuple: a point on E
        -- print_detail, bool, default False: whether return the list of all point in order
    return the numbers of order (or the list of point in this orders if print_detail is True)
"""
    points = [g]
    q = add_two_point(a, b, p, g, g)
    while q:
        points.append(q)
        q = add_two_point(a, b, p, g, q)

    # the point O (the point at infinity)
    O = (math.inf, math.inf)
    points.append(O)

    if print_detail:
        return points
    else:
        return len(points)






