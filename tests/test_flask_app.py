import datetime
import json
import pandas as pd

def test_health(client):
    r = client.get('/api/health')
    assert r.status_code == 200
    assert r.data == b'{"msg": "ok"}'
# end test_health

def test_api_fredcast(client):
    # Try a few dates & IDs, to poke around edge cases
    fred_id = 'MONAN'
    start_date = '2018-01-01'
    r = client.get(f'/api/fredcast?fred_id={fred_id}&start_date={start_date}')

    fred_id = 'MONAN'
    start_date = '2019-04-23'
    end_date = '2019-06-31'
    r = client.get(f'/api/fredcast?fred_id={fred_id}&start_date={start_date}&end_date={end_date}')

    fred_id = 'GDP'
    start_date = '2018-01-01'
    end_date = '2019-07-15'
    r = client.get(f'/api/fredcast?fred_id={fred_id}&start_date={start_date}&end_date={end_date}')
    
    fred_id = 'GDP'
    end_date = '2019-07-15'
    r = client.get(f'/api/fredcast?fred_id={fred_id}&end_date={end_date}')
    
    fred_id = 'CPIAUCSL'
    r = client.get(f'/api/fredcast?fred_id={fred_id}')
    
    # Now test some other properties
    assert r.is_json
    data = json.loads(r.data.decode('utf-8'))
    assert list(data[0].keys()) == ['DATE', fred_id, 'label', 'MAPE']
    df = pd.DataFrame(data = data)
    df = df.sort_values('DATE')
    assert len(df) == len(data)
# end test_fcast
