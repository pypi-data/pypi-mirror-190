import os
import os.path
import pickle
import logging
import re

import torch
import pandas as pd
import numpy as np
import joblib

DIGITS=3
def glob_re(pattern, strings):
    return list(filter(re.compile(pattern).match, strings))


def predict_on_cluster(data, model):
    """
    Given a binary class data (X, y) and a binary classifier model with sklarn API
    * Predict the label
    * Compute the accuracy
    """
    X = data["X"].values
    y_truth = data["y"].values
    y_pred = model.predict(X)
    metrics = model.get_metrics(X, y_truth)
    return {m: round(metrics[m], DIGITS) for m in metrics}


def load_model(path_model):
    """
    Load a sleep_models model and be verbose
    """
    logging.info(f"Loading model {path_model} ...")
    if path_model.endswith(".joblib"):
        model = joblib.load(path_model)
    elif path_model.endswith(".pkl") or path_model.endswith(".pickle"):
        with open(path_model, "rb") as filehandle:
            model = pickle.load(filehandle)
    elif path_model.endswith(".pth"):
        model = torch.load(path_model)
    else:
        raise Exception(
            f"Model file {path_model} not supported. Please use either .joblib, .pkl or .pth"
        )

    logging.info("Done!")
    return model


def read_val_set(folder, cluster):

    return {
        "X": pd.read_csv(os.path.join(folder, f"{cluster}_X-val.csv"), index_col=0,),
        "y": pd.read_csv(os.path.join(folder, f"{cluster}_y-val.csv"), index_col=0,),
    }


def load_and_predict(input_folder, clusters, cluster_name):
    """
    Load the model for the cluster_name and predict on all clusters (including itself)

    Arguments:

        input_folder (str): Path to cached model and datasets
        clusters (list): List of clusters to run the model on
        cluster_nme (str): Name of the cluster that was used to train the model which will be selected
    """
    data = []
    extensions = ["joblib", "pth", "pickle"]
    pattern = "|".join(extensions)
    model_files = glob_re(r".*(" + pattern + ")", os.listdir(input_folder))
    extension = [ext for ext in extensions if ext in model_files[0]][0]
    model_files = glob_re(r".*(" + extension + ")", os.listdir(input_folder))
    path_model = [f for f in model_files if cluster_name + f".{extension}" == f][0]
    print(f"{cluster_name} -> {path_model}")
    if path_model:
        path_model = os.path.join(input_folder, path_model)
    else:
        raise Exception(
            f"Model for celltype {cluster_name} not found in {input_folder}"
        )

    model = load_model(path_model)

    for versus_cluster_name in clusters:
        logging.info(f"Predicting on {versus_cluster_name} using {cluster_name} model")
        versus_cluster_data = read_val_set(input_folder, versus_cluster_name)

        metrics = predict_on_cluster(versus_cluster_data, model)
        # _ = versus_cluster_data["X"]
        y = versus_cluster_data["y"]
        f_sleep = round(y["1"].mean(), DIGITS)
        logging.info(f", % sleep: {f_sleep}")

        pair = (cluster_name, versus_cluster_name)
        metrics.update({"f_sleep": f_sleep})

        data.append((pair, metrics))
        print(f"Train on {pair[0]} and predict on {pair[1]}")
        for metric in metrics:
            print(f"  {metric}: {metrics[metric]}")

    return data


def predict(input_folder, background_path, ncores=1):
    """
    Evaluate a model already trained on one cell type across all cell types of its background
    and build a table for the model metrics which display the value of the metric for each combination of 
    train on and evaluated (predict) on

    Arguments:

        input_folder (str): Path to cached model and datasets
        background_path (str): Path to .csv with information about the name of the cell types belonging to the background


    Return:

        tables (dict): A dictionary where each key is a metric and each value is a dataframe with the value of the metric
        for each combination
    """
    background = pd.read_csv(background_path, index_col=False, comment="#")["cluster"].tolist()

    output = joblib.Parallel(n_jobs=ncores, verbose=10)(
        joblib.delayed(load_and_predict)(input_folder, background, cluster)
        for cluster in background
    )

    # TODO
    # This is highly likely to break. somehow change this code so it becomes more robust
    metrics=output[0][0][1]


    all_metrics = {metric: {cluster: {} for cluster in background} for metric in metrics}
    for i, full_comparison in enumerate(output):
        for pair in full_comparison:
            (cluster_name, versus_cluster_name), metrics = pair
            for metric in metrics:
                all_metrics[metric][cluster_name][versus_cluster_name] = metrics[metric]

    # pd.DataFrame creates a table out of a dict of dicts
    # the first level dicts become the columns
    # the second level dicts become the rows
    # therefore, the columns represent the cluster on which the model was trained
    # and the rows represent the clusters on which the model is tested

    ## TRAINED ON #
    ###############
    # R
    # U
    # N
    #
    # O
    # N
    ################
    tables={}
    for metric in all_metrics:
        tables[metric] = pd.DataFrame(all_metrics[metric]).T

    return tables
