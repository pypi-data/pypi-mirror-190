import os.path
import joblib

import numpy as np
from interpret.glassbox import ExplainableBoostingClassifier
from sklearn.metrics import (
    accuracy_score,
    log_loss,
)

from sleep_models.models.models import SleepModel

class EBM(
    SleepModel, ExplainableBoostingClassifier,
):

    _estimator_type = "classifier"
    _encoding = "ONE_HOT"
    # this just means the validation accuracy is evaluated for illustrative purposes only
    # (i.e. it is not guiding the training by any means)
    uses_validation_in_train = True

    def __init__(
        self,
        name,
        target,
        output=".",
        random_state=1000,
        outer_bags=8,
        inner_bags=0,
        learning_rate=0.01,
        validation_size=0.15,
        min_samples_leaf=2,
        max_leaves=3,
        max_rounds=5000,
        early_stopping_rounds=50,
        early_stopping_tolerance=1e-4,
    ):
        ExplainableBoostingClassifier.__init__(
            self,
            outer_bags=outer_bags,
            inner_bags=inner_bags,
            learning_rate=learning_rate,
            validation_size=validation_size,
            min_samples_leaf=min_samples_leaf,
            max_leaves=max_leaves,
            max_rounds=max_rounds,
            early_stopping_rounds=early_stopping_rounds,
            early_stopping_tolerance=early_stopping_tolerance,
        )

        super(EBM, self).__init__(
            name=name, target=target, output=output, random_state=random_state
        )
        self._ncols = None

    @classmethod
    def new_model(cls, config, X_train=None, y_train=None, encoding=None):
        model = cls(
            name=config.cluster,
            output=config.output,
            random_state=config.random_state,
            target=config.target,
        )
        model._label_code = encoding
        return model

    def predict_log_proba(self, *args, **kwargs):
        return np.log(self.predict_proba(*args, **kwargs))


    def fit(self, X, y, *args, X_val=None, y_val=None, **kwargs):
        self._ncols = y.shape[1]
        y_truth = y.argmax(1)
        # only the training set is used to fit the model
        result = super(EBM, self).fit(X, y_truth)
        
        y_pred_val = self.predict(X_val)

        confusion_table = self.get_confusion_table(
            y_val.argmax(1), y_pred_val.argmax(1)
        )
        self.save()
        self.save_results(confusion_table=confusion_table)
        return result

    def predict(self, X):
        y_pred = super().predict(X)
        ph = np.zeros((y_pred.shape[0], self._ncols))

        for i in range(y_pred.shape[0]):
            ph[i, y_pred[i]] = 1

        return ph

    def benchmark(self, X, y):

        y2 = y.argmax(1)
        prediction = self.predict(X)
        accuracy = accuracy_score(y, prediction)
        loss = log_loss(y, prediction)

        prediction_code = prediction
        right = prediction_code == y

        return accuracy, loss, prediction, right

    def save(self):
        path = os.path.join(self.output, f"{self.name}.joblib")
        print(f"Saving model to {path}")
        with open(path, "wb") as filehandle:
            joblib.dump(self, filehandle)
