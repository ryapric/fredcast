import pytest
from pandas.testing import assert_frame_equal
from fredcast.io.get import get_fred
from fredcast.io.db import db_write
import pandas as pd
from sqlalchemy import create_engine

def test_get_fred():
    fred_id = 'MONAN'
    df = get_fred(fred_id)
    assert list(df.columns.values) == ['DATE', fred_id, 'label']
    # Definitely one of these # of months by default
    assert len(df.index) in [59, 60, 61]
    # Fail on unapproved dates
    for d in ['2018-01-32', '20180101', '1', 'abc']:
        with pytest.raises(ValueError) as e:
            get_fred('MONAN', start_date = d)
        with pytest.raises(ValueError) as e:
            get_fred('MONAN', end_date = d)
# end test_get_fred

def test_db_write(df_m):
    fred_id = 'MONAN'
    dbpath = './test.db'
    db_write(df_m, fred_id, dbpath = dbpath)

    con = create_engine(f'sqlite:///{dbpath}').connect()
    tbl = pd.read_sql_table(f'fcast_{fred_id}', con)
    con.close()

    assert_frame_equal(tbl, df_m)
# end test_db_write

def test_teardown(teardown):
    pass
