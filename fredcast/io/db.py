from sqlalchemy import create_engine

def db_write(df_out, fred_id, dbpath = './fcast.db', if_exists = 'replace'):
    """
    Write out `DataFrame` containing actual & forecast values to database.
    Currently writes to local SQLite DB, `fcast.db`, in working directory.
    Tables are written using their FRED ID, in the form 'fcast_<fred_id>'.

    :param df_out: pandas `DataFrame` to store in DB.

    :param fred_id: FRED series ID. Used in naming DB table.

    :param dbpath: File path to SQLite DB

    :param if_exists: Passed to `pd.DataFrame.to_sql()`
    """
    con = create_engine(f'sqlite:///{dbpath}').connect()
    df_out.to_sql(f'fcast_{fred_id}', con, index = False, if_exists = if_exists)
    con.close()
# end db_write
