from experiments.figure1_guide import BATCHES, MODEL_RENAMING
from experiments.constants import MOTHER_PATH, TEST_FILE_NAME, GOLD_NAME
from KimEval import sentence_level_f1
from library.ensemble import ensemble
from tqdm import tqdm
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
import matplotlib.pyplot as plt
import os

def bar_numbers(golds, models):
    references = [open(os.path.join(MOTHER_PATH, model, run, TEST_FILE_NAME)).readlines() for model,run in models]
    inners = sorted([sentence_level_f1(golds, r) for r in references])
    ensembles = ensemble(references)
    outer = sentence_level_f1(golds, ensembles)
    return inners, outer

def bar_row(golds, models):
    inners, outer = bar_numbers(golds, models)
    return (list(zip([model[0] for model in models], inners)), outer)

def figure_1():
    golds = open(os.path.join(MOTHER_PATH, GOLD_NAME, TEST_FILE_NAME)).readlines()
    data = [[bar_row(golds, b) for b in batch] for batch in tqdm(BATCHES)]
    bar_width = 0.25
    y_low = min([d[1] for da in data for d in da[0][0]]+[d[1] for da in data for d in da[1][0]]) - 5
    y_low = 16

    def plot_one_group(ax, start, models, overal, color, line, hatch, label, text_only_on=None, annotate=None, denoising_overal=None):
        overal_width = bar_width*len(models)
        overal_bar = ax.bar(
                [start+bar_width],
                [overal],
                width=overal_width,
                edgecolor='black',
                hatch=hatch,
                facecolor='none',
                linestyle=line,
                label=label,
                alpha=0.35,
        )
        bars = ax.bar(
                [start+i*bar_width for i in range(len(models))],
                [m[1] for m in models],
                width=bar_width,
                edgecolor='grey',
                facecolor=color,
                alpha=0.7,
        )
        annotations_color = 'blue'
        if annotate=='denoising':
            ax.annotate("", xy=(start+(len(models)-1)*bar_width, max([m[1] for m in models])-.5), xytext=(start+(len(models)-1)*bar_width, overal+.3),
                        arrowprops=dict(arrowstyle="<->", lw=1, color=annotations_color))
            ax.annotate(
                'Denoising',
                xy=(start+(len(models)-1)*bar_width, overal+.3), xycoords='data',
                xytext=(-5.2*start, 31), textcoords='offset points',
                fontsize=10, color=annotations_color, fontstyle='italic')
            ax.annotate(
                'effect',
                xy=(start+(len(models)-1)*bar_width, overal+.3), xycoords='data',
                xytext=(-5.2*start, 20), textcoords='offset points',
                arrowprops=dict(arrowstyle="-", connectionstyle="angle,angleA=0,angleB=90,rad=10",color=annotations_color),
                fontsize=10, color=annotations_color, fontstyle='italic')
        if annotate=='util':
            ax.annotate("", xy=(start-.5*bar_width, denoising_overal-0.5), xytext=(start-.5*bar_width, overal+.5),
                        arrowprops=dict(arrowstyle="<->", lw=1, color=annotations_color))
            ax.annotate(
                'Additional\nboost\ngained by\nutilizing\nexpertise',
                xy=(start-.5*bar_width, overal+.5), xycoords='data',
                xytext=(start, 15), textcoords='offset points',
                arrowprops=dict(arrowstyle="-", connectionstyle="angle,angleA=0,angleB=90,rad=10",color=annotations_color),
                fontsize=10, color=annotations_color, fontstyle='italic')
        for i, (bar, label) in enumerate(zip(bars, [m[0] for m in models])):
                if text_only_on is not None and text_only_on!=i:
                    continue
                yval = bar.get_height()
                ax.text(
                        bar.get_x() + bar.get_width()/2,
                        y_low + 1,
                        MODEL_RENAMING[label],
                        ha='center',
                        va='bottom',
                        color='black',
                        fontsize=10,
                        rotation=90,
                )
                ax.text(
                        bar.get_x() + bar.get_width()/2,
                        max(yval-5, 34),
                        yval,
                        ha='center',
                        va='bottom',
                        color='black',
                        fontsize=10,
                        rotation=90,
                )
        ax.text(
                overal_bar[0].get_x() + overal_bar[0].get_width()/2,
                overal,
                overal,
                ha='center',
                va='bottom',
                color='black',
                fontsize=10,
        )
        return start + overal_width, overal_bar

    fig, ax = plt.subplots(figsize=(15, 6))
    start = bar_width
    start = 0
    for i, ((denoising_models, denoising_overal), (utilizing_models, utilizing_overal)) in enumerate(data):
            is_last = i==len(data)-1
            start, denoising_bar = plot_one_group(ax, start, denoising_models, denoising_overal, '#daedfe', 'dotted', '/', 'Ensemble of different runs', annotate='denoising' if is_last else None)
            start, utilizing_bar = plot_one_group(ax, start, utilizing_models, utilizing_overal, '#dafcd9', 'dashdot', '....', 'Ensemble of different models', annotate='util' if is_last else None, denoising_overal=denoising_overal)
            start += bar_width/2
    plt.xticks([2.5*bar_width+6.5*i*bar_width for i in range(7)], [f'Group {i+1}' for i in range(7)],fontsize=13)
    plt.yticks(fontsize=13)
    plt.legend(handles=[denoising_bar, utilizing_bar], fontsize=13)
    plt.ylim(y_low, max([d[1][1] for d in data])+3)
    plt.xlim(0-bar_width, start-bar_width/2)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.savefig('figure1.png')