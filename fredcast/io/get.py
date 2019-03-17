import requests
import datetime # stdlib
import tempfile #stlib
import pandas as pd

# get_fred() defaults
today = datetime.datetime.now().strftime('%Y-%m-%d')
start_date_default = (pd.to_datetime(today) - pd.DateOffset(years = 5)).strftime('%Y-%m-%d')
end_date_default = today

def get_fred(fred_id, start_date = start_date_default, end_date = end_date_default):
    """
    Fetch time-series data from Federal Reserve Economic Data (FRED), provided
    by the Federal Reserve Bank of St. Louis.

    :param fred_id: ID string for FRED series

    :param start_date: Start date for FRED series, as a string in the format
                       YYYY-MM-DD. Defaults to five years prior to the date
                       called.

    :param end_date: End date for FRED series. Defaults to the date called.

    :returns: A pandas `DataFrame`
    """
    # Shitty way around not asking for an API key, since returned data is raw
    # text. With a key, change this to GET from the API endpoint
    try:
        [datetime.datetime.strptime(d, '%Y-%m-%d') for d in [start_date, end_date]]
    except ValueError:
        raise ValueError('Bad date format! Must be YYYY-MM-DD')
    
    url = 'https://fred.stlouisfed.org/graph/fredgraph.csv'
    r = requests.get(f'{url}?id={fred_id}&cosd={start_date}&coed={end_date}')

    with tempfile.NamedTemporaryFile('w', delete = False) as f:
        f.write(r.text)
        tmpfile = f.name

    df = pd.read_csv(tmpfile)

    # Prep
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['label'] = 'Actual'

    return df
# end get_fred
