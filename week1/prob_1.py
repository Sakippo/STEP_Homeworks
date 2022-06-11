
def sort(word):
    letters = sorted(word)
    sorted_word = "".join(letters)

    return sorted_word

def binary_search(word, dictionary): 
    #二分探索
    left, right = 0, len(dictionary)-1
    while  left <= right:
        center = (left + right)//2
        
        if word == dictionary[center][0]:
            return center
        elif word < dictionary[center][0]:
            right = center - 1
        else:
            left = center + 1
    
    return -1

def anagram_search(word,dictionary):
    anagram = []
    key = binary_search(word,dictionary)
    
    if key != -1:
        #全てのanagramを列挙
        anagram.append(dictionary[key][1])
        #二分探索で見つかったkeyの前後を探索
        for i in range(key+1, len(dictionary)):
            if word == dictionary[i][0]:
                anagram.append(dictionary[i][1])
            else:
                break

        for i in reversed(range(0, key)):
            if word == dictionary[i][0]:
                anagram.append(dictionary[i][1])
            else:
                break
    
    return anagram

def better_solution(random_word, dictionary): 
    sorted_random_word = sort(random_word) #文字列のソート
    
    anagram = anagram_search(sorted_random_word, dictionary)

    return anagram

if __name__ == "__main__":

    random_word = input()

    text = open('words.txt', 'r')
    dictionary = []
    for word in text:
        dictionary.append(word.replace("\n", ""))
    
    new_dictionary = []
    for word in dictionary:
        new_dictionary.append((sort(word),word)) #辞書の単語をソートした文字列と元の単語のリストを作成
    new_dictionary.sort() 
    
    anagram = better_solution(random_word, new_dictionary)
    for word in anagram:
        print(word)

    text.close()