import os.path
import warnings

import pandas as pd
from tqdm import tqdm
import joblib
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ranksums

from sleep_models.models import EBM
from sleep_models.utils.utils import load_pipeline_config
from sleep_models.explain import main as collect_results
from sleep_models.plotting import plot_gene_scores, plot_volcano_plots

config = load_pipeline_config()
statistical_test=ranksums
N_JOBS=4
RESULTS_FOLDER = config["results_dir"]
CELLTYPES={}
COUNTER=0
SECONDARY_TARGET = config.get("secondary_target", None)

for background_name in config["background"]:
    background = pd.read_csv(
        os.path.join(config["data_dir"], "backgrounds", f"{background_name}.csv"),
        index_col=0
    )
    CELLTYPES[background_name] = background.index.tolist()


def explain_shuffled_control(background, celltype, targets=None, shuffle=0):
    background=background + f"_shuffled_{shuffle}"

    explain_cell_type(background, celltype=celltype)
    if targets:
        for target in targets:
            explain_control(background, secondary_target=target)

def explain_cell_type(background, celltype):

    tables = []

    for random_state in config["seeds"]:

        ret, importance_table = load_model_results(background, random_state, target=None, celltype=celltype)
        if ret:

            save_results(celltype,importance_table,
                output=os.path.join(
                    RESULTS_FOLDER, f"{background}-train", "EBM",
                    f"random-state_{random_state}"
                )
            )
            tables.append(importance_table)

    arrs = []
    for table in tables:
        t=table.values
        t[np.isinf(t)] = np.nan
        arrs.append(t)

    mean_data = np.nanmean(np.stack(arrs), 0)
    importance_table=pd.DataFrame(mean_data, index=tables[0].index, columns=tables[0].columns)

    save_results(celltype, importance_table,
        output=os.path.join(
            RESULTS_FOLDER, f"{background}-train", "EBM",
        )
    )



def explain_control(background, secondary_target):

    print(background, secondary_target)

    for random_state in config["seeds"]:

        ret, importance_table = load_model_results(background, random_state, target=secondary_target)
        if ret:
            save_results(background, importance_table,
                output=os.path.join(
                    RESULTS_FOLDER, secondary_target, f"{background}-train", "EBM",
                    f"random-state_{random_state}"
                )
            )

def load_model_results(background, random_state, target = None, celltype=None):


    if celltype is None:

        assert target is not None

        model_path = f"{RESULTS_FOLDER}/{target}/{background}-train/EBM/random-state_{random_state}/{celltype}.joblib"
        X_train_path = f"{RESULTS_FOLDER}/{target}/{background}-train/EBM/random-state_{random_state}/{celltype}_X-train.csv"
        y_train_path = f"{RESULTS_FOLDER}/{target}/{background}-train/EBM/random-state_{random_state}/{celltype}_y-train.csv"

    else:
        model_path = f"{RESULTS_FOLDER}/{background}-train/EBM/random-state_{random_state}/{celltype}.joblib"
        X_train_path = f"{RESULTS_FOLDER}/{background}-train/EBM/random-state_{random_state}/{celltype}_X-train.csv"
        y_train_path = f"{RESULTS_FOLDER}/{background}-train/EBM/random-state_{random_state}/{celltype}_y-train.csv"

    if os.path.exists(model_path) and os.path.exists(X_train_path):

        ebm = joblib.load(model_path)
        X_train=pd.read_csv(X_train_path, index_col=0)
        y_train=pd.read_csv(y_train_path, index_col=0)
        ebm.name=celltype
        ebm.target=target


        ebm_global = ebm.explain_global()

        features=ebm_global.data()["names"]
        keep_genes=[i for i, feat in enumerate(features) if " x " not in feat]
        genes = np.array(X_train.columns)
        scores = np.array(ebm_global.data()["scores"])
        scores=scores[keep_genes]

        genes=genes[np.argsort(scores)][::-1]
        scores=scores[np.argsort(scores)][::-1]

        importance_table = pd.DataFrame.from_dict({
            "gene": genes,
            "S": scores,
            "log10S": np.log10(scores),
        },
            orient="columns",
        )

        importance_table.set_index("gene", inplace=True)

        # sort the columns of X_train according to the order of the genes in the importance table
        # and then pick only the cells belonging to one label.
        # Compute the mean expression, for each gene
        # and placeit in the importance table

        if celltype is not None:

            expression_by_label = {label: X_train[importance_table.index.values.tolist()][y_train["1"] == label].values for label in [0, 1]}
            mean_expression_by_label = {label: expression.mean(0) for label, expression in expression_by_label.items()}
            p_values = []

            for gene in tqdm(range(expression_by_label[0].shape[1]), desc="Running statistical tests"):
                _, p_val=statistical_test(
                    x=expression_by_label[1][:,gene],
                    y=expression_by_label[0][:,gene],
                    alternative="two-sided"
                )
                p_values.append(p_val)

            importance_table["mean_expression_0"] = mean_expression_by_label[0]
            importance_table["mean_expression_1"] = mean_expression_by_label[1]
            importance_table["FC"] = mean_expression_by_label[1] / mean_expression_by_label[0]
            importance_table["log2FC"] = np.log2(importance_table["FC"])
            importance_table["P"] = p_values
            importance_table["-log10P"] = -np.log10(importance_table["P"])


        return True, importance_table

    else:
        warnings.warn(f"{model_path} does not exist")
        return False, None


def save_results(celltype, importance_table, output):

    global COUNTER

    importance_table.to_csv(
        os.path.join(output, f"{celltype}_explanation.csv")
    )

    gene_scores=plot_gene_scores(importance_table, COUNTER)
    COUNTER+=1

    if "-log10P" in importance_table.columns:
        volcano_plots_p=plot_volcano_plots(importance_table, COUNTER, y = "-log10P")
        COUNTER+=1
    else:
        volcano_plots_p = None

    if "log2FC" in importance_table.columns:
        volcano_plots_sc=plot_volcano_plots(importance_table, COUNTER, y = "log10S")
        COUNTER+=1
    else:
        volcano_plots_sc=None

    for extension in [".png", ".svg"]:

        gene_scores.savefig(os.path.join(output, f"{celltype}_explanation{extension}"))

        if volcano_plots_p is not None:
            volcano_plots_p.savefig(os.path.join(output, f"{celltype}_volcano{extension}"))

        if volcano_plots_sc is not None:
            volcano_plots_sc.savefig(os.path.join(output, f"{celltype}_volcano_sc{extension}"))

    plt.close()


def main():

    # for background in CELLTYPES:
    #
    #     joblib.Parallel(n_jobs=N_JOBS)(
    #         joblib.delayed(
    #             explain_cell_type
    #         )(
    #             background, celltype
    #         ) for celltype in CELLTYPES[background]
    #     )

    #     joblib.Parallel(n_jobs=N_JOBS)(
    #         joblib.delayed(
    #             explain_shuffled_control
    #         )(
    #             background, celltype
    #         ) for celltype in CELLTYPES[background]
    #     )

    #     for shuffle in range(config["shuffles"]):

    #         shuffle_background = background + f"_shuffled_{shuffle}"
    #
    #         joblib.Parallel(n_jobs=N_JOBS)(
    #             joblib.delayed(
    #                 explain_control
    #             )(
    #                 shuffle_background, target
    #             ) for target in SECONDARY_TARGET
    #         )

    #     joblib.Parallel(n_jobs=N_JOBS)(
    #         joblib.delayed(
    #             explain_control
    #         )(
    #             background, target
    #         ) for target in SECONDARY_TARGET
    #     )

    collect_results(targets=SECONDARY_TARGET)


