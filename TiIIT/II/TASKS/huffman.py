import heapq
from collections import Counter
from collections import namedtuple

class node(namedtuple("node", ["left", "right"])):
    def walk(self, code, acc):
        self.left.walk(code, acc + "0")
        self.right.walk(code, acc + "1")

class leaf(namedtuple("Leaf",["char"])):
    def walk(self, code, acc):
        code[self.char] = acc or "0"
    
def huffman(s):
    h = []
    for el, freq in Counter(s).items():
        h.append((freq, len(h), leaf(el)))
    heapq.heapify(h)
    count = len(h)

    while len(h) > 1:
        freq1, _, left = heapq.heappop(h)
        freq2, _, right = heapq.heappop(h)

        heapq.heappush(h, (freq1 + freq2, count, node(left, right)))
        count += 1

    code = {}
    if h:
        [(_, _, root)] = h
        root.walk(code, "")
    return code

if __name__=="__main__":
    phrase = '''Значительная корреляция между двумя величинами всегда является свидетельством 
существовании некоторой статистической связи данной выборки, но это связь не обязательно должна 
наблюдаться для другой выборки и иметь причинно-следственный характер. Часто заманчивая простота корреляционного 
исследователя подталкивает следователя делать ложные, интуитивные выводы о наличии причинно-следственной связи 
между парами признаков.'''
    phrase = phrase.lower().replace('\n', '')
    code = huffman(phrase)
    encoded = "".join(code[el] for el in phrase)
    
    print(code, end='\n\n')
    print(encoded)