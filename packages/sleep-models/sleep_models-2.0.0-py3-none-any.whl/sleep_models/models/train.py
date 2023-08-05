import logging

logger = logging.getLogger(__name__)
import os.path


def fit_model(model, X_train, y_train, X_val, y_val):

    logger.info("Training model")
    if model.uses_validation_in_train:
        model.fit(X_train, y_train, X_val=X_val, y_val=y_val)
    else:
        model.fit(X_train, y_train)


def train_model(model, X_train, y_train, X_val, y_val):
    """
    Arguments:

        * model (sleep_models.models.models.SleepModel): An instance of one of the models in sleep_models
        * data (tuple of np.ndarray): tuple of length 4 with the features and labels of a train and a validation set
    """

    fit_model(model, X_train, y_train, X_val, y_val)

    logger.info("Backing up model")
    model.save()

    print(f"{model._metrics[0]} on train set: {model.get_metric(X_train, y_train, model._metrics[0])}")
    print(f"{model._metrics[0]} on validation set: {model.get_metric(X_val, y_val, model._metrics[0])}")
    return 0
