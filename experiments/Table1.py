from KimEval import sentence_level_f1
from experiments.constants import MOTHER_PATH, TEST_FILE_NAME
from experiments.table1_guide import CORR_HETEROGENEOUS, CORR_DIORA
import os

def triangle(models):
    for i in range(len(models)):
        line = []
        for j in range(i+1):
            f1 = sentence_level_f1(
                open(os.path.join(MOTHER_PATH, models[j][0], models[j][1], TEST_FILE_NAME)).readlines(),
                open(os.path.join(MOTHER_PATH, models[i][0], models[i][1], TEST_FILE_NAME)).readlines(),
            )
            line.append(str(f1))
        print(f'{models[i][0]} ({models[i][1]})\t'+("\t" if len(models[i][0]+models[i][1])<12 else "")+'| '+'\t\t '.join(line))
    print('\t\t\t','-'*47)
    print('\t\t\t'+'\t'.join([model[0]+("\t" if len(model[0])<12 else "") for model in models]))
    print('\t\t\t'+'\t'.join([model[1]+("\t" if len(model[1])<12 else "") for model in models]))
    

def table_1():
    print('='*72)
    triangle(CORR_HETEROGENEOUS)
    print('-'*72)
    triangle(CORR_DIORA)
    print('='*72)
