from KimEval import constituency_label_recall
from experiments.constants import TABLE6_GUIDE_NAME, MOTHER_PATH, RUN, TEST_FILE_NAME, GOLD_NAME
from library.ensemble import ensemble
import pandas as pd
from tqdm import tqdm
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
import matplotlib.pyplot as plt
import os
import seaborn as sns

def create_recall_df(golds, reference, model, top=5):
    recall, coverage = constituency_label_recall(
        golds,
        reference
    )
    recall_df = pd.DataFrame({'tag': recall.keys(), 'Recall': recall.values(), 'Coverage': coverage.values()})
    recall_df = recall_df.sort_values('Coverage', ascending=False).head(top)
    coverage = recall_df['Coverage'].sum()
    recall_df = recall_df.drop(columns='Coverage')
    recall_df['model'] = model
    recall_df['Recall'] *= 100
    return recall_df, coverage*100

def figure_4():
    guide = pd.read_csv(os.path.join(MOTHER_PATH, TABLE6_GUIDE_NAME)).set_index(RUN)
    golds = open(os.path.join(MOTHER_PATH, GOLD_NAME, TEST_FILE_NAME)).readlines()
    data = []
    for run in tqdm(guide.index):
        references = []
        for model in tqdm(guide.columns):
            variant = guide.loc[run, model]
            reference = open(os.path.join(MOTHER_PATH, model, variant, TEST_FILE_NAME)).readlines()
            references.append(reference)
            recall_df,_ = create_recall_df(golds, reference, model)
            data.append(recall_df)
        recall_df, coverage = create_recall_df(golds, ensemble(references), 'Ensemble')
        data.append(recall_df)
    data = pd.concat(data)
    print(f"Coverage of reported tags: {coverage}%")

    labels = ['Ordered Neurons', 'Neural PCFG', 'Compound PCFG', 'DIORA', 'S-DIORA','ConTest', 'ContexDistort','Our ensemble']
    fig, ax = plt.subplots(figsize=(12, 6))
    ax = sns.barplot(data=data, x="tag", y="Recall", hue="model", palette=sns.light_palette("seagreen", 7)+['#80c3ff'],
                    err_kws={'linewidth': 1, 'color': 'gray'}, capsize=0.05, edgecolor='k', errorbar="sd", width=0.9, alpha=.55)
    for i, bars in enumerate(ax.containers):
        for j, bar in enumerate(bars):
            ax.text(
            bar.get_x() + bar.get_width()/2,
            1,
            labels[i],# if not (j==4 and i==0) else 'ON',
            ha='center',
            va='bottom',
            color='black',
            fontsize=10,
            rotation=90,
            )
    plt.legend().set_visible(False)
    plt.xlabel('').set_visible(False)
    plt.ylabel(r'Recall on PTB test', fontsize=13).set_visible(False)
    plt.yticks(fontsize=13)
    plt.xticks(fontsize=13)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.savefig('figure4.png')