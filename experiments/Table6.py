from KimEval import sentence_level_f1
from experiments.constants import MOTHER_PATH, TABLE6_GUIDE_NAME, PREVIOUSLY_REPORTED_NUMBERS, TEST_FILE_NAME, GOLD_NAME, RUN
import pandas as pd
import os

def table_6():
    guide = pd.read_csv(os.path.join(MOTHER_PATH, TABLE6_GUIDE_NAME)).set_index(RUN)
    golds = open(os.path.join(MOTHER_PATH, GOLD_NAME, TEST_FILE_NAME)).readlines()
    print('Model\t| Run\t| F1\t| Source')
    print('='*60)
    for model in guide.columns:
        print(f'{model}:\t{PREVIOUSLY_REPORTED_NUMBERS[model]} Reported in the reference paper.')
        print('\t','-'*51)
        for run in guide.index:
            f1 = sentence_level_f1(
                golds,
                open(os.path.join(MOTHER_PATH, model, guide.loc[run, model], TEST_FILE_NAME)).readlines()
            )
            print(f'\t  {run}\t| {f1}\t| {guide.loc[run, model]}')
        print('-'*60)