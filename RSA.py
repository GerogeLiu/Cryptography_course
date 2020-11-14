from util import isprime, get_multiplicative_inverse

# RSA cryptosystem
# RSA ALGORITHM
"""
RSA ALGORITHM
<Key generation>
1. Generate two large prime numbers, p and q;
2. Let n = p*q
3. Let phi(n) = (p-1)*(q-1)
4. Choose a small number e, coprime to phi(n)
5. Find d, such that d * e = 1 (mod phi(n))
6. Publish e and n as the public key
7. Keep d, p, q secret. d and n constitute the private key.
<Encryption>
c = m ^ e mod n 
<Decryption>
m = c ^ d mod n
"""
class RSA:
    """
    Implement RSA algorithm above
    """
    def __init__(self, p, q):
        self.public_key = None
        self.__p = p
        self.__q = q
        self.__n = p * q
        self.__phi = (p - 1) * (q - 1) # the sum of numbers relatively prime to n
    
    def generate_candidates(self, amount=10):
        """
        e * d = 1 (mod phi)
        Return the candidates of e * d
        
        params: amount, integer: the amount of candidates
        return candidates, list
        """
        candidates = []
        for i in range(1, amount+1):
            num = i * self.__phi + 1
            # Determine whether it can be factored
            if not isprime(num):
                candidates.append(num)
        return candidates

    def set_e(self, e):
        assert gcd(e, self.__phi) == 1, '%d and %d is not coprime.'%(e, self.phi)
        self.__e = e
        self.__d = get_multiplicative_inverse(self.__e, self.__phi)
        self.public_key = (self.__n, self.__e)

    def encrypt(self, msg):
        """
        Return ciphertext such that msg ^ e mod n

        params: msg, integer
        return: ciphertext, integer
        """
        ciphertext = msg ** self.__e % self.__n
        return ciphertext

    def decrypt(self, ciphertext):
        """
        Return plaintext

        params: ciphertext, integer
        return: msg, integer
        """
        msg = ciphertext ** self.__d % self.__n
        return msg

    def get_public_key(self):
        return self.__n, self.__e

class RSA_Digital_Signature:
    """
    SENDER A: public key:{m, e}, private key:d
    RECEIVER B: public key: {n, h}; private key: g
    """
    def __init__(self, sender, receiver):
        """
        params:
                sender: tuple, {p, q, e} create a new RSA object
                receiver: tuple, {r, s, h} 
        """
        self.sender = RSA(sender[:2])
        self.receiver = RSA(receiver[:2])
        self.sender.set_e(sender[-1])
        self.receiver.set_e(receiver[-1])
        self.sender_public_key = self.sender.public_key
        self.receiver_public_key = self.receiver.public_key

    def sender_encrypt(self, msg):
        n, h = self.receiver_public_key
        sign = self.sender.encrypt(msg)
        ciphertext = sign ** h % n
        return ciphertext

    def receiver_decrypt(self, ciphertext):
        m, e = self.sender_public_key
        z = self.receiver.decrypt(ciphertext)
        plaintext = z ** e % m
        return plaintext

