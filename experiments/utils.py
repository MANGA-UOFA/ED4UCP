from experiments.constants import MOTHER_PATH, TEST_FILE_NAME
from library.ensemble import ensemble
import os

def ensemble_by_model_run(models, file_name=TEST_FILE_NAME, MBR_mode='generative'): # MBR_mode: generative or selective
    references = [open(os.path.join(MOTHER_PATH, model, run, file_name)) for model,run in models.items()]
    ensembles = ensemble(references, MBR_mode=MBR_mode)
    return ensembles