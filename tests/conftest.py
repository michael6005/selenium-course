import json
from selenium import webdriver
import pytest
from config.settings import BASE_DIR


def get_config_file_path():
    return BASE_DIR / 'config' / 'test_config.json'


@pytest.fixture
def config(scope='session'):
    with open(get_config_file_path()) as config_file:
        config = json.load(config_file)
        return config


def set_options(opts, config):
    if config['mode'] == 'Headless':
        opts.add_argument('--headless=new')


@pytest.fixture()
def browser(config):
    if config['browser'] == 'Chrome':
        opts = webdriver.ChromeOptions()
        set_options(opts, config)
        driver = webdriver.Chrome(options=opts)
    elif config['browser'] == 'Edge':
        opts = webdriver.EdgeOptions()
        set_options(opts, config)
        driver = webdriver.Edge(options=opts)
    else:
        raise Exception('Unknown type of browser')
    yield driver

    driver.quit()
