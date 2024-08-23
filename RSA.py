import random

class RSA:
    def __init__(self, bits=512):
        self.bits = bits
        self.public_key, self.private_key = self.generate_keys()

    @staticmethod
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def miller_rabin(n, k):
        if n == 2 or n == 3:
            return True
        if n < 2 or n % 2 == 0:
            return False

        r, s = 0, n - 1
        while s % 2 == 0:
            r += 1
            s //= 2

        for _ in range(k):
            a = random.randrange(2, n - 1)
            x = pow(a, s, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    @staticmethod
    def random_odd_value(bits):
        return random.randrange(2**(bits-1) | 1, 2**bits, 2)

    def generate_prime_number(self):
        while True:
            n = self.random_odd_value(self.bits)
            if self.miller_rabin(n, 40):
                return n

    @staticmethod
    def extended_euclid_gcd(a, b):
        if b == 0:
            return a, 1, 0
        else:
            gcd, x, y = RSA.extended_euclid_gcd(b, a % b)
            return gcd, y, x - (a // b) * y

    @staticmethod
    def mod_inverse(a, m):
        gcd, x, _ = RSA.extended_euclid_gcd(a, m)
        if gcd != 1:
            raise Exception('Modular inverse does not exist')
        else:
            return x % m

    def generate_keys(self):
        p = self.generate_prime_number()
        q = self.generate_prime_number()

        while p == q:
            q = self.generate_prime_number()

        n = p * q
        phi = (p - 1) * (q - 1)

        e = 65537  # Commonly used value for e

        # Ensure e and phi are coprime
        while self.gcd(e, phi) != 1:
            e = random.randrange(3, phi, 2)

        d = self.mod_inverse(e, phi)

        public = (e, n)
        private = (d, n)

        return public, private

    def encrypt(self, plaintext):
        e, n = self.public_key
        return pow(plaintext, e, n)

    def decrypt(self, ciphertext):
        d, n = self.private_key
        return pow(ciphertext, d, n)