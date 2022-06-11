SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]

def calculate_score(word):
    score = 0
    for character in list(word):
        score += SCORES[ord(character) - ord('a')]
    return score

def character_count(word):
    characters = [0] * 26
    for i in list(word):
        characters[ord(i)-97]+=1
    
    return characters

def anagram_search(word_characters, dictionary):
    anagram = ""
    for word in dictionary:
        boolean = True
        for i in range(0, 26):
            if word_characters[i] < word[0][i]:
                boolean = False
        
        if boolean:
            anagram = word[1] #最大スコアのanagramが見つかったらbreak
            break
    
    return anagram


def best_solution(random_word, new_dictionary):
    word_characters = character_count(random_word) #入力のアルファベットを数える
    anagram = anagram_search(word_characters, new_dictionary)
    
    return anagram

def main(files, new_dictionary):
    for open_file in files:
        input_file = open(open_file, 'r') #ファイル読み込み
    
        solutions = []
        for word in input_file:
            solutions.append(best_solution(word.replace("\n", ""), new_dictionary))
        input_file.close()

        #ファイル書き出し
        if open_file == 'small.txt':
            output_file = open('small_answer.txt','w')
        elif open_file == 'medium.txt':
            output_file = open('medium_answer.txt','w')
        else:
            output_file = open('large_answer.txt','w')

        for word in solutions:
            output_file.write(word + '\n')

        output_file.close()

if __name__ == "__main__":

    text = open('words.txt', 'r')
    dictionary = []
    for word in text:
        dictionary.append(word.replace("\n", ""))
    
    #辞書の単語のアルファベットを数える＆スコアを計算
    new_dictionary = []
    for word in dictionary:
        new_dictionary.append((character_count(word), word, calculate_score(word)))
    new_dictionary.sort(reverse=True, key=lambda x:x[2]) #スコア順にソート

    main(['small.txt','medium.txt','large.txt'], new_dictionary)

    text.close()