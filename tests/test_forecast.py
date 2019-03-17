from fredcast.forecast.ets import (
    fit_ets,
    get_mape,
    fredcast
)

fred_id = 'MONAN'

# def test_fit_ets(df):
#     model = fit_ets(df, fred_id)
#     assert model.
# # end test_fit_ets

def test_get_mape(df):
    model = fit_ets(df, fred_id)
    mape = get_mape(model, df, fred_id)
    assert isinstance(mape, float)
# end test_get_mape

def test_fredcast(df):
    df_fcast = fredcast(df, fred_id)
    assert len(df_fcast.index) == (len(df.index) + 12)
    assert list(df_fcast.columns.values) == ['DATE', fred_id, 'label', 'MAPE']

    df_fcast = fredcast(df, fred_id, h = 6)
    assert len(df_fcast.index) == (len(df.index) + 6)
# end test_fredcast
