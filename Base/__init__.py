import os
import json
import ConfigParser
import logging.config

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# load the shared settings file
settings_file_path = os.path.join(base_dir, 'config', 'settings.config')
settings = ConfigParser.ConfigParser()
settings.read(settings_file_path)

# set up logging
with open(os.path.join(base_dir, 'config', 'logging.json'), 'r') as f:
    logging_config = json.load(f)
logging.config.dictConfig(logging_config)
log = logging.getLogger(__name__)
log.info("---------------------------------------------------------------------------")
requests_logger = logging.getLogger('requests')
requests_logger.setLevel(logging.INFO)