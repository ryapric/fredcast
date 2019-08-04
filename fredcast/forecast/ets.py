from datetime import timedelta
import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def fredcast(df, fred_id, seasonal_periods = None, h = None):
    """
    Construct time-series forecast on passed `DataFrame`

    :param df: pandas `DataFrame` containing FRED data

    :param fred_id: FRED series ID. Also used to index the correct column in
                    `df`.

    :param seasonal_periods: Number of seasonal periods for data. Defaults to
                             None, but will be computed based on data if not
                             supplied. Currently only supports monthly and
                             quaterly data.

    :param h: Number of periods to forecast forward. Default is None, but will
              be computed as identical to the `seasonal_periods`, if not
              supplied explicitly.
    """
    # Super conservative day bounds, to infer data frequency
    datediff_min = pd.Timedelta(days = 27)
    datediff_max = pd.Timedelta(days = 32)
    datediff = df.at[1, 'DATE'] - df.at[0, 'DATE']
    if datediff_min <= datediff <= datediff_max:
        seasonal_periods = 12
        freqmult = 1
    elif (datediff_min * 3) <= datediff <= (datediff_max * 3):
        seasonal_periods = 4
        freqmult = 3
    # elif (datediff_min * 12) <= datediff <= (datediff_max * 12):
    #     seasonal_periods = 1
    #     freqmult = 12
    else:
        raise Exception('Cannot determine data frequency; please pass explicitly')
    
    # Set forecast length to seasonal periods, if not supplied
    h_periods = h if h is not None else seasonal_periods
    
    # Fit and forecast from model
    model = fit_ets(df, fred_id, seasonal_periods)
    fcast = model.forecast(h_periods)
    mape = get_mape(model, df, fred_id)

    # Jesus, this is messy
    df_fcast = pd.DataFrame(
        data = {
            'DATE': pd.date_range(
                start = pd.to_datetime(df['DATE'].values[len(df.index)-1]) + pd.DateOffset(months = (1 * freqmult)),
                end = pd.to_datetime(df['DATE'].values[len(df.index)-1]) + pd.DateOffset(months = (1 * freqmult * h_periods)),
                periods = h_periods
            ),
            fred_id: fcast,
            'label': 'Forecast',
            'MAPE': mape
        }
    )
    df_out = df.append(df_fcast, sort = False)
    return df_out
# end fredcast

def fit_ets(df, fred_id, seasonal_periods):
    """
    Intermediate function to fit Holt-Winters ETS model.

    :param df: pandas `DataFrame` containing FRED data

    :param fred_id: FRED series ID

    :param seasonal_periods: Number of seasonal periods for data. If monthly,
                             then 12; if quarterly, then 4; etc.
    
    :returns: `statsmodels` ETS model object
    """
    model = ExponentialSmoothing(
        df[fred_id],
        trend = 'mul',
        seasonal = 'mul',
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
