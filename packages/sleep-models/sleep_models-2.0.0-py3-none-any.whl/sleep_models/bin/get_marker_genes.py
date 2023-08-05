import argparse
import os
import os.path
import sys
import glob

import sleep_models.dimensionality_reduction as dr
import sleep_models.preprocessing as pp
from sleep_models.dimensionality_reduction.algorithms import ALGORITHMS


def get_parser():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--h5ad-input",
        type=str,
        dest="h5ad_input",
        help=".h5ad with input adata",
        required=True,
    )
    ap.add_argument(
        "--output",
        type=str,
        help="Folder to which other output is saved",
        required=True,
    )
    ap.add_argument(
        "--algorithm",
        type=str,
        help="DR algoritm",
        choices=ALGORITHMS.keys(),
        required=True,
    )
    ap.add_argument(
        "--max-clusters",
        dest="max_clusters",
        help="""
        Genes are considered marker gene for the analysis
        if they are a marker gene of less than this number of clusters.
        For KC, 3 is a sensible default (3 different cell types)
        But for glia, which are many more cell types, it makes
        sense to choose a value under the number of cell types, like 5.
        This is not a typo. If a gene is a marker of many clusters of the background
        it is not differentiating between them! It is a marker of the background
        but not of the separate cell types
        """,
    )
    ap.add_argument("--ncores", default=1, type=int)
    ap.add_argument(
        "--thresholds",
        type=float,
        nargs="+",
        help="""
        absolute logFC thresholds to use
        when defining marker genes.
        Genes with a higher abs_logFC
        will be considered marker genes
        """,
    )

    return ap


def get_marker_genes(
    h5ad_input, marker_database, output, max_clusters, thresholds, algorithm=list(ALGORITHMS.keys()), cache=False
):

    f"""
    Detect genes which shape up the transcriptomic differences the most among the cell types in the dataset
    An a priori list of marker genes is needed for each cell type in the dataset, together with a quantification
    of how strong the gene is at differentiating the cell type (typically its fold change when comparing it to the rest of the dataset)
    This function takes different thresholds of this quantity and produces a dimensionality reduction plot of the dataset
    after removing genes in the marker database with a quantity higher than the threshold
    The plot informs us about how transcriptomically similar the cell types are, depending on how close they are on this transcriptomic space. 


    Please note that a gene may be a marker of a cell type when viewed in the context of the whole dataset (whole brain), but not in the context
    of a specific group of celltypes (background), for example within only Kenyon Cells or within glia only. This is why max_clusters is implemented

    Cells belonging to the same cell type are annotated as such because their corresponding label in the CellType column of the AnnData obs DataFrame is the same


    Arguments

        h5ad_input (str): Path to an h5ad file containing a serialized anndata.AnnData object
        marker_database (str): Path to a marker database, a folder with tsv files where each file follows the naming scheme CELLTYPE.csv
           and it contains tab separated columns gene and avg_logFC

           Example:
              gene	avg_logFC	pval
              pros	3.196108341217041	0.0
              CG42784	2.399651050567627	0.0

        max_clusters (int): if a gene is marker of this amount of clusters or more, it is not discarded 
        output (str): Folder under which the output of the function is stored. For each passed threshold, a folder called threshold-X
        is created containing:

            marker_genes.txt: A plain text file with one gene per line and no header. These are the genes with a logFC greater than the threshold
            ALGORITHM_embedding.pkl: A pickle file caching the embedding produced in the dimensionality reduction
            png/: A folder with 2 dimensionality reduction plots produced using the desired algorithm. One contains TODO
        
        thresholds (list): List of logFC values to be used as separators between an effective marker gene (higher) or not (lower)
        algorithm (str): One of the supported algorithms {list(ALGORITHMS.keys())}
        cache (bool): Whether to cache the embedding to a pkl file or not
    
    See also:

        sleep_models.dimensionality_reduction.SingleCellEmbedding

    """
    ncores=1

    os.makedirs(output, exist_ok=True)

    # load the data
    adata = pp.read_h5ad(h5ad_input)
    cell_types = list(set(adata.obs["CellType"].values.tolist()))

    # load the marker database for all celltypes
    column="avg_logFC"
    markers = dr.get_markers(cell_types, marker_database, column=column, postprocess_function="abs")

    background = os.path.basename(h5ad_input).rstrip("h5ad")
    name = background + f" {column} < " + "%s"

    # generate the initial DR
    embedding = dr.SingleCellEmbedding.analysis(
        adata=adata,
        root_fs=output,
        markers=markers,
        algorithm=algorithm,
        max_clusters=max_clusters,
        threshold=None,
        reducer=None,
        normalize=True,
        name=name,
        limits=None,
        cache=cache,
    )

    # for each threshold reproject onto the existing embedding
    # compute the distances and the silhouette
    dr.homogenize(
        output=output,
        adata=adata,
        reducer=embedding.reducer,
        markers=markers,
        thresholds=thresholds,
        max_clusters=max_clusters,
        ncores=ncores,
        name=name,
        cache=cache,
        limits=embedding._limits,
    )

    return 0


def main(args=None):

    if args is None:
        ap = get_parser()
        args = ap.parse_args()

    get_marker_genes(
        h5ad_input=args.h5ad_input,
        max_clusters=args.max_number_of_clusters_per_marker_gene,
        thresholds=args.thresholds,
        algorithm=args.algorithm,
        output=args.output,
    )


if __name__ == "__main__":
    main()
