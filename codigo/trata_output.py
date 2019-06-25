from os import listdir
from os.path import isfile, join

pasta_input = "output\\"
pasta_output = "output_separado\\"
encoding = "utf8"

file_input = "output_raw.txt"

N = 21

for qtd in range(1, 26):
    file_output = "output_5.2.05_" + str(qtd)+ ".txt"
    count = [0] * N
    with open(join(pasta_output, file_output), "w", encoding=encoding) as file_w:
        with open(join(pasta_input, file_input), "r", encoding=encoding) as file_r:
            lines = file_r.readlines()

            for line in lines:
                if line == '\n':
                    continue

                line_split = line.split('_')
                perg = int(line_split[0])
                count[perg] += 1

                if count[perg] <= qtd:
                    file_w.write(line)
