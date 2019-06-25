# Separa os artigos em paragrafos

from os import listdir
from os.path import isfile, join

pasta_input = "raw\\"
pasta_output = "input\\"
encoding = "utf8"
separador = "."

files = [f for f in listdir(pasta_input) if isfile(join(pasta_input, f))]
num_doc = 0

for file in files:
    with open(join(pasta_input, file), "r", encoding=encoding) as file_r:
        trechos = []
        lines = file_r.readlines()

        num_line = 0
        for line in lines:
            if line == '\n':
                continue
            file_output = str(num_doc) + "_" + str(num_line)
            with open(join(pasta_output, file_output), "w", encoding=encoding) as file_w:
                file_w.write(line)
            num_line += 1
        num_doc += 1
