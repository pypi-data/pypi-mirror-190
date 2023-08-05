from sklearn.neighbors import KNeighborsClassifier
from .models import SleepModel

class KNN(
    SleepModel, KNeighborsClassifier,
):
    _estimator_type = "classifier"
    _encoding = "ONE_HOT"

    @classmethod
    def new_model(cls, config, X_train=None, y_train=None, encoding=None):
        model = cls(
            name=config.cluster,
            n_neighbors=config.training_config.n_neighbors,
            weights=config.training_config.weights,
            leaf_size=config.training_config.leaf_size,
            p=config.training_config.p,
            metric=config.training_config.metric,
            random_state=config.random_state,
            target=config.target,
        )

        model._label_code = encoding
        return model

