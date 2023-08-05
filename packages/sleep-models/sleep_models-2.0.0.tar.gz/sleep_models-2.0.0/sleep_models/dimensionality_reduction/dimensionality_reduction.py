import time
import warnings
import os.path
import logging
import pickle
import itertools

import numpy as np
import pandas as pd
from tqdm import tqdm
from joblib import Parallel, delayed
from sklearn.metrics import silhouette_score


from sleep_models.plotting import make_dr_plot, plot_homogenization

from .algorithms import ALGORITHMS
MARKER_GENES_FILE="marker_genes.txt"

logger = logging.getLogger(__name__)

class SingleCellEmbedding:
    """
    Select the marker genes for a given threshold
    and run a DR algorithm on the dataset resulting
    from setting the counts of these genes to 0
    
    Arguments:

        * output (str): In this folder, a new folder called threshold-X will be created
            with the results of this function
        * adata (anndata.AnnData): Single cell dataset
        * markers (pd.DataFrame): Marker genes of the background with columns
                gene quantity cluster
        * max_clusters (int): A marker gene shared among this number of clusters or more is not considered
          a marker gene anymore
        * threshold (float): A logFC threshold to consider actual marker genes
        * normalize (bool): If True, the embedding is centered around 0
    
    Returns:
    """

    def __init__(
        self,
        adata,
        root_fs,
        markers,
        max_clusters,
        threshold,
        name,
        algorithm,
        limits=None,
        cache=False,
        reducer=None,
        normalize=True,
        **kwargs
    ):
        self.adata = adata
        self.root_fs = root_fs
        if reducer is None:
            reducer = get_dr_algorithm(algorithm)
            self.algorithm = algorithm
            self._fit = True
        else:
            self.algorithm = reducer.__class__.__name__
            self._fit = False

        self.reducer = reducer
        self.threshold = threshold
        self.max_clusters = max_clusters
        self.name = name
        self.normalize = normalize
        self.output_folder = os.path.join(self.root_fs, f"threshold-{self.threshold}")
        self._marker_genes_raw = markers

        self._count_matrix = None
        self._marker_genes = None
        self._embedding = None
        self._centers = None
        self._center_pairs = None
        self._pair_distance = None
        self._cache = cache
        self._limits = limits

        self._embedding_file = os.path.join(
            self.output_folder, f"{algorithm}_embedding.pkl"
        )
        self._genes_file = os.path.join(self.output_folder, MARKER_GENES_FILE)
        self.project_memo(**kwargs)


    def save_dr_plot(self, fig, prefix=""):
        filenames = [
            os.path.join(
                self.output_folder,
                "png",
                f"{self.algorithm}{prefix}_threshold-{self.threshold}.png",
            ),
            os.path.join(
                self.output_folder,
                "svg",
                f"{self.algorithm}{prefix}_threshold-{self.threshold}.svg",
            ),
        ]

        for filename in filenames:
            fig.savefig(filename)


    @classmethod
    def analysis(cls, *args, **kwargs):
        f"""
        Perform the projection of the dataset to a 2D transcriptomic space
        Arguments:
            See arguments to SingleCellEmbedding

        Returns
            embedding (SingleCellEmbedding): Object containing:
                1. the reducer used to perform the 2D projection (embedding.reducer)
                2. the threshold used to filter the genes (embedding.threshold)
                3. the resulting count matrix after applying the filter (embedding.count_matrix)
                4. the remaining marker genes after filtering (embedding.marker_genes)

        
        Side effects:
            Save the DR (2D) plots
            
                1. in the original resolution of the first time the reducer was obtained
                   (to compare across different filtering criteria)
                2. in a dynamic resolution based on the data (zoomed in)

            Save the list of filtered marker genes ({MARKER_GENES_FILE})
        """

        embedding = cls(*args, **kwargs)

        # embedding._limits is None the first time this function is called
        # just after initializing embedding
        # But the attribute is populated just now, which means
        # future calls will use a constant limit
        # This way the limits stay the same (even if the dataset is not because is filtered)
        fig, ax = embedding.draw_dr_plot(limits=embedding._limits)
        embedding.save_dr_plot(fig)

        if embedding._limits is None:
            embedding._limits = (ax.get_xlim(), ax.get_ylim())

        # limits None means the limits are computed on the spot
        # based on the coordinates of the embedding
        # i.e. the limits in this zoomin version are dynamic
        fig, ax = embedding.draw_dr_plot(limits=None)
        embedding.save_dr_plot(fig, prefix="zoomin")
        return embedding

    @property
    def embedding(self):
        return self._embedding

    @property
    def count_matrix(self):
        """
        Read the counts in the adata for the marker genes only

        See property marker_genes to know how they are selected, namely:

            * number of clusters in which the gene is a marker gene
            * strength or quantity of the marker (logFC in cell type vs all comparison)
        """
        
        if self._count_matrix is None:
            count_matrix = non_marker_genes_data(self.adata, self.marker_genes)
            self._count_matrix = count_matrix

        return self._count_matrix

    @property
    def marker_genes(self):
        return self._marker_genes

    @marker_genes.getter
    def marker_genes(self):
        if self._marker_genes is None:
            self._marker_genes = self.select_marker_genes(
                # the original table with all marker genes of the background, no filter applied
                self._marker_genes_raw,
                # marker genes of this number of clusters or more are still kept
                max_clusters=self.max_clusters,
                # marker genes with a strength under this are also kept
                threshold=self.threshold,
            )
        return self._marker_genes

    @marker_genes.setter
    def marker_genes(self, value):
        self._marker_genes = value


    @staticmethod
    def select_marker_genes(markers, threshold, max_clusters):
        """
        Arguments:
            markers (pd.DataFrame): Marker genes of the background with columns
                gene quantity cluster
            threshold (float): marker genes with a logFC under this value will not be treated as marker genes
            max_clusters (int): if a gene is marker of this amount of clusters or more, it is not discarded 
        Returns:
            genes (list): each entry is the name of a marker gene with a logFC above the passed threshold
        """

        counts = pd.DataFrame(markers["gene"].value_counts())
        counts.columns = ["count"]

        # NOTE This line of code is critical
        # This is where we decide which genes are considered marker genes
        # and which ones are not

        # A marker gene is any gene appearing in less than max_clusters
        # If it appears on max_clusters or more, it means it is a marker for many clusters
        # so it does not "differentiate so much between them"
        # It could actually be that it's a marker of each cluster separately
        # and it still looks different across them too
        # However, for most marker genes it is a fair assumption
        # and in the case of the assumption being wrong, it is only making our analysis
        # more stringent

        counts["marker"] = counts["count"] < max_clusters
        ##########################################################################
        marker_genes = counts.index[counts["marker"]].tolist()
        keep = [gene in marker_genes for gene in markers["gene"]]
        markers = markers.loc[keep]
        markers = markers.sort_values("quantity", ascending=False)  # decreasing

        if threshold is None:
            # assume None means infinite i.e. no marker gene actually
            genes = []
        else:
            try:
                markers = markers.loc[markers["quantity"] > threshold]
            except Exception as error:
                print(error)
                raise error
            genes = markers["gene"].tolist()
        return genes

    @property
    def pair_distance(self):
        return self._pair_distance

    @property
    def silhouette(self):
        return silhouette_score(self._embedding, self.adata.obs["CellType"])

    def restore_from_cache(self):

        with open(self._embedding_file, "rb") as fh:
            embedding = pickle.load(fh)

        with open(self._genes_file, "r") as fh:
            marker_genes = [fh.readline()]

        return embedding, marker_genes

    def project(self):
        """
        Produce an embedding for the object's count matrix
        using the algorithms in ALGORITHMS
        and an existing projection (stored in the self.reducer object)
        """
        self._embedding = run_reducer(self.reducer, self.count_matrix, fit=self._fit)

        # center the embedding
        if self.normalize:
            self._embedding -= self._embedding.mean(axis=0)


    def draw_dr_plot(self, **kwargs):
        
        if self.threshold is None:
            title = "All genes"
        else:
            title = f"log2FC < {self.threshold}"


        return make_dr_plot(
            embedding=self._embedding,
            adata=self.adata,
            centers=self._centers,
            center_pairs=self._center_pairs,
            distances=self.pair_distance,
            output=self.output_folder,
            title=title,
            marker_genes=self.marker_genes,
            **kwargs,
        )

    def project_memo(self, progress=None):
        
        """
        Project all cells in the dataset into a new space with reduced dimensions
        
        Moreover:
        
            - compute the coordinates of the center of each cluster in the new reduced space
            - compute the distance between each center

        The center of a cluster is the mean value of the X and Y coordinates of each cell of the cluster in the projected space 
        """

        # cache becomes None if there is not cache or the embedding results if they exist
        cache = self.check_cache()

        # load from cache
        if self._cache and cache is not None:
            if progress is not None:
                progress.set_description(f"Loading from cache {self._embedding_file}")
            self._embedding = cache[0]

        # actually project
        else:
            if progress is not None:
                progress.set_description(f"Computing {self.algorithm} at threshold = {self.threshold}")
            os.makedirs(self.output_folder, exist_ok=True)
            self.project()
            if progress is not None:
                progress.update(1)
            self.update_cache()

        self.compute_centers()
        self.compute_center_pairs()
        self.compute_distances()


    def compute_centers(self):
        """
        Populate self._centers
        """

        self._centers = {}
        cell_types = self.adata.obs["CellType"].unique()

        for cell_type in cell_types:

            x = self._embedding[np.where(self.adata.obs["CellType"] == cell_type), 0]
            y = self._embedding[np.where(self.adata.obs["CellType"] == cell_type), 1]

            c = (x.mean(), y.mean())
            self._centers[cell_type] = np.array(c)


    def compute_center_pairs(self):
        """
        Populate self._centers_pairs
        """
        
        assert self._centers is not None
        self._center_pairs = list(itertools.combinations(self._centers, 2))

    def compute_distances(self):
        """
        Populate self._pair_distance
        """

        self._pair_distance = {}

        for c1, c2 in self._center_pairs:
            dist = round(
                np.sqrt(np.sum((self._centers[c1] - self._centers[c2]) ** 2)), ndigits=2
            )
            self._pair_distance[(c1, c2)] = dist

    def check_cache(self):
        """
        Look for a cache file and if it exists, load and return it
        """

        if (
            os.path.exists(self.output_folder)
            and os.path.exists(self._embedding_file)
            and os.path.exists(self._genes_file)
        ):
            logger.info(f"threshold {self.threshold} already done")
            return self.restore_from_cache()
        else:
            return None

    def update_cache(self):
        with open(self._embedding_file, "wb") as fh:
            pickle.dump(self._embedding, fh)

        with open(self._genes_file, "w") as fh:
            for gene in self.marker_genes:
                fh.write(gene + "\n")


