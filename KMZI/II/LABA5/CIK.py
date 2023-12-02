import Voter
import random
import string
from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme


#просто обьявление всех глобальных переменных
voter_list, voter_with_id_blind_and_sign_from_cik = [], {}
private_key, public_key = None, None
#просто обьявление всех глобальных переменных


#создание случайного списка "избирателей", данные просто пустышки
def generate_voter_list(num_voters):
        global voter_list

        for _ in range(num_voters):
            voter_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            voter_name = ''.join(random.choices(string.ascii_uppercase, k=5))
            voter_age = random.randint(18, 90)
            voter_address = f"Street {random.randint(1, 100)}, City"
            
            voter = {
                'id': voter_id,
                'name': voter_name,
                'age': voter_age,
                'address': voter_address
            }

            voter_list.append(voter)

#генерирование пары открытый/закрытый ключ для RSA
def generate_key_pair():
    global private_key, public_key
    private_key = RSA.generate(1024)
    public_key = private_key.publickey()  #создание публичного ключа на основе закрытого
    # print("Private key: ", private_key.export_key().decode())
    # print("Public key: ", public_key.export_key().decode())

#проверяем подпись от избирателей
def check_signature():
    global voter_with_id_blind_and_sign_from_cik
    for voter in Voter.voter_with_id_blind_and_sign:
        try: 
            PKCS115_SigScheme(voter['public_key']).verify(voter['blind_m'], voter['sign_m'])
            print(f"Подпись избирателя с ID: {voter['id']} верна.")
            signatured_message_from_cik = PKCS115_SigScheme(private_key).sign(voter['blind_m'])
            voter['sign_m_from_cik'] = signatured_message_from_cik
        except:
            print(f"Подпись избирателя с ID: {voter['id']} не верна.")

    voter_with_id_blind_and_sign_from_cik = [{'id': voter['id'], 'blind_m': voter['blind_m'], 'public_key': voter['public_key'], 'sign_m_from_cik': voter['sign_m_from_cik'], 'r': voter['r'], 'M': voter['M']} for voter in Voter.voter_with_id_blind_and_sign]

def verify_and_results():
    candidateA, candidateB, candidateC = 0,0,0
    for voter in Voter.anonim_list:
        print(f'Метка М: {voter["M"]}, Голос отдан за {voter["vote"]}')
        match voter["vote"]:
            case "Candidate A":
                candidateA += 1
            case "Candidate B":
                candidateB += 1
            case "Candidate C":
                candidateC += 1
    winner = max({"Candidate A": candidateA, "Candidate B": candidateB, "Candidate C": candidateC}.items(), key=lambda x: x[1])
    print(f'Результаты: за Кандидата А отдано {candidateA} голосов,за Кандидата Б отдано {candidateB} голосов,за Кандидата С отдано {candidateC} голосов. Победил {winner[0]} с {winner[1]} голосами')
