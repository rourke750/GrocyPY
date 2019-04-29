"""Utility functions and classes.

Attributes:
    RESOURCE_PKG: The package that contains this project's resources

"""

import asyncio
import logging
import random
import sys
import time
import requests
from contextlib import contextmanager
from functools import wraps
from pkg_resources import resource_filename


RESOURCE_PKG = 'GrocyPY.resources'

@contextmanager
def resource(name, *args, **kwargs):
    filename = resource_path(name)
    with open(filename, *args, **kwargs) as f:
        yield f


def resource_path(name):
    return resource_filename(RESOURCE_PKG, name)


def chromedriver():
    self = chromedriver

    if 'driver' not in self.__dict__:
        if sys.platform.startswith('win'):
            binary = 'chromedriver.exe'
        else:
            binary = 'chromedriver'
        self.driver = resource_filename(RESOURCE_PKG, binary)

    return self.driver
    
def firefoxdriver():
    self = firefoxdriver

    if 'driver' not in self.__dict__:
        if sys.platform.startswith('win'):
            binary = 'geckodriver.exe'
        else:
            binary = 'geckodriver'
        self.driver = resource_filename(RESOURCE_PKG, binary)

    return self.driver


def random_useragent():
    self = random_useragent

    if 'useragents' not in self.__dict__:
        with resource('useragents.txt') as f:
            self.useragents = [line.strip() for line in f]

    return random.choice(self.useragents)


def headers():
    """Helper function for generating headers."""
    return {'User-Agent': random_useragent()}
   

def log(message, level=logging.DEBUG):
    if level == logging.DEBUG:
        logging.debug(message)
    elif level == logging.INFO:
        logging.info(message)
    elif level == logging.WARNING:
        logging.warning(message)
    elif level == logging.ERROR:
        logging.error(message)
    elif level == logging.CRITICAL:
        logging.critical(message)