def get_markers(cell_types, marker_database=None, column="avg_logFC", postprocess_function="abs"):
    """
    Arguments:
        cell_types (list): cell types whose markers should be loaded
        marker_database (str): path to folder with .tsv files
        column (str): Name of column on each .tsv file containing the strength of the marker
        postprocess_function (str): Function to be applied to the strength, if any. Must be implemented in numpy
    Returns:
        markers (pd.DataFrame): Marker genes of the background with columns
           gene quantity cluster
        where every row belongs to a gene that is a marker of up to max_clusters-1 clusters

    Detail:
       No filtering is applied in this step
    """

    markers = {}

    # concatenate all markers in the background
    for cell_type in cell_types:
        cluster_markers = pd.read_csv(
            os.path.join(marker_database, f"{cell_type}.tsv"), sep="\t"
        )
        assert column in cluster_markers.columns, f"Please ensure {column} is available in the marker_database for cell type {cell_type}"
        cluster_markers["quantity"] = cluster_markers[column]
        cluster_markers.drop(column, axis=1, inplace=True)
        if postprocess_function is not None:
            cluster_markers["quantity"]=getattr(cluster_markers["quantity"], postprocess_function)()

        cluster_markers["cluster"] = cell_type
        markers[cell_type] = cluster_markers
    markers = pd.concat(markers.values())
    return markers


