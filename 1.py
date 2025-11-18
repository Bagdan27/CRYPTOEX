import itertools
def decrypt_block_permutation(ciphertext, key_order):

    block_size = len(key_order)
    plaintext = []
    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i:i + block_size]
        if len(block) < block_size:
            break

        reordered_block = ''.join([block[k] for k in key_order])
        plaintext.append(reordered_block)

    return "".join(plaintext)

def solve_cipher(ciphertext):
    print(f"Шифротекст: {ciphertext}")


    target_dictionary = {
        'СРОЧНО', 'УХОДИТЕ', 'КВАРТИР', 'ИЗ',
        'ПРИВЕТ', 'ПОКА', 'РАБОТА', 'ДОМОЙ',
        'ВАЖНО', 'ОБЪЕКТ', 'ЦЕНТР'
    }

    best_score = -1
    best_text = ""
    best_key = None

    for key in itertools.permutations(range(5)):
        decrypted = decrypt_block_permutation(ciphertext, key)

        current_score = 0
        temp_text = decrypted.replace('_', '')

        for word in target_dictionary:
            if word in temp_text:
                current_score += len(word)

        if current_score > best_score:
            best_score = current_score
            best_text = decrypted
            best_key = key

    print(f"Знайдений ключ: {best_key}")
    print(f"Розшифрований текст: {best_text}")
ciphertext = "СОНРЧОУО_ХДТ_ИЕИ_ВЗКАТРРИ"
solve_cipher(ciphertext)
