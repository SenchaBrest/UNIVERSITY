import CIK
import random
from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA1


#просто обьявление всех глобальных переменных
voters_info_list, voter_with_id_blind_and_sign = {}, {}
#просто обьявление всех глобальных переменных

#бюллитень с кандидатами
bulliten = ["Candidate A", "Candidate B", "Candidate C"]

generated_marks = set()  #для отследивания меток M(мало ли одинковые сгенерятся)
#генерирование меток M
def generate_unique_mark():
    generated = False
    while generated == False:
        random_mark = random.randint(10**9, 10**10 - 1)
        if random_mark not in generated_marks:
            generated_marks.add(random_mark)
            generated = True

    return random_mark


generated_multi = set() #то же что и сет выше, но для множителя
#генерирование уникальных закрытых множителей
def generate_unique_closed_miltiplier():
    generated = False
    while generated == False:
        random_multi = random.randint(10**4, 10**5 - 1)
        if random_multi not in generated_multi:
            generated_multi.add(random_multi)
            generated = True

    return random_multi

#генерация открытого\закрытого ключа и метки M для каждого избирателя
def generate_specific_voters_data_list():
    global voters_info_list
    voters_list_from_CIK = CIK.voter_list
    i = 1
    for voter in voters_list_from_CIK:
        private_key = RSA.generate(1024)
        public_key = private_key.publickey()
        M = generate_unique_mark()
        r = generate_unique_closed_miltiplier()
        voter['private_key'] = private_key
        voter['public_key'] = public_key
        voter['M'] = M
        voter['r'] = r
        print(f'Избиратель {i} сгенерирован')
        i += 1

    #создание списка с такими данными для дальнейшей работы
    voters_info_list = [{'id': voter['id'], 'public_key': voter['public_key'], 'private_key': voter['private_key'], 'M': voter['M'], 'r': voter['r']} for voter in voters_list_from_CIK]


#протокол для "ослепления" метки M
def blinding_protocol():
    global voter_with_id_blind_and_sign
    #используем уникальный закрывающий множитель r, открытый ключ из ЦИК для скрытия метки M
    for voter in voters_info_list:
        blinded_message = (voter['r'] ** CIK.public_key.e * voter['M']) % CIK.public_key.n

        #перевод в байты для хэширования
        blinded_message_bytes = blinded_message.to_bytes((blinded_message.bit_length() + 7) // 8, 'big')
        #хэшируем полученное сообщение
        hashed_blinded_message = SHA1.new(blinded_message_bytes)

        #подписываем захэшированное сообщение с закрытым ключом каждого избирателя
        signatured_message = PKCS115_SigScheme(voter['private_key']).sign(hashed_blinded_message)

        voter['blind_m'] = hashed_blinded_message
        voter['sign_m'] = signatured_message

    #создаем список с полученными данными
    voter_with_id_blind_and_sign = [{'id': voter['id'], 'blind_m': voter['blind_m'], 'public_key': voter['public_key'], 'sign_m': voter['sign_m'], 'private_key': voter['private_key'], 'r': voter['r'], 'M': voter['M']} for voter in voters_info_list]

def remove_r():
    global anonim_list
    for voter in CIK.voter_with_id_blind_and_sign_from_cik:
        hashed_message_from_cik = SHA1.new()
        hashed_message_from_cik.update(voter['sign_m_from_cik'])
        #вычисление обратного значения r
        r_inv = pow(voter['r'], -1, CIK.public_key.n)
        #ЭЦП комисии после снятия закрытого множителя r
        DS_int = int.from_bytes(voter['sign_m_from_cik'], byteorder='big')
        DS = (DS_int * r_inv) % CIK.public_key.n
        voter['DS'] = DS
        vote = random.choice(bulliten)
        voter['vote'] = vote
    #список с данными для отправки
    anonim_list = [{'M': voter['M'], 'vote': voter['vote'], 'DS': voter['DS']} for voter in CIK.voter_with_id_blind_and_sign_from_cik]