def non_marker_genes_data(adata, marker_genes):
    """
    Arguments:
        * adata (anndata.AnnData): Single cell dataset where .X is np.ndarray
        * marker_genes (list): marker gene names

    Returns
        * gene_data (np.array) the matrix of counts
        where the marker gene count is set to null_value (0),
        (so it's like they are not observed)
    """
    assert isinstance(adata.X, np.ndarray)


    # null_value: should always be zero
    null_value = 0

    gene_data = adata.X.copy()
    index = [g in marker_genes for g in adata.var.index]

    if len(index) != 0:
        gene_data[:, index] = null_value
    return gene_data


def get_dr_algorithm(algorithm):
    """
    Initialize the requested DR algorithm
    """
    assert algorithm in ALGORITHMS, f"Please pass a valid algorithm: {list(ALGORITHMS.keys())}"
    reducer = ALGORITHMS[algorithm]()
    return reducer


def run_reducer(reducer, data, fit=True):

    """
    Arguments:
        * reducer (instance of one of the classes in ALGORITHMS).
            An instance of a DR algorithm with methods transform and fit_transform
        * data (np.ndarray): shape cells x genes storing gene counts
        * fit (bool): If True, a new embedding is computed prior to the projection,
            otherwise, we just projecting onto the existing embedding
            If the algorithm does not support fitting without transform, a warning is issued
            and the program fits and transforms i.e. forces fit=True.
    
    Returns:
        * embedding (np.ndarray): Projection of the cell data onto a dimensionally reduced space

    Calls either transform or fit_transform method of the DR algorithm instance with the passed dataset
    This is useful if you want to project different datasets on to the same space (fit=False)
    or not i.e. separate datasets get different projection spaces
    A projection space is generated by calling fit
    """

    before = time.time()
    if fit:
        embedding = reducer.fit_transform(data)
    else:
        f = getattr(reducer, "transform", None)
        if f is None:
            warnings.warn(
                f"""
                {reducer} has no transform method available.
                Using fit_transform -> this means the embedding will be recomputed,
                which means you cannot compare the exact position of the same cell
                across different plots. However, it is still a valid DR plot            
                """

            )
            f = getattr(reducer, "fit_transform")
        embedding = f(data)
    after=time.time()

    print(f"Done in {after-before} seconds")

    return embedding


