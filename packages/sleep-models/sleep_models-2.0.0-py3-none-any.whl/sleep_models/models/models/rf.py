
from sklearn.ensemble import RandomForestClassifier
from .models import SleepModel

class RF(SleepModel, RandomForestClassifier):

    _estimator_type = "classifier"
    _encoding = "ONE_HOT"
    uses_validation_in_train=True

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


    def fit(self, X, y, *args, X_val=None, y_val=None, **kwargs):
        self._ncols = y.shape[1]
        y_truth = y.argmax(1)
        result = super(RF, self).fit(X, y_truth)

        y_pred_test = self.predict(X_val)

        confusion_table = self.get_confusion_table(
            y_val.argmax(1), y_pred_test
        )
        self.save()
        self.save_results(confusion_table=confusion_table)
        return result

    def get_metric(self, X, y, metric=None):
        
        if metric is None:
            metric = self._metrics[0]

        return getattr(self, f"_get_{metric}")(X, y.argmax(1))
