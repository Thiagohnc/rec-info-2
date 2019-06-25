import fileinput
from os import listdir
from os.path import isfile, join
import numpy as np
import time
import re
from math import log
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

vetor_dict = dict()
idf = dict()

# Converte os valores do vetor para float e retorna uma copia
def copia_vetor(vetor):
    vet = []
    for v in vetor:
        vet.append(v)
    for i in range(len(vet)):
        vet[i] = float(vet[i])
    return vet

# Cria um dicionario que mapeia cada palavra a seu vetor
def cria_dicionario(perguntas, respostas):
    global vetor_dict

    palavras = []
    for p in perguntas:
        for termo in p.termos:
            palavras.append(termo)
    for r in respostas:
        for termo in r.termos:
            palavras.append(termo)
    palavras = list(set(palavras))

    counta = 0
    countb = 0
    with open("glove.42B.300d.txt", "r", encoding = "utf8") as file_glove:
        for line in file_glove:
            countb += 1
            line = line.split(' ')
            palavra = line[0]

            # Adiciona o vetor no dicionario
            if palavra in palavras:
                counta += 1
                line[-1] = line[-1][0:-1]
                vetor = line[1:]
                vetor_dict[palavra] = np.array(copia_vetor(vetor))

# Calcula a similaridade do cosseno
def cos_sim(a, b):
    global vetor_dict
    
    if a not in vetor_dict or b not in vetor_dict:
        return 0.0

    va = vetor_dict[a]
    vb = vetor_dict[b]
    return np.dot(va,vb) / (np.linalg.norm(va) * np.linalg.norm(vb))

def align(qi, A, Kpos, Kneg, Lambda):
    pos = 0
    neg = 0

    termos = []
    for t in A.termos:
        termos.append((cos_sim(t,qi), t))
    termos.sort(key = lambda t: -t[0])

    for k in range(0, Kpos):
        pos += ( 1/ (k+1) ) * termos[k][0]

    for k in range(0, Kneg):
        neg += ( 1/ (k+1) ) * termos[-k-1][0]

    return pos + Lambda * neg

def calcula_score(pergunta, resposta, Kpos, Kneg, Lambda):
    score = 0

    for termo in pergunta.termos:
        score += idf[termo] * align(termo, resposta, Kpos, Kneg, Lambda)

    return score

def rankeia_respostas(pergunta, respostas, Kpos, Kneg, Lambda):
    rankeadas = []

    for r in respostas:
        rankeadas.append((r,calcula_score(pergunta,r,Kpos,Kneg,Lambda)))
    rankeadas.sort(key = lambda r: -r[1])

    return rankeadas

# Tokeniza as palavras, remove stopwords e tudo que nao seja letra
def tokeniza(string):
    string = re.sub(r'[^a-zA-Z ]', '', string)
    palavras = word_tokenize(string)
    stopWords = set(stopwords.words('english'))
    tratadas = []
    for p in palavras:
        if p.lower() not in stopWords:
            tratadas.append(p.lower())
    return tratadas
    
def le_documentos(perguntas, respostas, pasta_input, encoding = 'utf8'):
    files = [f for f in listdir(pasta_input) if isfile(join(pasta_input, f))]
    for file in files:
        (doc,paragrafo) = file.split('_')
        with open(join(pasta_input, file), "r", encoding=encoding) as file_r:
            lines = file_r.readlines()
            line = lines[0][0:-1]
            if paragrafo == '0':
                perguntas.append(Documento(doc,tokeniza(line),paragrafo))
            else:
                respostas.append(Documento(doc,tokeniza(line),paragrafo))

def constroi_idf(perguntas_raw):
    N = len(perguntas_raw)
    perguntas = []
    palavras = []

    for pr in perguntas_raw:
        for termo in pr.termos:
            palavras.append(termo)
    palavras = list(set(palavras))

    for p in palavras:
        doc_freq = 0
        for pr in perguntas_raw:
            if p in pr.termos:
                doc_freq += 1
        idf[p] = log((N - doc_freq + 0.5) / (doc_freq + 0.5))
        
class Documento:
    def __init__(self, doc, termos, paragrafo):
        self.doc = doc
        self.termos = termos
        self.paragrafo = paragrafo

pasta_output = "output\\"
perguntas = []
respostas = []
le_documentos(perguntas, respostas, "input\\")

cria_dicionario(perguntas,respostas)
constroi_idf(perguntas)

perguntas.sort(key = lambda p: int(p.doc))

N = len(perguntas)
with open(pasta_output + "output_raw.txt", "w", encoding = "utf8") as file_output:
    for p in perguntas:
        rankeadas = rankeia_respostas(p,respostas,Kpos=5,Kneg=2,Lambda=0.5)
        for r in rankeadas:
            file_output.write(str(p.doc) + '_' + str(r[0].doc) + '_' + str(r[0].paragrafo) + '_' + str(r[1]) + '\n')
