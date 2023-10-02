from experiments.utils import ensemble_by_model_run
from library.ensemble import ensemble
from experiments.ensemble_guide import Bests, Worsts
from experiments.constants import MOTHER_PATH, TABLE6_GUIDE_NAME, RUN, TEST_FILE_NAME, MBR_PATH,\
    COMB_BEST_NAME, COMB_WORST_NAME
import pandas as pd
import os
import argparse

def write_ensemble(ensemble, path):
    open(path, 'w').write('\n'.join(ensemble))
    print("Saved to", path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--Run", default=None, action='append')
    parser.add_argument("--combination_of_the", default=None, action='append', choices=['Bests','Worsts'])
    parser.add_argument("--references", nargs='*')
    parser.add_argument("--MBR_mode", default='generative', choices=['generative','selective'])
    parser.add_argument("--file_name", default=TEST_FILE_NAME, help="For --Run and --combination_of_the")
    parser.add_argument("--write_directory", default=None)
    parser.add_argument("--output_file_name", default=None)
    parser.add_argument("--Run_all", action="store_true")
    config = parser.parse_args()
    if config.write_directory is None:
        config.write_directory = os.path.join(MOTHER_PATH, MBR_PATH[config.MBR_mode])
    if config.output_file_name is None:
        config.output_file_name = config.file_name
    
    guide = pd.read_csv(os.path.join(MOTHER_PATH, TABLE6_GUIDE_NAME)).set_index(RUN)
    if config.Run_all:
        config.Run = guide.index
        config.combination_of_the = ['Bests','Worsts']

    if config.Run is not None:
        for run in config.Run:
            ensembles = ensemble_by_model_run(dict(guide.loc[int(run)]), file_name=config.file_name, MBR_mode=config.MBR_mode)
            write_ensemble(ensembles, os.path.join(config.write_directory, RUN+str(run), config.output_file_name))

    if config.combination_of_the is not None:
        if 'Bests' in config.combination_of_the:
            ensembles = ensemble_by_model_run(Bests, file_name=config.file_name, MBR_mode=config.MBR_mode)
            write_ensemble(ensembles, os.path.join(config.write_directory, COMB_BEST_NAME, config.output_file_name))
        if 'Worsts' in config.combination_of_the:
            ensembles = ensemble_by_model_run(Worsts, file_name=config.file_name, MBR_mode=config.MBR_mode)
            write_ensemble(ensembles, os.path.join(config.write_directory, COMB_WORST_NAME, config.output_file_name))

    if config.references is not None:
        references = [open(path).readlines() for path in config.references]
        ensembles = ensemble(references, MBR_mode=config.MBR_mode)
        write_ensemble(ensembles, os.path.join(config.write_directory, config.output_file_name))

    
if __name__ == '__main__':
    main()