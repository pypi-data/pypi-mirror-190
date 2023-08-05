import yaml

def load_pipeline_config():
    with open("config.yaml", "r") as filehandle:
        config = yaml.load(filehandle, yaml.SafeLoader)

    return config

def save_pipeline_config(config, dest=None):
    if dest is None:
        dest = "config.yaml"

    with open(dest, "w") as filehandle:
        yaml.dump(config, filehandle)