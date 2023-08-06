import hashlib
import json
import os
import pickle
import sys
from copy import deepcopy

import numpy as np

sys.path.insert(0, "../")
sys.path.insert(0, "../../")
from src.datajoint.datajoint_config import *


def jsonify(dct):
    dct_jsonified = {}
    for key in list(dct.keys()):
        if type(dct[key]) == type({}):
            dct_jsonified[key] = jsonify(dct[key])
        elif type(dct[key]) == np.ndarray:
            dct_jsonified[key] = dct[key].tolist()
        else:
            dct_jsonified[key] = dct[key]
    return dct_jsonified


def get_hash(dictionary):
    dictionary_json = json.dumps(dictionary, sort_keys=True).encode("utf-8")
    h = hashlib.md5(dictionary_json).hexdigest()
    return h


folder = os.path.join("../", 'data', 'trained_RNNs', 'CDDM')
subfolders = os.listdir(folder)
for subfolder in subfolders:
    if not subfolder.startswith('.'):
        for file in list(os.listdir(os.path.join(folder, subfolder))):
            if 'params' in file:
                score = file.split('_')[-1].split(".pkl")[0]
                taskname = file.split('_')[1]

        config_dict = json.load(open(os.path.join(folder, subfolder, f'{score}_config.json'), 'rb'))
        net_params_file = os.path.join(folder, subfolder, f'params_CDDM_{score}.pkl')
        net_params = pickle.load(open(net_params_file, 'rb'))

        LA_data_file = os.path.join(folder, subfolder, f'{score}_LA_data.pkl')
        LA_data_file_exists = os.path.exists(LA_data_file)
        LA_data = pickle.load(open(LA_data_file, 'rb')) if LA_data_file_exists else None

        fp_data_file = os.path.join(folder, subfolder, f'{score}_fp_data.pkl')
        fp_data_file_exists = os.path.exists(fp_data_file)
        fp_data = pickle.load(open(fp_data_file, 'rb')) if fp_data_file_exists else None

        psycho_data_file = os.path.join(folder, subfolder, f'{score}_psycho_data.pkl')
        psycho_data_file_exists = os.path.exists(fp_data_file)
        psycho_data = pickle.load(open(psycho_data_file, 'rb')) if psycho_data_file_exists else None

        #         if psycho_data is None: print('found no psycho_data file!')
        #         if fp_data is None: print('found no fp_data file!')
        #         if LA_data is None: print('found no LA_data file!')

        if (psycho_data is None) or (fp_data is None) or (LA_data is None):
            pass  # skip this entry
        else:
            rnn_dj = RNNDJ()
            task_dj = TaskDJ()
            trainer_dj = TrainerDJ()
            if psycho_data_file_exists or fp_data_file_exists or LA_data_file_exists:
                cddm_analysis_dj = CDDMRNNAnalysisDJ()
            else:
                cddm_analysis_dj = None
            config_dict["task_params"]["seed"] = None  # non randomized task!
            task_dj_dict = {"task_name": taskname,
                            "n_steps": config_dict["n_steps"],
                            "n_inputs": config_dict["num_inputs"],
                            "n_outputs": config_dict["num_outputs"],
                            "task_params": config_dict["task_params"],
                            "mask": config_dict["mask"]}
            task_hash = get_hash(jsonify(task_dj_dict))
            task_dj_dict["task_hash"] = task_hash

            trainer_dj_dict = {"max_iter": config_dict["max_iter"],
                               "tol": config_dict["tol"],
                               "lr": config_dict["lr"],
                               "lambda_orth": config_dict["lambda_orth"],
                               "lambda_r": config_dict["lambda_r"],
                               "same_batch": config_dict["same_batch"],
                               "shuffle": False}
            trainer_hash = get_hash(jsonify(trainer_dj_dict))
            trainer_dj_dict["trainer_hash"] = trainer_hash

            rnn_dj_dict = {"task_name": taskname,
                           "mse_score": score,
                           "n": config_dict["N"],
                           "activation_name": config_dict["activation"],
                           "constrained": config_dict["constrained"],
                           "dt": config_dict["dt"],
                           "tau": config_dict["tau"],
                           "sr": config_dict["sr"],
                           "connectivity_density_rec": config_dict["connectivity_density_rec"],
                           "sigma_rec": config_dict["sigma_rec"],
                           "sigma_inp": config_dict["sigma_inp"],
                           "task_hash": task_hash,
                           "trainer_hash": trainer_hash}
            rnn_dj_dict["w_inp"] = net_params["W_inp"]
            rnn_dj_dict["w_rec"] = net_params["W_rec"]
            rnn_dj_dict["w_out"] = net_params["W_out"]
            rnn_dj_dict["b_rec"] = 0 if net_params["bias_rec"] is None else net_params["bias_rec"]
            rnn_hash = get_hash(jsonify(rnn_dj_dict))
            rnn_dj_dict["rnn_hash"] = rnn_hash
            cddm_analysis_dj_dict = {"task_hash": task_hash,
                                     "trainer_hash": trainer_hash,
                                     "rnn_hash": rnn_hash,
                                     "task_name": taskname,
                                     "mse_score": score,
                                     "psycho_data": deepcopy(psycho_data),
                                     "fp_data": deepcopy(fp_data),
                                     "la_data": deepcopy(LA_data)}

            task_dj.insert1(task_dj_dict, skip_duplicates=True)
            trainer_dj.insert1(trainer_dj_dict, skip_duplicates=True)
            rnn_dj.insert1(rnn_dj_dict, skip_duplicates=True)
            if not (cddm_analysis_dj is None):
                cddm_analysis_dj.insert1(cddm_analysis_dj_dict, skip_duplicates=True)

            print(f"successfully created new entry!")
