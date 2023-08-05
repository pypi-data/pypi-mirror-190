from sklearn.neural_network import MLPRegressor
from .models import SleepModel

class MLP(
    SleepModel, MLPRegressor,
):

    _estimator_type = "classifier"
    _encoding = "ONE_HOT"

    @classmethod
    def new_model(cls, config, X_train=None, y_train=None, encoding=None):
        model = cls(
            name=config.cluster,
            hidden_layer_sizes=config.training_config.n_neurons,
            activation=config.training_config.activation,
            solver=config.training_config.solver,
            alpha=config.training_config.alpha,
            batch_size=config.training_config.batch_size,
            learning_rate=config.training_confignfig.learning_rate,
            learning_rate_init=config.training_config.learning_rate_init,
            random_state=config.random_state,
            target=config.target,
        )

        model._label_code = encoding
        return model
