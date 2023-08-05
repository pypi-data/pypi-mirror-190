import argparse
import os.path
import logging
import json
import pandas as pd
import numpy as np
import sleep_models.preprocessing as pp

def load_template(template_file):
    with open(template_file, "r") as fh:
        template = json.load(fh)
    return template
        

def get_parser(ap=None):

    if ap is None:
        ap = argparse.ArgumentParser()
        ap.add_argument(
            "--h5ad-input",
            type=str,
            dest="h5ad_input",
            help="Path to an h5ad file containing a serialized anndata.AnnData object",
            required=True,
        )
        ap.add_argument(
            "--h5ad-output",
            type=str,
            dest="h5ad_output",
            help="Path where the resulting anndata.AnnData object will be stored",
            required=True,
        )
        ap.add_argument(
            "--background",
            type=str,
            help="Path to a background file that specifies which cells are to be kept",
            required=True,
        )

        ap.add_argument(
            "--random-state",
            "--seed",
            type=int,
            help="Random seed to ensure reproducibility even in analyses involving stochastic processes (ex. UMAP or t-SNE)",
            required=True,
        )
        ap.add_argument(
            "--raw",
            dest="raw",
            action="store_true",
            help="Whether raw counts should be used in the analysis or not",
            default=True,
        )
        ap.add_argument(
            "--not-raw",
            dest="raw",
            action="store_false",
            help="Whether raw counts should be used in the analysis or not",
            default=True,
        )

        ap.add_argument(
            "--exclude-genes-file",
            type=str,
            dest="exclude_genes_file",
            help="tab separated file where the first column contains gene names to be discarded",
        )
        ap.add_argument(
            "--batch-genes-file",
            type=str,
            dest="batch_genes_file",
            help="DEPRECATED. Path to excel workbook with a sheet called all and a column called gene containing batch effect genes",
        )
        ap.add_argument(
            "--template-file",
            type=str,
            dest="template_file",
            help="YAML file linking classes in the target column of the AnnData (keys) to pseudo-labels (values)",
            required=False,
        )
        ap.add_argument(
            "--shuffles",
            type=int,
            default=0,
            dest="shuffles",
            help="How many random shuffles of the AnnData to perform",
        )

    return ap


def make_dataset(
    h5ad_input,
    h5ad_output,
    background,
    random_state,
    batch_genes_file=None,
    exclude_genes_file=None,
    template_file=None,
    shuffles=0,
    pinned_columns=[],
    raw=True,
    highly_variable_genes=False,
):

    """
    Filter an input anndata.Anndata object so only cells belonging to the given background are kept

    Optionally, this function can also
    
    - remove batch genes
    - merge labels into 'pseudo-labels'
    - store the raw counts matrix instead of the normalized counts
    - filter so only highly variable genes are kept
    - decouple the link between transcriptome and cell identity, i.e. shuffle, (to perform _in-silico_ controls)

    Arguments:

        h5ad_input (str): Path to an h5ad file containing a serialized anndata.AnnData object
        h5ad_output (str): Path where the resulting anndata.AnnData object will be stored
        background (str): Path to a background file that specifies which cells are to be kept
        random_state (int): Random seed to ensure reproducibility even in analyses involving stochastic processes (ex. UMAP or t-SNE)
        batch_genes_file (str): DEPRECATED. Path to excel workbook with a sheet called all and a column called gene containing batch effect genes 
        exclude_genes_file (str): tab separated file where the first column contains gene names to be discarded
        template_file (str): YAML file linking classes in the target column of the AnnData (keys) to pseudo-labels (values)
        shuffles (int): How many random shuffles of the AnnData to perform
        pinned_columns (list): Columns whose link to the transcriptome should be kept during the shuffling process (i.e. they are not shuffled)
        raw (bool): Whether raw counts should be used in the analysis or not
        highly_variable_genes (bool): Whether only highly variable genes should be used in the analysis or not.
            If True, and the AnnData.var contains a column called highly_variable, it is used to define what a HVG is,
            if the AnnData.var does not contain it, it is created on the spot using the function `scanpy.preprocessing.highly_variable_genes`

    Returns:
        None

    Side effects:
        An h5ad file under the path provided by h5ad_output is produced with the desired configuration
        Additionally, one more h5ad per desired shuffle is produced in the same folder and a suffix _shuffled_X
            where X is the shuffle number (starting at 0)

    """


    if template_file is None:
        template_filename = "notemplate"
    else:
        template_filename = os.path.basename(template_file)

    filename = (
        os.path.basename(background.strip(".csv")) + "-" + template_filename + ".h5ad"
    )

    np.random.seed(random_state)

    logging.info("Loading anndata to memory")
    adata = pp.load_adata(h5ad_input=h5ad_input, raw=raw, highly_variable_genes=highly_variable_genes)
    
    background_file = background
    background = pd.read_csv(background, index_col=False, comment="#")

    if template_file:
        template = load_template(template_file)
        adata = pp.template_matching(adata, template)


    bad_genes = pp.get_bad_genes(batch_genes_file, exclude_genes_file)
    adata = pp.remove_genes_from_list(adata, bad_genes)
    adata._uns.update({"background": background_file})

    adata = pp.keep_cells_from_this_background(adata, background)
    logging.info(f"Saving h5ad to disk at {h5ad_output}")
    adata.write_h5ad(h5ad_output)

    for i in range(shuffles):
        filename = h5ad_output.replace(".h5ad", f"_shuffled_{i}.h5ad")
        adata_shuffled = pp.shuffle_adata(
            adata, filename, pinned_columns=pinned_columns
        )


def main(args=None):

    if args is None:
        ap = get_parser()
        args = ap.parse_args()

    make_dataset(
        h5ad_input=args.h5ad_input,
        h5ad_output=args.h5ad_output,
        background=args.background,
        random_state=args.random_state,
        batch_genes_file=args.batch_genes_file,
        exclude_genes_file=args.exclude_genes_file,
        template_file=args.template_file,
        shuffles=args.shuffles,
        raw=args.raw,
    )


if __name__ == "__main__":
    main()
