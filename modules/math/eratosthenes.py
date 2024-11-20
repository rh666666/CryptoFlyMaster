# Eratosthenes筛法求200以内素数

def sieve_of_eratosthenes(n):
    primes = [True for i in range(n+1)]
    p = 2
    while (p * p <= n):
        if (primes[p] == True):
            for i in range(p * p, n+1, p):
                primes[i] = False
                p += 1
    prime_numbers = [p for p in range(2, n) if primes[p]]
    return prime_numbers

def main():
    primes = sieve_of_eratosthenes(200)
    print('200以内的素数：', primes)
    input("\n[Press Enter to continue...]")

if __name__ == '__main__':
    main()