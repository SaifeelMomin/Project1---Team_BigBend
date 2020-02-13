import pandas as pd
from create_db import engine
from sqlalchemy.exc import ProgrammingError
import warnings
import numpy as np
import requests
import datetime

DATABASE = "team_big_bend"
engine.execute(f"USE {DATABASE}")

TABLENAME = "incidents"
engine.execute(f"DROP TABLE IF EXISTS {TABLENAME}")

# Set up the api url and parameters
traffic_incidents = []
r = requests.get(
    "https://data.austintexas.gov/resource/dx9v-zd7x.json",
    params={"$limit": 300000, "$offset": 0},
)
if r.status_code == 200:
    traffic_incidents = [
        {
            "ReportID": rec["traffic_report_id"],
            "IncidentDesc": rec["issue_reported"],
            "Address": str(rec["address"]).upper(),
            "IncidentDate": rec["traffic_report_status_date_time"],
        }
        for rec in r.json()
    ]
else:
    print("***** Critical Error Please Try again *****")
    print(r.status_code)


traffic_incidents = pd.DataFrame(traffic_incidents)
traffic_incidents["Street"] = traffic_incidents["Address"].str.extract(
    "(LAMAR)", expand=True
)
traffic_incidents["RecordDate"] = traffic_incidents["IncidentDate"].str.extract(
    "(\d+-\d+-\d+)", expand=True
)
traffic_inc_clean = traffic_incidents[traffic_incidents.Street.notnull()]

pd.DataFrame(traffic_inc_clean).to_sql(name=TABLENAME, con=engine)
