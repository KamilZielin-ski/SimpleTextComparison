import re

#Most common recurrent Levenshtein algorithm

def LD(s, t):
    m = len(s)
    n = len(t)
    d = [[0 for x in range(n + 1)] for x in range(m + 1)]
    
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                d[i][j] = j
            elif j == 0:
                d[i][j] = i
            elif s[i-1] == t[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                d[i][j] = min(d[i-1][j] + 1, d[i][j-1] + 1, d[i-1][j-1] + 1)
    
    return d[m][n]

'''
norm(text) - function that stripes down text to basic letters text
'''
 
def norm(text):

    lower_text = text.lower()
    no_special_signs_text = re.sub(r'[^\w\s]','', lower_text) #regular expression for getting rid of any special signs and whitespace characters
    #ignores only character, digits and underscores
    stripped_text = no_special_signs_text.strip()

    return stripped_text

'''
c_bow(text) - funtion used for creating bag of words
'''


def c_bow(text):
    list_text = [norm(text)][0].split() 
    bow = [] 
    for i in list_text:
      if not i in bow:
          bow.append(i);
    return bow


'''
Union Find algorithm - used for grouping similar words 
'''
def union(parent, x, y):
    x_set = find(parent, x)
    y_set = find(parent, y)
    parent[x_set] = y_set

def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, parent[x])
    return parent[x]


'''
Funtion used for finding similar words and grouping them into bags of words according to predefined Levenshtein distance variable: lev_distance 
using Union Find algorithm 
'''

def find_similar_words(text, bow):
    parent = {word: word for word in bow}
    for word in bow:
        for compare_word in bow:
            if word != compare_word:
                lev_distance = LD(word, compare_word)
            
                if lev_distance == 1 or lev_distance == 2:
                    union(parent, word, compare_word)

    groups = {}
    for word in bow:
        parent_word = find(parent, word)
        if parent_word in groups:
            groups[parent_word].append(word)
        else:
            groups[parent_word] = [word]
    return list(groups.values())


'''
Funtion for replacing similar words with the first one in their group
'''

def replace_similar_words(text, similar_words):
    words = text.split()
    for i, word in enumerate(words):
        for group in similar_words:
            if word in group:
                words[i] = group[0]
                break
    return ' '.join(words)