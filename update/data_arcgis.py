import re
import requests
import urllib

state_re = re.compile(r"(.+), ([A-Z]{2})( \(From Diamond Princess\))?\s*$")

SRC_URL = "".join(
    [
        "https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/1/query?f=json",
        "&returnGeometry=false",
        "&spatialRel=esriSpatialRelIntersects",
        "&cacheHint=true"
        "&outFields=Province_State,Country_Region,Confirmed,Deaths,Recovered",
        "&where=",
        urllib.parse.quote_plus("Confirmed > 0 AND Country_Region = 'US'"),
    ]
)


def get_raw_data():
    raw_data = [
        feature["attributes"] for feature in requests.get(SRC_URL).json()["features"]
    ]

    all_data = {
        "total": {"active": 0, "confirmed": 0, "deaths": 0, "recovered": 0},
        "states": {},
    }

    for place in raw_data:
        location = place["Province_State"]
        match = state_re.match(location)

        confirmed = place["Confirmed"]
        deaths = place["Deaths"]
        recovered = place["Recovered"]
        active = confirmed - deaths - recovered

        all_data["total"]["active"] += active
        all_data["total"]["confirmed"] += confirmed
        all_data["total"]["deaths"] += deaths
        all_data["total"]["recovered"] += recovered

        if match == None:
            continue

        location = match.group(1)
        state = match.group(2)

        if not state in all_data["states"].keys():
            all_data["states"][state] = {
                "total": {"active": 0, "confirmed": 0, "deaths": 0, "recovered": 0}
            }

        all_data["states"][state]["total"]["active"] += active
        all_data["states"][state]["total"]["confirmed"] += confirmed
        all_data["states"][state]["total"]["deaths"] += deaths
        all_data["states"][state]["total"]["recovered"] += recovered

        all_data["states"][state][location] = {
            "active": active,
            "confirmed": confirmed,
            "deaths": deaths,
            "recovered": recovered,
        }
    return all_data

