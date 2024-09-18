"""
Spark submit helper
"""

import yaml

def get_cluster_size(size_config_path:str='etl/config/spark_size.yaml', size:str='x-small') -> dict:
    """
    Parse spark config and return the corresponding setting
    :param size_config_path: path to config file
    :type size_config_path: str
    :param size: size of config to fetch
    :type size: str
    :raise KeyError: if we don't find the match size
    :return: config
    :rtype: dict
    """
    with open(size_config_path, 'r', encoding='utf-8') as yaml_file:
        yaml_content = yaml.load(yaml_file, Loader=yaml.FullLoader)
    return yaml_content[size]
