import re
import pickle

data_folder = 'C:\\Users\\coolt\\OneDrive\\AAUni\\third_year\\fyp\\ML_Coding_Playground\\TwitterMetaVector\\'
file = data_folder + 'SentiWords_1.1.txt'
reg = '#[A-Z a-z, 0-9]*'
r = re.compile(reg)
f = open(file, 'r')
clearLines = {}
c = 0
output = [0, 0, 0]
for i in f:
    c += 1
    if c >= 27:
        line = re.sub(reg, '', i)[:-1].split('\t')
        if float(line[1]) > 0.2:
            output[0] += 1
            clearLines[line[0]] = 1
        elif float(line[1]) < -0.2:
            output[1] += 1
            clearLines[line[0]] = -1
        else:
            output[2] += 1
            clearLines[line[0]] = 0
print(output)
pickle.dump(clearLines, open('SentiWord.p', 'wb'))
# print(clearLines)
for i in clearLines:
    if clearLines[i] == -1:
        print(i)
