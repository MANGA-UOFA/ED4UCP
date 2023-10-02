from KimEval import sentence_level_f1
from experiments.constants import MOTHER_PATH, TABLE6_GUIDE_NAME, RNNG_TEST_FILE_NAME, URNNG_TEST_FILE_NAME, TEST_FILE_NAME, GOLD_NAME,\
    MBR_GEN_PATH, MBR_SEL_PATH, COMB_BEST_NAME, COMB_WORST_NAME, UNION_PATH, RUN, ORACLE
from library.heuristics import left, right, oracle
import pandas as pd
import numpy as np
import os

def mean_std_run1(golds, model, runs):
    runs_f1 = []
    for run in runs:
        f1 = sentence_level_f1(golds, open(os.path.join(MOTHER_PATH, model, run, TEST_FILE_NAME)).readlines())
        runs_f1.append(f1)
    mean, std = round(np.mean(runs_f1), 1), round(np.std(runs_f1),1)
    return mean, std, runs_f1[0]

def table_2():
    golds = open(os.path.join(MOTHER_PATH, GOLD_NAME, TEST_FILE_NAME)).readlines()
    print('='*72)
    print( '   Model\t\t\t| Mean\t\t| Run1\t +RNNG\t +URNNG')
    print('-'*72)
    print(f' 1  Left branching\t\t| {sentence_level_f1(golds, map(left, golds))}\t\t|')
    print(f' 2  Right branching\t\t| {sentence_level_f1(golds, map(right, golds))}\t\t|')
    print('-'*72)

    guide = pd.read_csv(os.path.join(MOTHER_PATH, TABLE6_GUIDE_NAME)).set_index(RUN)
    run1 = guide.index[0]

    for i, model in enumerate(guide.columns):
        mean, std, run1_f1 = mean_std_run1(golds, model, guide[model])
        rnng_f1 = sentence_level_f1(golds, open(os.path.join(MOTHER_PATH, model, guide.loc[run1, model], RNNG_TEST_FILE_NAME)).readlines())
        urnng_f1 = sentence_level_f1(golds, open(os.path.join(MOTHER_PATH, model, guide.loc[run1, model], URNNG_TEST_FILE_NAME)).readlines())
        print(f' {i+3}  {model}\t\t'+("\t" if len(model)<12 else "")+f'| {mean}±{std}\t| {run1_f1}\t {rnng_f1}\t {urnng_f1}')
    print('-'*72)

    union_rnng_f1 = sentence_level_f1(golds, open(os.path.join(MOTHER_PATH, UNION_PATH, RNNG_TEST_FILE_NAME)).readlines())
    union_urnng_f1 = sentence_level_f1(golds, open(os.path.join(MOTHER_PATH, UNION_PATH, URNNG_TEST_FILE_NAME)).readlines())
    print(f' {len(guide.columns)+3} Union distillation\t\t| \t\t| \t {union_rnng_f1}\t {union_urnng_f1}')

    mean, std, run1_f1 = mean_std_run1(golds, MBR_SEL_PATH, [RUN+str(i) for i in guide.index])
    rnng_f1 = sentence_level_f1(golds, open(os.path.join(MOTHER_PATH, MBR_SEL_PATH, RUN+str(run1), RNNG_TEST_FILE_NAME)).readlines())
    urnng_f1 = sentence_level_f1(golds, open(os.path.join(MOTHER_PATH, MBR_SEL_PATH, RUN+str(run1), URNNG_TEST_FILE_NAME)).readlines())
    print(f' {len(guide.columns)+4} {MBR_SEL_PATH}\t\t'+("\t" if len(MBR_SEL_PATH)<12 else "")+f'| {mean}±{std}\t| {run1_f1}\t {rnng_f1}\t {urnng_f1}')

    mean, std, run1_f1 = mean_std_run1(golds, MBR_GEN_PATH, [RUN+str(i) for i in guide.index])
    rnng_f1 = sentence_level_f1(golds, open(os.path.join(MOTHER_PATH, MBR_GEN_PATH, RUN+str(run1), RNNG_TEST_FILE_NAME)).readlines())
    urnng_f1 = sentence_level_f1(golds, open(os.path.join(MOTHER_PATH, MBR_GEN_PATH, RUN+str(run1), URNNG_TEST_FILE_NAME)).readlines())
    print(f' {len(guide.columns)+5} {MBR_GEN_PATH}\t\t'+("\t" if len(MBR_GEN_PATH)<12 else "")+f'| {mean}±{std}\t| {run1_f1}\t {rnng_f1}\t {urnng_f1}')

    for i, comb in enumerate([COMB_WORST_NAME, COMB_BEST_NAME]):
        f1 = sentence_level_f1(golds, open(os.path.join(MOTHER_PATH, MBR_GEN_PATH, comb, TEST_FILE_NAME)).readlines())
        rnng_f1 = sentence_level_f1(golds, open(os.path.join(MOTHER_PATH, MBR_GEN_PATH, comb, RNNG_TEST_FILE_NAME)).readlines())
        urnng_f1 = sentence_level_f1(golds, open(os.path.join(MOTHER_PATH, MBR_GEN_PATH, comb, URNNG_TEST_FILE_NAME)).readlines())
        print(f' {len(guide.columns)+6+i} {MBR_GEN_PATH}({comb})\t'+f'| {f1}\t\t| \t {rnng_f1}\t {urnng_f1}')

    print('-'*72)
    f1 = sentence_level_f1(golds, map(oracle, golds))
    rnng_f1 = sentence_level_f1(golds, open(os.path.join(MOTHER_PATH, ORACLE, RNNG_TEST_FILE_NAME)).readlines())
    urnng_f1 = sentence_level_f1(golds, open(os.path.join(MOTHER_PATH, ORACLE, URNNG_TEST_FILE_NAME)).readlines())
    print(f' {len(guide.columns)+8} Oracle\t\t\t| {f1}\t\t| \t {rnng_f1}\t {urnng_f1}')
    print('-'*72)
