from fredcast.forecast.ets import (
    fit_ets,
    get_mape,
    fredcast
)

fred_id_m = 'MONAN'
fred_id_q = 'GDP'

# def test_fit_ets(df):
#     model = fit_ets(df, fred_id)
#     assert model.
# # end test_fit_ets

def test_get_mape(df_m):
    model = fit_ets(df_m, fred_id = fred_id_m, seasonal_periods = 12)
    mape = get_mape(model, df_m, fred_id_m)
    assert isinstance(mape, float)
# end test_get_mape

def test_fredcast_monthly(df_m):
    # Monthly data, default h
    df_fcast = fredcast(df_m, fred_id_m)
    assert len(df_fcast.index) == (len(df_m.index) + 12)
    assert list(df_fcast.columns.values) == ['DATE', fred_id_m, 'label', 'MAPE']
    # Monthly data, supplied h
    df_fcast = fredcast(df_m, fred_id_m, h = 6)
    assert len(df_fcast.index) == (len(df_m.index) + 6)
    assert list(df_fcast.columns.values) == ['DATE', fred_id_m, 'label', 'MAPE']
# end test_fredcast_monthly

def test_fredcast_quarterly(df_q):
    # Quarerly data, default h
    df_fcast = fredcast(df_q, fred_id_q)
    assert len(df_fcast.index) == (len(df_q.index) + 4)
    assert list(df_fcast.columns.values) == ['DATE', fred_id_q, 'label', 'MAPE']
    # Quarterly data, supplied h
    df_fcast = fredcast(df_q, fred_id_q, h = 2)
    assert len(df_fcast.index) == (len(df_q.index) + 2)
    assert list(df_fcast.columns.values) == ['DATE', fred_id_q, 'label', 'MAPE']
# end test_fredcast_quarterly
