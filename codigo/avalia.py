from os import listdir
from os.path import isfile, join
from matplotlib import pyplot as plt
from matplotlib import interactive
import pandas as pd
import numpy as np

pasta_input = "output_separado\\"
pasta_input_in = "input\\"
encoding = "utf8"

file_input = "output_5.1.04_3.txt"

def recall_precision(retornados, Nrel):
    RA_sz = 0
    ret_count = 0
    rec_prec = []

    for ret in retornados:
        ret_count += 1
        if ret[1] == ret[0]:
            RA_sz += 1
            rec_prec.append( (RA_sz/Nrel, RA_sz/ret_count) )
    return rec_prec

def mean_avg_prec(retornados, Nrel):
    rec_prec_list = recall_precision(retornados, Nrel)
  
    m_avg_p = 0
    for rp in rec_prec_list:
        m_avg_p += rp[1] / Nrel
  
    return m_avg_p

# Calcula o numero de relevantes para cada artigo
Nrel = dict()
files = [f for f in listdir(pasta_input_in) if isfile(join(pasta_input_in, f))]
for file in files:
    file_split = file.split('_')
    artigo = int(file_split[0])
    paragrafo = int(file_split[1])
    if paragrafo == 0:
        Nrel[artigo] = 0
    else:
        Nrel[artigo] += 1

MAP_list = [0]
files = [f for f in listdir(pasta_input) if isfile(join(pasta_input, f))]
files.sort(key = lambda f: int(f.split('_')[-1].split('.')[0]))
for file in files:
    retornados = []
    with open(join(pasta_input, file), "r", encoding=encoding) as file_r:
        lines = file_r.readlines()

        for line in lines:
            if line == '\n':
                continue
        
            line = line.split('_')
            line[0] = int(line[0])
            line[1] = int(line[1])
            line[2] = int(line[2])
            line[3] = float(line[3])
            perg = line[0]
            if len(retornados) <= perg:
                retornados.append([])
            retornados[perg].append(line)

    MAP = 0
    for i in range(len(retornados)):
        ret = retornados[i]
        mi = mean_avg_prec(ret,Nrel[i])
        MAP += mi/len(retornados)
    MAP_list.append(MAP)

interactive(True)

df = pd.DataFrame(np.array(MAP_list))
plt = df.plot(title='Grafico de MAP por respostas retornadas',legend=None)
plt.set_xlabel('Quantidade de respostas retornadas por pergunta')
plt.set_ylabel('Mean Average Precision')
plt

for i in range(0,140):
    print(str(i) + " " + str(MAP_list[i]))
