from experiments.constants import TABLE6_GUIDE_NAME, MOTHER_PATH, RUN, TEST_FILE_NAME, GOLD_NAME
from experiments.utils import ensemble_by_model_run
from KimEval import sentence_level_f1
import pandas as pd
import numpy as np
from itertools import combinations
from tqdm import tqdm
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
import matplotlib.pyplot as plt
import os
import math

def figure_2():
    guide = pd.read_csv(os.path.join(MOTHER_PATH, TABLE6_GUIDE_NAME)).set_index(RUN)
    golds = open(os.path.join(MOTHER_PATH, GOLD_NAME, TEST_FILE_NAME)).readlines()
    overal = []
    for i in tqdm(range(guide.shape[1])):
        scores = []
        for models in tqdm(combinations(guide.columns, i+1), total=math.comb(guide.shape[1], i+1)):
            this_cobination_scores = []
            for run in tqdm(guide.index):
                model_run = {model: guide.loc[run, model] for model in models}
                ensemble = ensemble_by_model_run(model_run)
                f1 = sentence_level_f1(golds, ensemble)
                this_cobination_scores.append(f1)
            scores.append(this_cobination_scores)
        min_min = min([min(one_cobination_scores) for one_cobination_scores in scores])
        max_max = max([max(one_cobination_scores) for one_cobination_scores in scores])
        scores = [np.mean(one_cobination_scores) for one_cobination_scores in scores]
        min_, max_ = min(scores), max(scores)
        mean = np.mean(scores)
        overal.append((min_min, min_, mean, max_, max_max))

    def plot(ax, data):
        colors = {
                'best': '#AFB7F8',
                'avg': '#6F7DF3',
                'worst': '#2F3779'
        }
        if len(data[0]) == 5:
            minmins, mins, means, maxs, maxmaxs = zip(*data)
        if len(data[0]) == 3:
            mins, means, maxs = zip(*data)
        labels = [str(i) for i in range(1, len(data)+1)]
        ax.plot(labels, maxs, linestyle='-.', marker='^', label='Best-performing combination', color=colors['best'], alpha=1)
        ax.plot(labels, means, marker='o', label='Average over all combinations', color=colors['avg'])
        ax.plot(labels, mins, linestyle='--', marker='s', label='Worst-performing combination', color=colors['worst'], alpha=0.5)
        ax.fill_between(labels, mins, maxs, color=colors['avg'], alpha=0.3)
        if len(data[0]) == 5:
            ax.fill_between(labels, maxs, maxmaxs, color=colors['best'], alpha=0.1/.8)
            ax.fill_between(labels, mins, minmins, color=colors['worst'], alpha=0.05/.8)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        return ax

    fig, ax = plt.subplots(figsize=(6, 5))
    ax = plot(ax, overal)
    plt.tight_layout()
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.legend(loc='lower right', fontsize=16)
    plt.ylabel(r'Ensemble $F_1$ score on PTB test', fontsize=16)
    plt.xlabel('Number of teachers in ensemble', fontsize=16)
    plt.savefig('figure2.png')