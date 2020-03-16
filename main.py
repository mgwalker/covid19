import chevron
import json
from math import log
import requests

time_series = requests.get("https://covidtracking.com/api/us/daily").json()
time_series = [
    {"date": date["date"], "total": date["positive"]} for date in time_series
]

prev = 0
for date in time_series:
    if prev == 0:
        date["change_percent"] = 0
        date["change"] = 0
        prev = date["total"]
        continue

    date["change_percent"] = (date["total"] / prev) - 1
    date["change"] = round(((date["total"] / prev) - 1) * 100, 2)
    prev = date["total"]

latest_change = time_series[-1]["change"]
prev = time_series[-2]["total"]
us_total = time_series[-1]["total"]

daily_average_change = sum([day["change_percent"] for day in time_series]) / (
    len(time_series) - 1
)

recent_days = 3
recent_average_change = (
    sum([day["change_percent"] for day in time_series[-recent_days:]]) / recent_days
)

doubling = round(log(2, 1 + daily_average_change), 2)
doubling_recent = round(log(2, 1 + recent_average_change), 2)

projections_all = {
    "10_days": f'{round(time_series[-1]["total"] * ((1 + daily_average_change) ** 10)):,}',
    "20_days": f'{round(time_series[-1]["total"] * ((1 + daily_average_change) ** 20)):,}',
    "30_days": f'{round(time_series[-1]["total"] * ((1 + daily_average_change) ** 30)):,}',
}
projections_recent = {
    "10_days": f'{round(time_series[-1]["total"] * ((1 + recent_average_change) ** 10)):,}',
    "20_days": f'{round(time_series[-1]["total"] * ((1 + recent_average_change) ** 20)):,}',
    "30_days": f'{round(time_series[-1]["total"] * ((1 + recent_average_change) ** 30)):,}',
}

states = requests.get("https://covidtracking.com/api/states").json()

state_max = max([state["positive"] for state in states])

state_data = {}
with open("states.css", "w") as css:
    for state in states:
        state_data[state["state"]] = {
            "death": state["death"],
            "positive": state["positive"],
            "negative": state["negative"],
            "total": state["total"],
        }

        proportion = state["positive"] / state_max
        not_blue = round(211 * (1 - proportion))
        css.write(
            f'.{state["state"]}, .{state["state"]} * {{ fill: rgb({not_blue}, {not_blue}, 211); }}\n'
        )
css.close()

with open("index.mustache", "r") as template:
    with open("index.html", "w") as index:
        index.write(
            chevron.render(
                template,
                {
                    "doubling": doubling,
                    "doubling_recent": doubling_recent,
                    "percent_change": latest_change,
                    "prev": f"{prev:,}",
                    "projections_all": projections_all,
                    "projections_recent": projections_recent,
                    "recent_days": recent_days,
                    "state_data": json.dumps(state_data),
                    "total": f"{us_total:,}",
                },
            )
        )
        index.close()
    template.close()
