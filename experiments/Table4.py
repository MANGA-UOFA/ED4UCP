from experiments.constants import MOTHER_PATH, ENTROPIES
import numpy as np
import os

def table_4():
    distillation_methods = os.listdir(os.path.join(MOTHER_PATH, ENTROPIES))
    print('='*40)
    print('Distillation Approach\tMean\tStd\t')
    print('-'*40)
    for distillation_method in distillation_methods:
        runs = os.listdir(os.path.join(MOTHER_PATH, ENTROPIES, distillation_method))
        entropies = [np.mean(list(map(float, open(os.path.join(MOTHER_PATH, ENTROPIES, distillation_method, run)).read().strip().split('\n')))) for run in runs]
        print(f'{distillation_method}\t\t\t{round(np.mean(entropies), 2)}\t{round(np.std(entropies), 2)}')
    print('='*40)