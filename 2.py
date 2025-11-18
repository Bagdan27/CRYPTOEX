import numpy as np

alphabet = "АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
n = len(alphabet)  # 31

print(f"Розмір алфавіту: {n}")
print(f"Алфавіт: {alphabet}\n")

def text_to_numbers(text, alphabet):
    return [alphabet.index(char) for char in text]

def numbers_to_text(numbers, alphabet):
    return ''.join([alphabet[num % len(alphabet)] for num in numbers])

# розширений алгоритм Евкліда
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

# знаходження оберненого елемента за модулем
def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a % m, m)
    if gcd != 1:
        raise ValueError(f"Обернений елемент не існує для {a} mod {m}")
    return (x % m + m) % m

# обчислення визначника матриці за модулем
def matrix_det_mod(matrix, mod):
    det = int(np.round(np.linalg.det(matrix)))
    return det % mod

#обчислення оберненої матриці за модулем
def matrix_inverse_mod(matrix, mod):
    det = matrix_det_mod(matrix, mod)
    det_inv = mod_inverse(det, mod)

    # для матриці 2x2
    if matrix.shape == (2, 2):
        adj_matrix = np.array([[matrix[1, 1], -matrix[0, 1]],
                               [-matrix[1, 0], matrix[0, 0]]])
    else:
        raise ValueError("Реалізовано для матриць 2x2")

    inv_matrix = (det_inv * adj_matrix) % mod
    return inv_matrix.astype(int)

#вихідні дані
plaintext = "МУХА"
ciphertext = "РГЛЗ"

print(f"Відкритий текст: {plaintext}")
print(f"Шифротекст: {ciphertext}\n")

#перетворення в числа
plain_nums = text_to_numbers(plaintext, alphabet)
cipher_nums = text_to_numbers(ciphertext, alphabet)

print(f"Відкритий текст (числа): {plain_nums}")
print(f"Шифротекст (числа): {cipher_nums}\n")

#формування матриць 2 на 2
X = np.array([[plain_nums[0], plain_nums[2]],
              [plain_nums[1], plain_nums[3]]])

Y = np.array([[cipher_nums[0], cipher_nums[2]],
              [cipher_nums[1], cipher_nums[3]]])

print("Матриця відкритого тексту X:")
print(X)
print("\nМатриця шифротексту Y:")
print(Y)

print(" Знаходження X^(-1) mod 31")

det_X = matrix_det_mod(X, n)
print(f"det(X) mod {n} = {det_X}")

det_X_inv = mod_inverse(det_X, n)
print(f"det(X)^(-1) mod {n} = {det_X_inv}")

X_inv = matrix_inverse_mod(X, n)
print(f"\nX^(-1) mod {n}:")
print(X_inv)

X_check = (X @ X_inv) % n
print(f"\nПеревірка: X * X^(-1) mod {n}:")
print(X_check)

print("Знаходження матриці шифрування H1")

H1 = (Y @ X_inv) % n
print(f"H1 = Y * X^(-1) mod {n}:")
print(H1)

#перетворення матриці H1 в ключове слово
key_numbers = [H1[0, 0], H1[0, 1], H1[1, 0], H1[1, 1]]
key_word = numbers_to_text(key_numbers, alphabet)
print(f"\nКлючове слово (читається по рядках): {key_word}")
print(f"Числове представлення ключа: {key_numbers}")

print("Знаходження матриці розшифрування H2")

det_H1 = matrix_det_mod(H1, n)
print(f"det(H1) mod {n} = {det_H1}")

det_H1_inv = mod_inverse(det_H1, n)
print(f"det(H1)^(-1) mod {n} = {det_H1_inv}")

H2 = matrix_inverse_mod(H1, n)
print(f"\nH2 = H1^(-1) mod {n}:")
print(H2)

print("Перевірка умови H1 * H2 ≡ I (mod 31)")

identity_check = (H1 @ H2) % n
print(f"H1 * H2 mod {n}:")
print(identity_check)

is_identity = np.array_equal(identity_check, np.eye(2, dtype=int))
print(f"\nЧи є результат одиничною матрицею? {'так' if is_identity else 'НІ ✗'}")

# шифрування відкритого тексту
encrypted = (H1 @ X) % n
encrypted_text = numbers_to_text([encrypted[0, 0], encrypted[1, 0],
                                  encrypted[0, 1], encrypted[1, 1]], alphabet)
print(f"Оригінальний відкритий текст: {plaintext}")
print(f"шифрований текст: {encrypted_text}")
print(f"Очікуваний шифротекст: {ciphertext}")
print(f"Шифрування працює правильно? {'так' if encrypted_text == ciphertext else 'НІ ✗'}")
print(" Перевірка розшифрування")
decrypted = (H2 @ Y) % n
decrypted_text = numbers_to_text([decrypted[0, 0], decrypted[1, 0],
                                  decrypted[0, 1], decrypted[1, 1]], alphabet)
print(f"Шифротекст {ciphertext}")
print(f"Розшифрований текст {decrypted_text}")
print(f"Очікуваний відкритий текст {plaintext}")
print(f"Розшифрування працює правильно? {'так' if decrypted_text == plaintext else 'НІ ✗'}")
print(f"Ключ слово: {key_word}")
