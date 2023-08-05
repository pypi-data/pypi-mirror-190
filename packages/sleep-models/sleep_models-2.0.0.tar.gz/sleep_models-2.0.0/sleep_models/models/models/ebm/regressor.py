import os.path
import joblib

import pandas as pd
import numpy as np
from interpret.glassbox import ExplainableBoostingRegressor
from sklearn.metrics import (
    mean_squared_error,
    log_loss,
)

from sleep_models.models.models import SleepModel

class EBMRegressor(
    SleepModel, ExplainableBoostingRegressor,
):

    _estimator_type = "regressor"
    # this just means the validation accuracy is evaluated for illustrative purposes only
    # (i.e. it is not guiding the training by any means)
    uses_validation_in_train = True
    _encoding = None
    _metrics = ["mean_squared_error"]

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
        ExplainableBoostingRegressor.__init__(
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

        super(EBMRegressor, self).__init__(
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
        result = super(EBMRegressor, self).fit(X, y.flatten())
        y_pred = self.predict(X)
        loss_table=pd.DataFrame.from_dict({"y": y.flatten(), "y_pred": y_pred})

        y_pred_val = self.predict(X_val)
        loss_table_val=pd.DataFrame.from_dict({"y": y_val.flatten(), "y_pred": y_pred_val})

        self.save()
        self.save_results(loss_table=loss_table, loss_table_val=loss_table_val)
        return result


    def benchmark(self, X, y):
        prediction = self.predict(X)
        loss = log_loss(y, prediction)
        prediction_code = prediction
        right = prediction_code == y
        return _, loss, _, _

    def _get_mean_squared_error(self, X, y):
        prediction = self.predict(X)
        mse = mean_squared_error(y, prediction)
        return mse

    def save(self):
        path = os.path.join(self.output, f"{self.name}.joblib")
        print(f"Saving model to {path}")
        with open(path, "wb") as filehandle:
            joblib.dump(self, filehandle)
