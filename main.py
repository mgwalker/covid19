import chevron
import json
from math import log
import requests

from state_data import names, population

us_population = sum(population.values())

time_series = requests.get("https://covidtracking.com/api/us/daily").json()
time_series = [
    {"date": date["date"], "total": date["positive"]} for date in time_series
]

states = requests.get("https://covidtracking.com/api/states").json()

state_max = max(
    [
        state["positive"]
        for state in states
        if state["positive"] != None and state["positive"] > 0
    ]
)
proportions = [
    state["positive"] / population[state["state"]]
    for state in states
    if state["positive"] != None and state["positive"] > 0
]
state_max = max(proportions)
state_min = min(proportions)

per = 1
while state_min < 0.6 and state_min > 0 and per < 1000000:
    per *= 10
    state_min *= 10

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
    "10_days": f'{round(time_series[-1]["total"] * ((1 + daily_average_change) ** 10) / us_population * per):,}',
    "20_days": f'{round(time_series[-1]["total"] * ((1 + daily_average_change) ** 20) / us_population * per):,}',
    "30_days": f'{round(time_series[-1]["total"] * ((1 + daily_average_change) ** 30) / us_population * per):,}',
}
projections_recent = {
    "10_days": f'{round(time_series[-1]["total"] * ((1 + recent_average_change) ** 10) / us_population * per):,}',
    "20_days": f'{round(time_series[-1]["total"] * ((1 + recent_average_change) ** 20) / us_population * per):,}',
    "30_days": f'{round(time_series[-1]["total"] * ((1 + recent_average_change) ** 30) / us_population * per):,}',
}

state_data = {}
with open("states.css", "w") as css:
    for state in states:
        proportion = (state["positive"] or 0) / population[state["state"]]
        scaled_proportion = proportion / state_max

        not_blue = round(211 * (1 - scaled_proportion))
        css.write(
            f'.{state["state"]}, .{state["state"]} * {{ fill: rgb({not_blue}, {not_blue}, 211); }}\n'
        )

        state_data[state["state"]] = {
            "death": f'{state["death"] or 0:,}',
            "name": names[state["state"]],
            "proportion": f"{round(proportion * per, 2)} cases per {per:,} people",
            "test_proportion": f'{round(state["total"] / population[state["state"]] * per)} per {per:,} people',
        }

css.close()

with open("index.mustache", "r") as template:
    with open("index.html", "w") as index:
        index.write(
            chevron.render(
                template,
                {
                    "doubling": doubling,
                    "doubling_recent": doubling_recent,
                    "per": f"{per:,}",
                    "percent_change": latest_change,
                    "prev": f"{round(prev / us_population * per, 2)}",
                    "projections_all": projections_all,
                    "projections_recent": projections_recent,
                    "recent_days": recent_days,
                    "state_data": json.dumps(state_data),
                    "total": f"{us_total:,}",
                    "total": f"{round(us_total / us_population * per, 2)} cases per {per:,} people",
                },
            )
        )
        index.close()
    template.close()
