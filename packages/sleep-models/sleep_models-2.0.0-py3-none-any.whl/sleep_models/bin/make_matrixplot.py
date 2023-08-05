import argparse
import os.path

import pandas as pd
import numpy as np

from sleep_models.plotting import make_matrix_from_array, make_matrixplot


def get_parser():
    ap = argparse.ArgumentParser()

    ap.add_argument(
        "--prediction-results",
        "--input",
        type=str,
        dest="prediction_results",
        help="Folder where the replicate data splits+train have been saved",
        required=True,
    )

    ap.add_argument(
        "--metric",
        type=str,
        dest="accuracy",
        help="Metric to use when rendering the matrixplot",
        choices=["accuracy", "recall", "f_sleep"],
        required=True,
    )

    ap.add_argument(
        "--barlimits",
        type=int,
        nargs="+",
        help="Minimum and maximum percent value of accuracy encompassed by the colorbar. Example: 50 70 will assign the lowest color to 50 percent acc and the highest to 70 percent. Everything above 70 or below 50 will look like 70 and 50, respectively.",
    )
    ap.add_argument(
        "--ignore-cell-types",
        dest="ignore_cell_types",
        type=str,
        nargs="+",
        default=None,
        help="""
        Cell types to ignore
        """,
    )
    return ap


def main(args=None):

    if args is None:
        ap = get_parser()
        args = ap.parse_args()

    make_matrixplot_main(
        args.prediction_results,
        metric=args.metric,
        barlimits=args.barlimits,
        ignore_cell_types=args.ignore_cell_types,
    )


def make_matrixplot_main(
    prediction_results, metric, barlimits=None, ignore_cell_types=None, save_results=None, **plotting_kwargs
):

    """
    Make a matrixplot using results saved to disk

    Arguments:

        * prediction_results (str): Path to a folder containing folders with an accuracy.csv file
        * ignore_cell_types (list): Celltypes to be ignored when constructing the matrixplot
        * plotting_kwargs (dict): Extra keyword arguments to sleep_models.plotting.make_matrixplot

    Returns:
        None
    """

    replicate_folders = os.listdir(prediction_results)
    replicate_folders = [f for f in replicate_folders if f.startswith("random-state")]

    results = {
        f: (
            pd.read_csv(
                os.path.join(prediction_results, f, f"{metric}.csv"), index_col=0,
            ),
            None,
        )
        for f in replicate_folders
    }
    for key in results:
        dataframe = results[key][0]
        if ignore_cell_types:
            for cell_type in ignore_cell_types:
                dataframe = dataframe.drop(cell_type, axis=0).drop(cell_type, axis=1)

        results[key] = (dataframe, *results[key][1:])

    clusters = results[list(results.keys())[0]][0].columns

    # make matrixplot
    replicates = np.stack([tables[0].values for tables in results.values()], axis=0)
    stat_values = {}
    for statistic in ["mean", "std"]:
        value = pd.DataFrame(getattr(replicates, statistic)(axis=0))
        value.index = list(results.values())[0][0].index
        value.columns = list(results.values())[0][0].columns
        value.to_csv(os.path.join(prediction_results, f"matrixplot_{metric}_{statistic}.csv"))
        stat_values[statistic] = value

    img = make_matrix_from_array(stat_values["mean"].values.copy())

    if save_results:
        filenames = tuple(
            os.path.join(prediction_results, f"matrixplot_{metric}_mean.{ext}")
            for ext in ["svg", "png"]
        )
    else:
        filenames = []


    return make_matrixplot(
        img,
        clusters,
        filenames=filenames,
        barlimits=barlimits,
        **plotting_kwargs,
    )


if __name__ == "__main__":
    main()
