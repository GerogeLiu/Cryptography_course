# Author: GerogeLiu

import random

# Find divisors
def find_divisors(n):
    """
    Return a list of all integers that can divide n

    param: n, integer
    return: divisors, list
    """
    divisors = []
    for i in range(2, n):
        if n % i == 0:
            divisors.append(i)
    return divisors

# Get the greatest of common divisor of a and b
# Euclidean Algorithm
def gcd(a, b):
    """
    Get the greatest of common divisor of a and b
    params: a, b: integer,
    return: integer
    """
    a, b = (b, a) if a < b else (a, b)
    while b != 0:
        r = a % b
        # print(a, b, r)
        a, b = b, r
        
    return a

# determine whether an integer n is prime
def isprime(n):
    """
    Return True if n is prime, or False

    params: n, integer
    return: True or False
    """
    if n > 2 and n % 2 == 0:
        return False
    limit = int(pow(n, 0.5)) + 1
    for i in range(2, limit):
        if n % i == 0:
            return False
    return True

# extended Euclidean Algorithm
def extended_euclidean_algorithm(a, b):
    """
    Let a and b be positive integers. Then the integer(not necessarily positive)numbers x and y exist
    such that ax + by = gcd(a, b)

    params: a, b: positive integer
    return: u: tuple --> (gcd(a, b), x, y)
    """
    u = (a, 1, 0)
    v = (b, 0, 1)
    while v[0] != 0:
        q = u[0] // v[0]
        t = (u[0] % v[0], u[1] - q * v[1], u[2] - q * v[2])
        u = v
        v = t
    return u


# multiplicative inverse
def get_multiplicative_inverse(a, m):
    """
    The modulo operation on both parts of equation gives us
    ax = 1 (mod m)
    Thus, x is the modular multiplicative inverse of a modulo m
    params: a, m : integer
    return x : integer
    """
    if a == 0:
        return 0
    if a < 0:
        a %= m
    assert gcd(a, m) == 1, '%d and %d is not coprime.'% (a, m)
    _, x, y = extended_euclidean_algorithm(a, m)
    if x < 0:
        x += m
    return x


# modular inverse
# solving equation
def solve_modular_inverse_equation(a, b, p):
    """
    The equation a * x = b(mod p), solving the equation to get x
    params: a, integer
            b, integer
            p, integer, gcd(a,p) = 1
    return: x: integer, x = b * a ^ (-1) (mod p)
    a ^ (-1) mod p : get_multiplicative_inverse(a, p)
    """
    assert gcd(a, p) == 1, '%d and %d is not coprime.'% (a, p)
    a_inverse = get_multiplicative_inverse(a, p)
    x = b * a_inverse % p
    return x


# Modular Exponentiation(from right to left)
def get_modular_exponentiation_from_right(a, x, p):
    """
    params: a: integer 底数
            x: positive integer 指数
            p: integer 模数
    return: a ^ x mod p: integer
    """
    # from right to left
    x = bin(x)[2:][::-1]
    y = 1
    s = a
    for i in x:
        if i == '1':
            y = y * s % p
        s = s * s % p
    return y

# Modular Exponentiation(from left to right)
def get_modular_exponentiation_from_left(a, x, p):
    """
    params: a: integer 底数
            x: positive integer 指数
            p: integer 模数
    return: a ^ x mod p: integer
    """
    # from left to right
    x = bin(x)[2:]
    y = 1
    # print(f'x: {x}')
    for i in x:
        y = y * y % p
        if i == '1':
            y = y * a % p
    return y



# order of a modulo n
def get_order_of_modulo(a, n):
    """
    Return the smallest integer i for which
    a ^ (i + 1) mod n = a
    we call the order of a modulo n

    params: a, integer
            n, integer
    return i, integer

    >>> get_order_of_modulo(2, 31)
    5
    >>> get_order_of_modulo(3, 7)
    6
    """
    i = 1
    while i < n:
        assert a ** (i + 1) % n != 0, "No solutions!!\n Because %d ** %d %% %d == 0"%(a, i+1, n)
        if a ** (i + 1) % n == a:
            return i
        i += 1
    return 0


# integer generators 
def get_smallest_generator(p):
    """
    Return the smallest integer generator `g` such that
    ord{g, p} = p - 1
    from Euler's theorem:
    if a is coprime to n, that is, gcd(a, n) =1, then a ^(phi(n)) = 1 mod n;
    if p is prime number, the integer between 1 and p, but 1 and p, gcd(g, p) == 1

    params: p, integer, prime number
    return: g, integer
    """
    assert isprime(p), 'p is not prime number.'
    divisors = find_divisors(p - 1)
    i = 2
    while i < p:
        for d in divisors:
            if i ** d % p == 1:
                # print(f'{i} ^ {d} mod {p} == 1')
                break
        else:
            if i ** (p - 1) % p == 1:
                return i
        i += 1

def find_several_generators(p, amount=10):
    """
    Return the several integer generator `g` such that
    ord{g, p} = p - 1

    params: p, integer, prime number
            amount, integer, the amount of produce generators
    return: generators, set
    """
    assert isprime(p), 'p is not prime number.'
    generators = []
    divisors = find_divisors(p - 1)
    for i in range(2, p-1):
        for j in divisors:
            if i ** j % p == 1:
                break
        else:
            generators.append(i)
        if len(generators) == amount:
            return generators
    return generators

# get a integer's prime factor
def prime_factorization(n):
    """
    Return the integer n's prime factors

    param: n, integer
    return: factors, list
    """
    if isprime(n):
        return [1, n]
    d = 2
    factors = []
    while n > 1:
        if n % d == 0:
            factors.append(d)
            n = n // d
        else:
            d += 1 + d % 2
    return factors





