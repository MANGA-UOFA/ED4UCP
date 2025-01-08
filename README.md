# ED4UCP
An official implementation for the paper "Ensemble Distillation for Unsupervised Constituency Parsing."

[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/ensemble-distillation-for-unsupervised/constituency-grammar-induction-on-ptb)](https://paperswithcode.com/sota/constituency-grammar-induction-on-ptb?p=ensemble-distillation-for-unsupervised)

## Install
```bash
conda create -n ED4UCP python=3.9
conda activate ED4UCP
while read requirement; do pip install $requirement; done < requirements.txt 
```

## Evaluation
### Evaluate using the commandline interface
#### Sentence-level F1 score of a prediction w.r.t. some reference
```bash
python evaluate.py --ref path_to_reference_treebank.txt --pred path_to_predicted_treebank.txt
```
### Replicating papers' tables and figures
```bash
python replicate.py [--Table1] [--Table2] [--Table3] [--Table4] [--Table6] [--Figure1] [--Figure2] [--Figure4]
```
Keep those you want to re-evaluate. Discard `[]`s.

### Import and use in python
#### Sentence-level F1 score
```python
from KimEval import sentence_level_f1

f1 = sentence_level_f1(ref=list_of_reference_trees, pred=list_of_predicted_trees, round_it=False)
```
Use bracket-based representations of trees. Include words and constituent labels. Constituent labels don't matter. You can put any character (like `X`) instead of all of them.

#### Corpus-level constituency Label Recall
```python
from KimEval import constituency_label_recall

recall, coverage = constituency_label_recall(ref=list_of_reference_trees, pred=list_of_predicted_trees, round_it=False)
```
Use bracket-based tree representations. Recall is based on constituent labels in reference trees.

## Ensemble
### Ensemble using the commandline interface
```bash
python ensemble.py \
  [--Run <RUN_ID>] [--Run <ANOTHER_RUN_ID>] \
  [--combination_of_the Bests] [--combination_of_the Worsts] \
  [--references <PATH1> <PATH2> ...] \
  [--MBR_mode <generative|selective>] \
  [--file_name <FILE_NAME>] \
  [--write_directory <WRITE_DIRECTORY>] \
  [--output_file_name <OUTPUT_FILE_NAME>] \
  [--Run_all]
```
#### Arguments:
* --Run <RUN_ID>: Specify the run ID to process. It is according to the [experiments' guide](https://github.com/MANGA-UOFA/ED4UCP/blob/main/experiments/table6_guide.csv). This argument can be appended multiple times to process multiple runs.
* --combination_of_the <Bests|Worsts>: This allows you to specify whether you want to create ensembles of the best (or worst) models across runs, according to the [ensemble guide](https://github.com/MANGA-UOFA/ED4UCP/blob/main/experiments/ensemble_guide.py). This argument can be appended multiple times (to cover both).
* --references \<PATH1> \<PATH2> ...: Define one or multiple reference file paths. You can specify multiple paths separated by spaces. It will create an ensemble of all of them.
* --MBR_mode <generative|selective>: Specify the mode as either generative or selective. Details are provided in the paper. Defaults to generative.
* --file_name <FILE_NAME>: Specify the file name for --Run and --combination_of_the. Defaults to the value of TEST_FILE_NAME defined in [the constants](https://github.com/MANGA-UOFA/ED4UCP/blob/main/experiments/constants.py).
* --write_directory <WRITE_DIRECTORY>: Specify the directory where the output should be written. If not specified, it defaults to the directory composed of MOTHER_PATH and the respective MBR_PATH for the chosen MBR_mode (see [the constants](https://github.com/MANGA-UOFA/ED4UCP/blob/main/experiments/constants.py)).
* --output_file_name <OUTPUT_FILE_NAME>: Define the name of the output file. If not specified, it defaults to the value of --file_name.
* --Run_all: If set, it will run all available runs specified in [the guide](https://github.com/MANGA-UOFA/ED4UCP/blob/main/experiments/table6_guide.csv), as well as both combinations of the bests and worsts.

Note: Having multiple ensemble strategies (using `--Run`, `combination_of_the <Bests|Worsts>`, or `--references`) will result in different ensembles, one per each.

### Import and use in python
```python
from library.ensemble import ensemble

ensemble_treebank = ensemble(
  references=list_of_reference_treebanks,
  MBR_mode='generative', # or 'selective'
  right=False, # If True, it will add the right-branching heuristic as an additional reference treebank
)
```
Each reference treebank is a list of bracket-based trees.

## Processed Data
We have provided teachers' outputs, along with our produced parse structures, in the [experiments](https://github.com/MANGA-UOFA/ED4UCP/tree/main/experiments) directory.

---
<a href="https://TheShayegh.github.io/"><img src="https://TheShayegh.github.io/img/favicon.png" style="background-color:red;"/></a>
