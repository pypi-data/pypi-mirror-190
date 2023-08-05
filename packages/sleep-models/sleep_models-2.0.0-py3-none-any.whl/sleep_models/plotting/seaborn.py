import numpy as np
import warnings
from typing import Iterable

import matplotlib.pyplot as plt
import seaborn as sns



def make_matrixplot_sns(
    matrix: np.uint8,
    clusters: Iterable,
    filenames: Iterable[str],
    barlimits=None,
    dpi=72,
    rotation=(0, 0),
    palette="YlGnBu_r",
    metric="accuracy"
):

    plt.style.use('default')
    plt.rcParams["font.size"] = 22
    plt.set_cmap(palette)

    matrix = np.uint8(100 * np.float64(matrix) / 255)
    kwargs = {
        "data": matrix,
        "figsize": (5,5),
        "xticklabels": clusters,
        "yticklabels": clusters,
        "row_cluster": False,
        "col_cluster": False,
        "cmap": palette,
    }


    if barlimits is not None and len(barlimits) == 2:
        kwargs.update({"vmin": barlimits[0], "vmax": barlimits[1]})

    matrixplot=sns.clustermap(**kwargs)
    yaxis=matrixplot.figure.axes[0]
    bbox = np.array(yaxis.get_position())
    x, y, w, h = (1.15, bbox[0][1], 0.05, bbox[1][1]-bbox[0][1])
    matrixplot = sns.clustermap(**kwargs, cbar_pos=(x, y, w, h))

    metric = metric[0].upper() + metric[1:]
    matrixplot.ax_cbar.set_ylabel(metric)

    plt.setp(matrixplot.ax_heatmap.xaxis.get_majorticklabels(), rotation=rotation[0])
    plt.setp(matrixplot.ax_heatmap.yaxis.get_majorticklabels(), rotation=rotation[1])
    matrixplot.ax_heatmap.set_ylabel("Trained on")
    matrixplot.ax_heatmap.set_xlabel("Predicts  on")

    for f in filenames:
        matrixplot.savefig(f, transparent=True, dpi=dpi)#, bbox_inches="tight")

