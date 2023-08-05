import os.path

import pandas as pd
import numpy as np
import joblib

def load_model(results_dir, model_name, background, celltype, seed):
    
    # load the gene expression matrix and get the gene names
    X_train_path = f"{results_dir}/{background}-train/{model_name}/random-state_{seed}/{celltype}_X-train.csv"
    X_train=pd.read_csv(X_train_path, index_col=0)
    genes = np.array(X_train.columns)
    del X_train

    # Load the model, which contains the weights but not the gene name
    # feature_001 is the first gene in the expression matrix, and so on
    model_path = os.path.join(results_dir, f"{background}-train/{model_name}/random-state_{seed}", f"{celltype}.joblib")
    ebm = joblib.load(model_path)
    ebm.name=celltype
    ebm.target="Treatment"
    return ebm, genes
    
def explain_model(ebm, genes):
    # extract the weights
    ebm_global = ebm.explain_global()

    
    features=ebm_global.data()["names"]
    keep_genes=[i for i, feat in enumerate(features) if " x " not in feat]
    scores = np.array(ebm_global.data()["scores"])
    scores=scores[keep_genes]

    genes=genes[np.argsort(scores)][::-1]
    scores=scores[np.argsort(scores)][::-1]

    importance_table = pd.DataFrame.from_dict({
        "gene": genes,
        "log10S": np.log10(scores),
    },
        orient="columns",
    )
    
    importance_table.set_index("gene", inplace=True)
        
    return importance_table