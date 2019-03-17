import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def fit_ets(df, fred_id, seasonal_periods = 12):
    """
    Intermediate function to fit Holt-Winters ETS model.

    :param df: pandas `DataFrame` containing FRED data

    :param fred_id: FRED series ID

    :param seasonal_periods: Number of seasonal periods for data. If monthly,
                             then 12 (the default); if quarterly, then 4; etc.
    
    :returns: `statsmodels` ETS model object
    """
    model = ExponentialSmoothing(
        df[fred_id],
        trend = 'add',
        seasonal = 'add',
        seasonal_periods = seasonal_periods
    ).fit()
    return model
# end fit_ets

def get_mape(model, df, fred_id):
    """
    Intermediate function to calculate mean absolute percentage eror (MAPE) of
    ETS model, returned as its points representation (e.g. 3 == 3% MAPE,
    originally 0.03).

    :param model: ETS model object from `statsmodels.tsa.holtwinters.ExponentialSmoothing()`

    :param df: pandas `DataFrame` of FRED data that the model was based on

    :param fred_id: FRED series ID

    :returns: float
    """
    pct_error = np.abs((df[fred_id] - model.fcastvalues) / df[fred_id])
    mape = np.mean(pct_error) * 100
    return mape
# end get_mape

def fredcast(df, fred_id, seasonal_periods = 12, h = 12):
    """
    Construct time-series forecast on passed `DataFrame`

    :param df: pandas `DataFrame` containing FRED data

    :param fred_id: FRED series ID. Also used to index the correct column in `df`.

    :param seasonal_periods: Number of seasonal periods for data. If monthly,
                             then 12 (the default); if quarterly, then 4; etc.

    :param h: Number of periods to forecast forward
    """
    model = fit_ets(df, fred_id, seasonal_periods)
    fcast = model.forecast(h)
    mape = get_mape(model, df, fred_id)
    # Jesus, this is messy
    df_fcast = pd.DataFrame(
        data = {
            'DATE': pd.date_range(
                pd.to_datetime(df['DATE'].values[len(df.index)-1]) + pd.DateOffset(months = 1),
                periods = h,
                freq = 'MS'
            ),
            fred_id: fcast,
            'label': 'Forecast',
            'MAPE': mape
        }
    )
    df_out = df.append(df_fcast, sort = False)
    return df_out
# end fredcast
