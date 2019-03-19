import pytest
from fredcast.app.app_factory import create_app
import os
import pandas as pd

@pytest.fixture
def df_m():
    df_m = pd.read_csv('tests/data/example_monthly.csv')
    df_m['DATE'] = pd.to_datetime(df_m['DATE'])
    return df_m

@pytest.fixture
def df_q():
    df_q = pd.read_csv('tests/data/example_quarterly.csv')
    df_q['DATE'] = pd.to_datetime(df_q['DATE'])
    return df_q

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
