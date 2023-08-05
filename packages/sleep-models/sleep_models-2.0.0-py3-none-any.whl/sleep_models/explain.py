import warnings
import os.path
from functools import reduce
import pandas as pd
from sklearn.utils import shuffle

CELLTYPES={}
COUNTER=0
from sleep_models.utils.utils import load_pipeline_config

config = load_pipeline_config()


def read_explanation_for_celltype(background, celltype, target=None, shuffle=None, seeds=None, results_dir=None):

    if results_dir is None:
        results_dir = config["results_dir"]


    explanations={}
    if shuffle == None:
        background_folder = f"{background}-train"
    else:
        background_folder = f"{background}_shuffled_{shuffle}-train"


    if seeds is None:
        seeds = config["seeds"]

    for seed in seeds:
        if celltype is None:
            assert target is not None
            if shuffle is None:
                filename = f"{background}_explanation.csv"
            else:
                filename = f"{background}_shuffled_{shuffle}_explanation.csv"

            explanation_path = os.path.join(results_dir, target, background_folder, "EBM", f"random-state_{seed}", filename)
        else:
            if shuffle is None:
                filename = f"{celltype}_explanation.csv"
            else:
                filename = f"{celltype}_shuffled_{shuffle}_explanation.csv"

            explanation_path = os.path.join(results_dir, background_folder, "EBM", f"random-state_{seed}", f"{celltype}_explanation.csv")

        if not os.path.exists(explanation_path):
            warnings.warn(f"{explanation_path} does not exist", stacklevel=2)
            return

        explanations[seed]=pd.read_csv(explanation_path, index_col=0)

    if shuffle == 0 and background == "glia" and target == "CellType":
        import ipdb; ipdb.set_trace()

    explanation=reduce(
        lambda x, y: x + y.loc[x.index]
        , list(explanations.values())

    )

    explanation /= len(seeds)
    return explanation


def read_explanation_all(celltypes, targets, **kwargs):
    explanations={}

    for background in celltypes:

        explanations[background] = {}
        for celltype in celltypes[background]:
            explanations[background][celltype] = read_explanation_for_celltype(background, celltype, **kwargs)

        for target in targets:
            explanations[background][target] = read_explanation_for_celltype(background, None, target=target, **kwargs)

    return explanations


def make_datasets(celltypes, explanations, differential_data=True):
    datasets={}
    for background in celltypes:
        for celltype in explanations[background]:

            if explanations[background][celltype] is None:
                continue

            if differential_data and not celltype in config["secondary_target"]:
                columns=[
                    (celltype, "S"),
                    (celltype, "log10S"),
                    (celltype, "mean_expression_0"),
                    (celltype, "mean_expression_1"),
                    (celltype, "FC"),
                    (celltype, "log2FC"),
                    (celltype, "P"),
                    (celltype, "-log10P"),
                ]

            else:
                columns=[
                    (celltype, "S"),
                    (celltype, "log10S"),
                ]

            multindex=pd.MultiIndex.from_tuples(
                columns,
                names=["celltype", "feature"]
            )
            explanations[background][celltype].columns=multindex

        explanations_clean = {
            background: {
                celltype: explanations[background][celltype]
                for celltype in explanations[background]
                if explanations[background][celltype] is not None
            }
            for background in explanations
        }

        explanations = explanations_clean

        background_dataset = reduce(
            lambda  left,right: pd.merge(
                left,right,
                left_index=True, right_index=True
            ),
            list(explanations[background].values())
        )

        datasets[background]=background_dataset

    return datasets


def main(targets):


    for background_name in config["background"]:
        background = pd.read_csv(
            os.path.join(config["data_dir"], "backgrounds", f"{background_name}.csv"),
            index_col=0
        )

        CELLTYPES[background_name] = background.index.tolist()

    explanations = read_explanation_all(CELLTYPES, targets=targets)
    for shuffle in range(config["shuffles"]):
        explanations_shuffled_ = read_explanation_all(CELLTYPES, targets=targets, shuffle=shuffle)
        explanations_shuffled = {f"{k}_shuffled_{shuffle}": explanations_shuffled_[k] for k in explanations_shuffled_}
        explanations.update(explanations_shuffled)

    celltypes = list(CELLTYPES.keys())
    for shuffle in range(config["shuffles"]):
        for background in CELLTYPES:
            celltypes.append(f"{background}_shuffled_{shuffle}")

    datasets = make_datasets(celltypes, explanations)
    for background in datasets:
        celltypes=sorted(set(datasets[background].columns.get_level_values("celltype")))
        excel_file = os.path.join(config["results_dir"], f"{background}-train", "EBM", f"{background}_explanation.xlsx")
        print(excel_file)
        with pd.ExcelWriter(excel_file) as writer:
            for celltype in celltypes:
                datasets[background][celltype].sort_values("log10S")[::-1].to_excel(writer, sheet_name=celltype)

