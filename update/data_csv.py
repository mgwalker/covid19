import csv
import re
import requests
from io import StringIO
import urllib

state_re = re.compile(r"(.+), ([A-Z]{2})( \(From Diamond Princess\))?\s*$")

base_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-{}.csv"


def get_raw_data():
    all_data = {
        "total": {"active": 0, "confirmed": 0, "deaths": 0, "recovered": 0},
        "states": {},
    }

    def getDataFor(type):
        data = csv.DictReader(StringIO(requests.get(base_url.format(type)).text))
        key = type.lower()

        for row in data:
            if row["Country/Region"] == "US":
                all_keys = [*row]
                last = all_keys.pop()
                location = row["Province/State"]
                match = state_re.match(location)

                while row[last] == "":
                    last = all_keys.pop()

                count = int(row[last])

                if match == None:
                    print(f"{count}: {location}")
                    continue

                location = match.group(1)
                state = match.group(2)

                if not state in all_data["states"].keys():
                    all_data["states"][state] = {
                        "total": {
                            "active": 0,
                            "confirmed": 0,
                            "deaths": 0,
                            "recovered": 0,
                        }
                    }
                if not location in all_data["states"][state].keys():
                    all_data["states"][state][location] = {
                        "active": 0,
                        "confirmed": 0,
                        "deaths": 0,
                        "recovered": 0,
                    }

                all_data["states"][state]["total"][key] += count
                all_data["states"][state][location][key] = count

    getDataFor("Confirmed")
    getDataFor("Deaths")
    getDataFor("Recovered")

    for state in all_data["states"]:
        state = all_data["states"][state]

        for location in state:
            state[location]["active"] = (
                state[location]["confirmed"]
                - state[location]["deaths"]
                - state[location]["recovered"]
            )

        all_data["total"]["active"] += state["total"]["active"]
        all_data["total"]["confirmed"] += state["total"]["confirmed"]
        all_data["total"]["deaths"] += state["total"]["deaths"]
        all_data["total"]["recovered"] += state["total"]["recovered"]

    return all_data

