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

# find one generator
def find_smallest_generator(p):
    """
    Return the smallest integer generator `g` such that
    ord{g, p} = p - 1
    from Euler's theorem:
    if p is coprime to n, that is, gcd(p, n) =1, then p ^(phi(n)) = 1 mod n;
    if p is prime number, the integer between 1 and p(but 1 and p)'s order 
    is the divisor of p - 1

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
    

