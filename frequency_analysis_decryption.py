
input_text = open('input.txt','r')
frequency_text = open('frequency.txt', 'r')

alph =['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
cypher_alph = ['V', 'N', 'T', 'G', 'P', 'H', 'Z', 'K', 'J', 'W', 'S', 'I', 'U', 'A', 'Q', 'Y', 'M', 'R', 'L', 'E', 'C', 'O', 'F', 'B', 'D', 'X']
correct_guess= {}
for a in range(len(alph)):
    correct_guess[cypher_alph[a]] = alph[a]
input_text = input_text.read()
input_text = input_text.lower()
frequency_text = frequency_text.read()
frequency_text = frequency_text.lower()
import random
def random_alph(alph):
    cypher_alph=[]
    for let in alph:
        cypher_alph.append(let.upper())
    random.shuffle(cypher_alph)
    return cypher_alph
 

def encrypt(alph,cypher_alph,input_text):
    cypher_text=''
    for a in input_text:
        for i in range(len(alph)):
            if a == alph[i]:
                cypher_text += cypher_alph[i]
        if a not in alph:
            cypher_text += a
    return cypher_text

def frequency(alph,text):
    let_freq=[]
    for char in alph:
        let_freq.append([char,text.count(char)])
    let_freq = sorted(let_freq,key=lambda let_freq: let_freq[1],reverse=True)
    return let_freq
        
def base_alph_prob(alph,cypher_lets):
    prob = {}
    for let in alph:
        tmp ={}
        for a in cypher_lets:
            tmp[a]=1./len(cypher_lets)
        prob[let]=tmp
    return prob

def comp_freq_prob(text_freq,cypher_freq,prob,freq_weight=10):
    for t in range(len(text_freq)-2):
        prob[text_freq[t][0]][cypher_freq[t][0]]+=.3
        prob[text_freq[t][0]][cypher_freq[t+1][0]]+=.2
        prob[text_freq[t][0]][cypher_freq[t+2][0]]+=.1
    return prob

def normalize_prob(prob):
    for p in prob:
        val = 0
        for c in prob[p]:
            val += prob[p][c]
        for d in prob[p]:
            prob[p][d] = prob[p][d]/val
    return prob

def best_guess(prob):
    guess={}
    
    for p in prob:
        best = 0.
        for c in prob[p]:
            if prob[p][c] >= best:
                best = prob[p][c]
                guess[p]=c
    dist=0
    for g in guess:
        dist += prob[g][guess[g]]
    inverse_guess = {}
    for g in guess:
        inverse_guess[guess[g]]=g
    return inverse_guess,dist/26

def decrypt(cypher_text,guess):
    decryption = ''
    for c in cypher_text:
        if c in guess:
            decryption+=(guess[c])
        else:
            decryption+=(c)
    return decryption

def find_pairs(text,alph,num=2):
    tmp_dic = {}
    pairs, start, end, double, other = [],[],[],[],[]
    for t in range(len(text)-1):
        if text[t]+text[(t+1)] in tmp_dic:
            tmp_dic[text[t]+text[(t+1)]]+=1
        else:
            tmp_dic[text[t]+text[(t+1)]]=1
    for t in tmp_dic:
        pairs.append([list(t),tmp_dic[t]])
    for p in range(len(pairs)):
        if pairs[p][0][0] in alph or pairs[p][0][1] in alph:
            if pairs[p][0][0] == pairs[p][0][1]:
                double.append(pairs[p])
            elif pairs[p][0][0] == ' ':
                start.append(pairs[p])
            elif pairs[p][0][1] == (' ' or '.' or ',' or '"' or '!' or '?'):
                end.append(pairs[p])
            else:
                other.append(pairs[p])
    double = normalize_pairs(double)
    start = normalize_pairs(start)
    end = normalize_pairs(end)
    other = normalize_pairs(other)
    #print double
    return [double,start,end]

def normalize_pairs(pairs):
    pairs = sorted(pairs,key=lambda pairs: pairs[1],reverse=True)
    pairs = pairs[:26]
    return pairs

def pairs_update_prob(base_pairs,cypher_pairs,prob):
    for p in range(min([len(base_pairs),len(cypher_pairs)])):
        for q in range(min([len(base_pairs),len(cypher_pairs)])):
            for r in range(len(cypher_pairs[q][0])):
                if base_pairs[p][0][r] in prob and cypher_pairs[q][0][r] in prob[base_pairs[p][0][r]]:
                    prob[base_pairs[p][0][r]][cypher_pairs[q][0][r]] += .09/(1+abs(p-q))
    return normalize_prob(prob)

def all_pairs_update(base_pairs,cypher_pairs,prob):
    for p in range(len(base_pairs)):
        prob = pairs_update_prob(base_pairs[p],cypher_pairs[p],prob)
    return prob
cypher_alph = ['V', 'N', 'T', 'G', 'P', 'H', 'Z', 'K', 'J', 'W', 'S', 'I', 'U', 'A', 'Q', 'Y', 'M', 'R', 'L', 'E', 'C', 'O', 'F', 'B', 'D', 'X']

cypher_text = encrypt(alph,cypher_alph,input_text)

text_freq = frequency(alph,frequency_text)
#input_freq = frequency(alph,input_text)
cypher_freq = frequency(cypher_alph,cypher_text)

base_pairs = find_pairs(frequency_text,alph)
base_pairs.append(text_freq)
#print text_freq
#print cypher_freq
cypher_pairs = find_pairs(cypher_text,cypher_alph)
cypher_pairs.append(cypher_freq)
#print base_pairs[0]
#print cypher_pairs[0]
prob = base_alph_prob(alph,cypher_alph)

#prob = comp_freq_prob(text_freq,cypher_freq,prob)
guess = best_guess(prob)

#print guess,len(guess[0])
#print len(guess)
#print decrypt(cypher_text,guess[0])

all_pairs_update(base_pairs,cypher_pairs,prob)
print prob['s']
guess = best_guess(prob)
#print prob['e']['P']
#print guess,len(guess[0])
#for p in range(len(cypher_freq)):
#    print text_freq[p],input_freq[p]
#for p in range(min(len(base_pairs[3]),len(cypher_pairs[3]))):
#    print base_pairs[3][p], cypher_pairs[3][p]
#for p in range(len(cypher_pairs[0])):
#    print cypher_pairs[0][p]
num_correct= 0
for g in guess[0]:    
    #print g,guess[0][g],correct_guess[g]
    if guess[0][g]== correct_guess[g]:
        num_correct += 1
print num_correct
decrypted_text = decrypt(cypher_text,guess[0])
print decrypted_text
decrypted_freq = frequency(alph,decrypted_text)
input_pairs = find_pairs(input_text,alph)
decrypted_pairs = find_pairs(decrypted_text,alph)
d =3
#for p in range(min(len(input_pairs[d]),len(decrypted_pairs[d]),len(base_pairs[d]))):
#    print 'input',input_pairs[d][p],'decryp',decrypted_pairs[d][p],'base',base_pairs[d][p]
#for p in range(len(cypher_freq)):
#    print text_freq[p],decrypted_freq[p]
                  
