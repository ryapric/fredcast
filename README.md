Project: Forecasts for Federal Reserve Bank of St. Louis
========================================================

[FREDcast](https://fredcast.appspot.com) is a web application for
programmatically requesting forecasts of the Federal Reserve Economic Data
(FRED). It spawned as an example of how to introduce DevOps best-practices into
"data science" workflows, a workshop track I led; you can find that parent repo
[here](https://github.com/ryapric/pbdw).

It now serves as a lightweight example to myself and others on how to use
[Flask](https://flask.pocoo.org) as a production web server framework, as well
as how to implement DevOps principles like CI/CD into such a deployment; in this
case, by leveraging [Google Cloud Platform's](https://cloud.google.com) [Cloud
Build system](https://cloud.google.com/cloud-build), though there are many tools
to help you realize these and other goals ([AWS](https://aws.amazon.com),
[Azure](https://azure.microsoft.com), [Jenkins](https://jenkins.io) (on-prem,
even), etc).

API Documentation
-----------------

This Flask application is hosted [here](https://fredcast.appspot.com), and
exposes several endpoints from which you may request data via query strings:

| Endpoint | Query String Parameter | Parameter Format |
| --- | --- | --- |
| `/api/fredcast` | `fred_id` | String. A list of valid `fred_id`s can be found [here](https://fred.stlouisfed.org/tags/series), hovering over a link, and noting the last part of its URL |
| `/api/fredcast` | `start_date` | String. Must be in the format `YYYY-MM-DD` |
| `/api/fredcast` | `end_date` | String. Must be in the format `YYYY-MM-DD` |

Future Work
-----------

Currently, the forecast methodology only supports *monthly* data (as that's the
frequency it expects). This will soon be expanded to automatically handle data
of any frequency.
