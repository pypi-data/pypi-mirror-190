from .models import EBM, EBMRegressor, MLP, KNN, RF
#from .torch.nn import NeuralNetwork

MODELS = {model.__name__: model for model in [
    EBM, KNN, MLP, RF,
    #NeuralNetwork,
    EBMRegressor
]}
