def compare_bits_in_file(file_path, line_num1, line_num2):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

            if line_num1 < 1 or line_num2 < 1 or line_num1 > len(lines) or line_num2 > len(lines):
                return "Номер строки вне допустимого диапазона"

            str1 = lines[line_num1 - 1].strip()
            str2 = lines[line_num2 - 1].strip()

            bits1 = ''.join(format(ord(char), '08b') for char in str1)
            bits2 = ''.join(format(ord(char), '08b') for char in str2)

            if len(bits1) != len(bits2):
                return "Строки имеют разную длину в битах"

            match_count = 0
            mismatch_count = 0
            for bit1, bit2 in zip(bits1, bits2):
                if bit1 == bit2:
                    match_count += 1
                else:
                    mismatch_count += 1

            return f"Совпадает: {match_count} битов, Не совпадает: {mismatch_count} битов"
    except FileNotFoundError:
        return "Файл не найден"

file_path = 'hash.txt'
for i in range(1, 9):
    print(compare_bits_in_file(file_path, i, 8 + i))
