import pytest
from fredcast.app.app_factory import create_app
import os
import pandas as pd

@pytest.fixture
def df():
    df = pd.read_csv('tests/data/example.csv')
    df['DATE'] = pd.to_datetime(df['DATE'])
    return df

@pytest.fixture
def app():
    # Not 100% sure why, but both of these appear in the Flask docs. They might
    # be redundant.
    app = create_app({'TESTING': True})
    app.testing = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def teardown():
    """
    Dummy 'test' fixture for teardown functionality, like removing SQLite DB,
    etc.
    """
    try:
        os.remove('./test.db')
    except:
        pass
