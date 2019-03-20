from flask import Flask, request, Response
import fredcast.io.get as get
import fredcast.forecast.ets as fc
import pandas as pd

def create_app(test_config = None):
    app = Flask(__name__)

    # Flag for when running tests
    testing = True if (test_config is not None and test_config['TESTING']) else False

    # Index
    @app.route('/', methods = ['GET'])
    def index():
        helpstr = """
        <p>
        Get forecasted data by hitting /api/fredcast with a valid query string
        containing `fred_id`, `start_date`, and `end_date`. The API will run
        with defaults if some or all values are not specified.
        <br/><br/>
        Those defaults are:
        <br/>
        <ul>
            <li>`fred_id` = 'GDP'</li>
            <li>`start_date` = five years ago</li>
            <li>`end_date` = today</li>
        </ul>
        </p>
        """
        return helpstr, 200
    #end index

    # Health check
    @app.route('/api/health', methods = ['GET'])
    def app_health():
        return '{"msg": "ok"}', 200
    # end app_health

    @app.route('/api/fredcast', methods = ['GET'])
    def fcast():
        """
        Hit this endpoint with a query string to receive a JSON response that
        can then  be parsed into a tabular  containing
        """
        start_date_default = get.start_date_default
        end_date_default = get.end_date_default

        fred_id = request.args.get('fred_id', default = 'GDP', type = str)
        start_date = request.args.get('start_date', default = start_date_default, type = str)
        end_date = request.args.get('end_date', default = end_date_default, type = str)

        try:
            df = get.get_fred(fred_id, start_date, end_date)
        except:
            errmsg = """
            <p>
            Please check your `fred_id`, and/or dates, and try again.
            <br/><br/>
            <ul>
                <li>`fred_id` must be a valid FRED series ID, a list of which
                can be found
                <a href='https://fred.stlouisfed.org/tags/series'>here</a>.
                Hovering over the link will show you the series ID as the last
                URL component.</li>
                <li>`start_date` and `end_date` must be in this exact format:
                YYYY-MM-DD</li>
            </ul>
            </p>
            """
            return errmsg, 400
        # end try
        
        df_fcast = fc.fredcast(df, fred_id)

        # Enforce response is *clean* JSON
        # just df.to_json() still returns text/html, and calling flask.jsonify()
        # on it adds too many escape characters
        resp = Response(
            response = df_fcast.to_json(orient = 'records'),
            status = 200,
            mimetype = 'application/json'
        )
        return resp
    # end api_fcast

    return app
# end create_app