def get_embeddings(
    output,
    adata,
    reducer,
    markers,
    max_clusters,
    thresholds,
    limits,
    algorithm=None,
    name="DR",
    ncores=1,
    cache=False,
):
    f"""
    Compute the embedding and projection resulting from
    removing all marker genes with a defined marker strength greater than the threshold

    The embedding is computed using the passed algorithm / reducer
    The plot is saved in the output folder
    The data is taken from the adata and markers variables


    Arguments

        output (str): Folder where the results are stored, does not have to exist
        adata (anndata.AnnData): Single cell dataset with only cells from a particular background
        (a group of cell types with similar properties, example: Kenyon Cells, glia, etc)
        reducer (instance of one of the classes in {list(ALGORITHMS.keys())}).
            An instance of a DR algorithm with methods transform and fit_transform.
            If not None, the embedding obtained previously and stored in this variable is reused, so only a reprojection is performed
        algorithm (str): One of the algorithms in {list(ALGORITHMS.keys())} if reducer is not provided
        markers (pd.DataFrame): Marker genes of the background with columns
                gene quantity cluster
        max_clusters (int): Genes that were an original marker gene of this number of clusters (cell types), are kept and not filtered out
        thresholds (list): Each of the values here will be used to filter the raw marker genes and produce a dataset of more and more similar cell types
            the lower this value becomes (because the more differentiating genes become filtered out)
        limits (tuple): None or a tuple of tuples with the min and max value of x and y coordinates on the projection plot
        ncores (int): How many jobs to spawn in parallel to speed up the computation for each threshold


    Returns
        results (dict): For each threshold (key), the value is an instance of an SingleCellEmbedding class

    Side effect:
        See side effect of SingleCellEmbedding.analysis
    """

    pbar = tqdm(thresholds)


    if algorithm is None:
        algorithm=reducer.__class__.__name__
        if reducer is None:
            raise Exception(f"Please pass an algorithm if no reducer is provided. Options {ALGORITHMS}")
    elif reducer is not None:
        warnings.warn(f"The pased algorithm will be ignored. The passed reducer will be used instead")


    if ncores == 1:
        results = {}
        for threshold in thresholds:
            # https://stackoverflow.com/a/45519268/3541756
            results[threshold] = SingleCellEmbedding.analysis(
                root_fs=output,
                adata=adata,
                reducer=reducer,
                algorithm=algorithm,
                markers=markers,
                max_clusters=max_clusters,
                threshold=threshold,
                name=name,
                cache=cache,
                limits=limits,
                progress=pbar,
            )

    else:
        parallel_output = Parallel(n_jobs=ncores)(
            delayed(SingleCellEmbedding).analysis(
                root_fs=output,
                adata=adata,
                reducer=reducer,
                algorithm=algorithm,
                markers=markers,
                max_clusters=max_clusters,
                threshold=threshold,
                name=name,
                cache=cache,
                limits=limits,
            )
            for threshold in thresholds
        )
        results = {
            threshold: parallel_output[i] for i, threshold in enumerate(thresholds)
        }

    return results


def homogenize(adata, output, reducer, **kwargs):
    
    f"""
    Mix-up the cells in-silico by removing marker genes more and more aggressively at increasing marker thresholds
    and compute stats about how the process evolves through the thresholds

    Arguments

        output (str): Folder on which to save the results
        reducer (DR algorithm): Instance of one of the models in {ALGORITHMS}


    Side effect:
            1. See side effect of SingleCellEmbedding.analysis
            2. See side effecto of plot_homogenization

    """

    algorithm = reducer.__class__.__name__

    single_cell_embeddings = get_embeddings(output=output, adata=adata, reducer=reducer, **kwargs)
    benchmark = benchmark_homogenization(output, single_cell_embeddings)
    plot_homogenization(
        output, adata, single_cell_embeddings, benchmark, algorithm=algorithm
    )


def benchmark_homogenization(output, single_cell_embeddings):

    algorithm = list(single_cell_embeddings.values())[0].algorithm

    distances = {
        threshold: single_cell_embeddings[threshold].pair_distance
        for threshold in single_cell_embeddings
    }

    dfs = []
    i = 0
    for threshold, dists in distances.items():

        d = {"-".join(k): v for k, v in dists.items()}
        df = pd.DataFrame(d, index=[i])
        df["silhouette"] = single_cell_embeddings[threshold].silhouette
        df["logFC"] = threshold

        dfs.append(df)
        i += 1

    benchmark = pd.concat(dfs).sort_values("logFC").loc[::-1, :]
    benchmark.to_csv(os.path.join(output, f"{algorithm}_benchmark.csv"))
    return benchmark
