import logging
import yaml
import os.path
import logging.config

def apply_logging_config():
    if os.path.exists("logging.yaml"):
        with open("logging.yaml", "r") as filehandle:
            config = yaml.load(filehandle, yaml.SafeLoader)
        logging.config.dictConfig(config)

    

