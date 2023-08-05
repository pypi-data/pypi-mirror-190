import numpy as np


def expected_mean_score(y):
    _, counts = np.unique(y, return_counts=True)
    p = counts / counts.sum()
    entropy = -np.sum(p * np.log2(p)).item()
    accuracy = entropy2accuracy(entropy)

    return accuracy


def entropy2accuracy(entropy):
    """
    The inverse of Shanon's entropy
    i.e. given the entropy of a binary variable,
    give me the p of the positive class
    """
    acc=np.round(1 / (2 ** entropy), 3)
    return acc


def trivial_mean_score(y):
    counts = np.unique(y, return_counts=True)[1]
    return round((counts.max() / counts.sum()).item(), 3)


def calibrate_accuracy(labels):
    """
    """
    random_accuracy = expected_mean_score(labels.argmax(axis=1))
    print(f"Random accuracy: {random_accuracy}")
    trivial_accuracy = trivial_mean_score(labels.argmax(axis=1))
    print(f"Trivial accuracy: {trivial_accuracy}")
    return {"random": random_accuracy, "trivial": trivial_accuracy}

def specificity_score(y_true, y_pred):

    tn = np.bitwise_and(
        y_true == 0,
        y_pred == 0
    ).sum()

    fp = np.bitwise_and(
        y_true == 0,
        y_pred == 1
    ).sum()
    specificity = tn / (tn+fp)
    return specificity
