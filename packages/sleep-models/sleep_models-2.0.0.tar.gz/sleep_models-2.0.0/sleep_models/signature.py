import os.path
import pickle
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from loess.loess_1d import loess_1d
import joblib
import shap

import sleep_models.preprocessing as pp
from sleep_models.utils.data import sort_celltypes


def plot_log_odds(log_odds, feature):
    log_odds = log_odds[:, feature]
    x = log_odds.data
    y = log_odds.values
    data = list(zip(x, y))
    data = sorted(data, key=lambda x: x[0])
    x_sorted = np.array([e[0] for e in data])
    y_sorted = np.array([e[1] for e in data])
    xout, yout, wout = loess_1d(x_sorted, y_sorted)
    plt.scatter(x_sorted, y_sorted)
    plt.plot(xout, yout, label=feature)



def get_celltypes(h5ad_input, celltype_column):
    cache_file = "all_celltypes.txt"
    if os.path.exists(cache_file):
        with open("all_celltypes.txt", "r") as filehandle:
            celltypes = [e.strip("\n") for e in filehandle.readlines()]    
    else:
        adata=pp.load_adata(h5ad_input)
        celltypes = set(adata.obs[celltype_column].tolist())
        celltypes = sort_celltypes(celltypes)
        celltypes.append("Bulk")

        with open(cache_file, "w") as filehandle:
            for celltype in celltypes:
                filehandle.write(f"{celltype}\n")
    
    return celltypes


def read_val_set(results_dir, celltype, arch, seed):
    return pd.read_csv(
        os.path.join(
            get_result_folder(results_dir, celltype, arch, seed),
            f"{celltype}_X-val.csv"
        ),
    index_col=0)


def get_signature_file(results_dir, celltype, arch, seed):
    return os.path.join(
            get_result_folder(results_dir, celltype, arch, seed),
            f"{celltype}_signature.csv"
        ) 

def get_result_folder(results_dir, celltype, arch, seed):
    return os.path.join(
            results_dir,
            f"{celltype}-train",
            arch,
            f"random-state_{seed}"
        )

def load_model(results_dir, celltype, arch, seed):
    if arch == "RF":
        model_file = os.path.join(
            get_result_folder(results_dir, celltype, arch, seed),
            f"{celltype}.pickle"
        )

        with open(model_file, "rb") as filehandle:
            model = pickle.load(filehandle)

        model.target = model._target
    
    elif arch == "EBM":
        model_file = os.path.join(
            get_result_folder(results_dir, celltype, arch, seed),
            f"{celltype}.joblib"
        )
        model = joblib.load(model_file)
    return model


def compute_celltype_stats(results_dir, celltype, arch, seed):

    stats = {"celltype": celltype, "arch": arch, "seed": seed}
    confusion_table_path = os.path.join(
        get_result_folder(results_dir, celltype, arch, seed),
        f"{celltype}_confusion_table.csv"
    )

    if os.path.exists(confusion_table_path):
        confusion_table = pd.read_csv(confusion_table_path, index_col=0)
        acc = compute_accuracy(confusion_table)
        tp = compute_true_positives(confusion_table)
        tn = compute_true_negatives(confusion_table)
        fp = compute_false_positives(confusion_table)
        fn = compute_false_negatives(confusion_table)

        size = compute_size(confusion_table)
        stats.update({"acc": acc, "tp": tp, "tn": tn,  "fp": fp, "fn": fn, "size": size})
    else:
        stats.update({"acc": np.nan, "tp": np.nan, "tn": np.nan, "fp": np.nan, "fn": np.nan, "size": np.nan})
        
    return stats


def plot_performance(data, x, y):
    data=data.drop("Bulk", axis=0)
    data.sort_values(x, inplace=True)
    x = data[x].values
    y = data[y].values
    xout, yout, wout = loess_1d(x, y)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x, y)
    ax.plot(xout, yout, color="black")
    ax.set_ylim([0.5, math.ceil(y.max() * 10) / 10])
    
def compute_accuracy(confusion_table):
    return np.diag(confusion_table.values).sum() / confusion_table.values.sum()

def compute_true_positives(confusion_table):
    return confusion_table["Sleep"].loc["Sleep"]

def compute_true_negatives(confusion_table):
    return confusion_table["Wake"].loc["Wake"]

def compute_false_positives(confusion_table):
    return confusion_table["Wake"].loc["Sleep"]
def compute_false_negatives(confusion_table):
    return confusion_table["Sleep"].loc["Wake"]

def compute_size(confusion_table):
    return confusion_table.values.sum()

                   
    
def get_summary_table(results_dir, celltypes, architectures, seeds):
    stats = []
    for celltype in celltypes:
        for arch in architectures:
            for seed in seeds:
                stats.append(
                    compute_celltype_stats(results_dir, celltype=celltype, arch=arch, seed=seed)
                )
    stats_df = pd.DataFrame.from_records(stats)
    stats_df["sensitivity"] = stats_df["tp"] / (stats_df["tp"] + stats_df["fn"])
    stats_df["specificity"] = stats_df["tn"] / (stats_df["tn"] + stats_df["fp"])
    stats_df=stats_df.loc[~pd.isna(stats_df).any(1)]
    stats_df["pass"] = (stats_df[["acc", "specificity", "sensitivity"]] > 0.5).all(axis=1).values
    stats_df=stats_df.loc[stats_df["pass"]]
    # the last reset index there is to keep the first entry in case of tie
    stats_df=stats_df.groupby("celltype").apply(lambda t: t[t.acc==t.acc.max()].iloc[0])
    stats_df.reset_index(drop=True, inplace=True)
    stats_df.sort_values("acc", ascending=False, inplace=True)
    stats_df.set_index("celltype", inplace=True)

    return stats_df


def compute_signature(model, data, f="predict", sample_size=100):
    X_sample = data.sample(min(data.shape[0], sample_size))
    genes=data.columns.tolist()
    explainer = shap.Explainer(getattr(model, f), X_sample)
    shap_values = explainer(X_sample, max_evals=3000)

    shap_stats = {}

    for feature in genes:
        feature_values = shap_values[:, feature].values
        diff = np.abs(feature_values.min() - feature_values.max())
        std = np.std(np.abs(feature_values))
        # shap_diff[feature] =  {"diff": diff, "std": std, "mean": shap_values.abs.max(0).mean(0)}
        shap_stats[feature] = {"diff": diff, "std": std, "mean": np.abs(feature_values).mean()}

    shap_stats=pd.DataFrame(shap_stats).T    
    shap_stats.sort_values("mean", ascending=False, inplace=True)
    # the top 10  genes on this plot
    # are the same top 10 genes in shap_stats when sorting by mean
    # shap.plots.bar(shap_values)
    return shap_stats, shap_values
