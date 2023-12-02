import CIK, Voter

def get_cik_key():
    public_key_from_CIK = CIK.public_key  #получение ключа от ЦИК

def get_voters_info():
    global voters_info_in_CSK
    for voter in Voter.voters_info_list:
        voters_info_in_CSK = [voter['id'], voter['public_key']]  #получение данных(id и ключ) о избирателях