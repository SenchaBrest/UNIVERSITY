import numpy as np
phrase = '''Значительная корреляция между двумя величинами всегда является свидетельством 
существовании некоторой статистической связи данной выборки, но это связь не обязательно должна 
наблюдаться для другой выборки и иметь причинно-следственный характер. Часто заманчивая простота корреляционного 
исследователя подталкивает следователя делать ложные, интуитивные выводы о наличии причинно-следственной связи 
между парами признаков.'''
el, counts = np.unique(np.array(list(phrase.lower().replace('\n', ''))), return_counts=True)
p = counts/np.sum(counts)

DICT = dict(sorted(dict(zip(el, p)).items(), key=lambda i: i[1])[::-1])

def shannon_fano(arr, keys, encoding):
    if len(arr) == 1:
        DICT[keys[0]] = encoding
        return 
    
    whole_sum = np.sum(arr)
    i, sum = 0, 0

    while sum < whole_sum / 2:
        sum += arr[i]
        i += 1
    left_arr, right_arr = arr[:i], arr[i:]
    left_keys, right_keys = keys[:i], keys[i:]
    
    shannon_fano(left_arr, left_keys, encoding + "0")
    shannon_fano(right_arr, right_keys, encoding + "1")
    
shannon_fano(list(DICT.values()), list(DICT.keys()), "")

print(DICT, end='\n\n')
for el in phrase.lower().replace('\n', ''):
    print(DICT[el], end='')