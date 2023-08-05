from sklearn.decomposition import TruncatedSVD
from sklearn.manifold import TSNE
from umap import UMAP  # takes a while to load

ALGORITHMS = {
    TruncatedSVD.__name__: TruncatedSVD,
    UMAP.__name__: UMAP,
    TSNE.__name__: TSNE,
}
