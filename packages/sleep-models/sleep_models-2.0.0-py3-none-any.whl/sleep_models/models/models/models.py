# To add a new model:
# Keep calm and...
#
#
# 1. Create a class with the scikit learn API
# (either from scratch or subclassing)
#
# 2. Define the class' _metric = "ACC"
#
# 3. Add that class to the MODELS list at the end
#
#
#

import logging
from abc import ABC, abstractmethod
import os.path
import pickle
import warnings

import numpy as np
import pandas as pd
import yaml
from sklearn.metrics import (
    accuracy_score,
    mean_squared_error,
    log_loss,
    recall_score,
)
from sleep_models.models.utils.metrics import (
    calibrate_accuracy,
    specificity_score,
    expected_mean_score,
    trivial_mean_score,
)



from sklearn.utils.estimator_checks import check_estimator
from sleep_models.preprocessing import make_confusion_table
from sleep_models.models.utils.config import isnamedtupleinstance
from sleep_models.plotting import plot_confusion_table
from sleep_models.preprocessing import make_confusion_long_to_square
from sleep_models.models.variables import ModelProperties

logger = logging.getLogger(__name__)


class SleepModel(ABC):

    _estimator_type = None
    uses_validation_in_train = False
    _metrics = ["accuracy", "recall", "specificity", "expected_accuracy", "trivial_accuracy"]

    def __init__(self, name, target, output=".", random_state=1000):
        self.name = name
        self.output = output
        self.random_state = random_state
        self._target = target
        super().__init__()

    @classmethod
    @abstractmethod
    def new_model(cls, config, X_train=None, y_train=None, encoding=None):
        raise NotImplementedError

    @property
    def epochs(self):
        return 0

    @classmethod
    def model_properties(cls):
        return ModelProperties(
            encoding=cls._encoding, estimator_type=cls._estimator_type
        )

    def proba(self, x):
        return self.predict_proba(x)[:,1]
    def log_odds(self, x):
        p = self.predict_log_proba(x)
        return p[:,1] - p[:,0]


    def benchmark(self, X, y):

        prediction = self.predict(X)

        accuracy = accuracy_score(y, prediction)
        loss = log_loss(y, prediction)

        prediction_code = np.array(prediction).argmax(1)
        right = prediction_code == y.argmax(1)

        return accuracy, loss, prediction, right

    def fit(self, X, y, *args, X_val=None, y_val=None, **kwargs):
        labels=set(y)
        weights=np.ones(len(y))
        for label in labels:
            weight = 1/len(labels) * len(y) / (y==label).sum()
            print(f"Label {label} ({round((y==label).mean(), 4)}) - weight {round(weight, 5)}")
            weights[y==label] = weight

        try:
            return super(SleepModel, self).fit(X, y, sample_weight=weights)
        except Exception as error:
            import ipdb; ipdb.set_trace()

    def get_loss(self, X, y):
        """
        Returns the loss of the model for this dataset

        Arguments:
            X (np.ndarray): Shape nxm where n = number of samples (single cells) and m number of features
            y (np.ndarray): Shape nxc where n = number of samples (single cells) and c number of categories
        Returns:
            loss (float): Number from 0 to Infinity quantifying how wrong the model is
                loss of 0 means the model asssigns all probability to the truth i.e 0 to wrong options
                A non zero loss is compatible with 100% accuracy, because predictions can be made
                correctly while still assigning some probability to the wrong classes
        """

        _, loss, _, _ = self.benchmark(X, y)
        return loss

    def get_metric(self, X, y, metric=None):
        if metric is None:
            metric = self._metrics[0]
        return getattr(self, f"_get_{metric}")(X, y)

    def get_metrics(self, X, y):

        metrics = {
            metric: self.get_metric(X, y, metric=metric) for metric in self._metrics
        }

        return metrics


    def _get_accuracy(self, X, y):
        return self.score(X, y)

    def _get_recall(self, X, y):
        y_true = y
        y_pred = self.predict(X)

        if len(y_true.shape) > 1:
            y_true = y_true.argmax(1)
            y_pred = y_pred.argmax(1)

        return recall_score(y_true, y_pred)


    def _get_trivial_accuracy(self, X, y):
        y_true = y
        if len(y_true.shape) > 1:
            y_true = y_true.argmax(1)

        return trivial_mean_score(y_true)

    def _get_expected_accuracy(self, X, y):
        y_true = y
        if len(y_true.shape) > 1:
            y_true = y_true.argmax(1)

        return expected_mean_score(y_true)


    def _get_specificity(self, X, y):
        y_true = y
        y_pred = self.predict(X)

        if len(y_true.shape) > 1:
            y_true = y_true.argmax(1)
            y_pred = y_pred.argmax(1)

        return specificity_score(y_true, y_pred)


    def _get_rmse(self, X, y):
        """
        Compute Root Mean Squared Error for this dataset

        Arguments:
            X (np.ndarray): Shape nxm where n = number of samples (single cells) and m number of features
            y (np.ndarray): Shape nxc where n = number of samples (single cells) and c number of categories
        """

        y_pred = self.predict(X).argmax(1)
        y_flat = y.argmax(1)
        return np.sqrt(mean_squared_error(y_pred, y_flat))

    def get_confusion_table(self, truth, predictions):
        """
        Compute confusion table for this dataset

        Arguments:
            X (np.ndarray): Shape nxm where n = number of samples (single cells) and m number of features
            y (np.ndarray): Shape nxc where n = number of samples (single cells) and c number of categories
        """
        order = list(self._label_code.values())

        confusion_table = make_confusion_long_to_square(
            make_confusion_table(self, truth, predictions), order=order
        )

        return confusion_table

    def save(self):
        path = os.path.join(self.output, f"{self.name}.pickle")
        print(f"Saving model to {path}")
        with open(path, "wb") as filehandle:
            pickle.dump(self, filehandle)

    def save_metrics(self):
        return

    def save_results(self, suffix=None, **kwargs):

        self.save_metrics()

        for key, value in kwargs.items():

            components = [self.name, key, suffix]
            components = [c for c in components if c is not None]

            base_filename = "_".join(components)

            # confusion table
            if isinstance(value, pd.DataFrame):
                value.to_csv(os.path.join(self.output, base_filename + ".csv"))

                if key == "confusion_table":
                    confusion_table = value
                    print(confusion_table)

                    plot_confusion_table(
                        confusion_table,
                        os.path.join(self.output, f"{base_filename}.png"),
                    )

            # config
            elif isinstance(value, tuple) and isnamedtupleinstance(value):
                data = {k: getattr(value, k) for k in value._fields}
                with open(
                    os.path.join(self.output, base_filename + ".yml"), "w"
                ) as filehandle:
                    yaml.dump(data, filehandle)

