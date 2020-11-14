import random

from util import gcd, get_multiplicative_inverse

# EIGamal Encryption
"""
A --> B
p, g 
A private key CA, public key dA = g ^ CA mod p
B private key CB, public key dB = g ^ CB mod p
A select random key k, and have a message m which want to send to B
get r = g ^ k mod p
get e = m * dB ^ k mod p
sent (r, e) to B

B get message m which A send through some calculations as below
m = e * r ^ (p - 1 - CB) mod p
"""

def to_EIGamal_Encryption(p, g, m, dB, secret_key=None):
    """
    A sent a message m to B
    params: p , a large prime number;
            g , integer
            m , integer m < p
            dB, the public key of B
            secret_key - default None, random a integer [1, p -2]
    return (C, H)
    """
    # generate a random number
    k = random.randint(1, p - 2) if secret_key == None else secret_key
    M = dB ** k % p # mask
    while M == 1:
        if secret_key != None:
            print('Secret Key IS BAD CHOICE!, PLEASE CHOOSE AGAIN!')
            return
        elif secret_key == None:
            k = random.randint(1, p - 2)
        M = dB ** k % p
    C = m * M % p # ciphertext
    H = g ** k % p  # hint
    return (C, H)

def to_EIGamal_decryption(from_A, p, CB):
    """
    B decrypt through (C,H) which get from A and private key CB
    params: from_A, tuple: from the sender
            p, the large prime number;
            CB, integer: the private key of B (receiver)
    return: m, integer(the message what A want to send to B)
    """
    C, H = from_A
    q = p - 1 - CB
    R = (H ** q) % p # opener
    m = C * R % p
    return m

# EIGamal Digital Signature as sender 
def to_EIGamal_DigitalSignature_as_sender(p, g, r, R, M):
    """
    Return the signature of M

    params: p, integer, prime number
            g, integer
            r, integer, random number [1, p-1]
            R, integer, random number [1, p-2]
            m, integer, the message that sender want to send
    return (M, X, Y) , (X, Y) is the signature such that
            compute X = g ^ R mod p
            find Y such that M = r * X + R * Y mod (p-1)
            Y = (M - r * X) * R^-1 mod (p - 1)
    """
    assert gcd(R, p-1) == 1, '{%d , %d} is not coprime.'%(R, p-1)
    X = g ** R % p
    R_inv = get_multiplicative_inverse(R, p-1)
    Y = (M - r * X) * R_inv % (p - 1)
    return M, X, Y


# EIGamal Digital Signature as receiver
def is_message_from_A_EIGamal_DigitalSignature_as_receiver(from_A, p, g, K):
    """
    Return True if The message is from A, or return False

    param:  
            from_A, tuple: received information
            p, integer: prime number
            g, integer
            K, integer:  A's random number r compute g ^ r mod p 
    return True or False
    """
    M, X, Y = from_A
    A = (K ** X) * (X ** Y) % p
    return A == g ** M % p
