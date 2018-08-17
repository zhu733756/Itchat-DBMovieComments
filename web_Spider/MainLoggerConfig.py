# -*- coding: utf-8 -*-
"""
@author: zh
"""
import logging,os,yaml
from logging.config import dictConfig

def setup_logging(default_path,default_level = logging.INFO,env_key = "LOG_CFG"):
    path = default_path
    value = os.getenv(env_key,None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path,"r") as f:
            dictConfig(yaml.load(f))
    else:
        logging.basicConfig(level = default_level)









