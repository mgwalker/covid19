import chevron
import requests

time_series = requests.get("https://covidtracking.com/api/us/daily").json()
time_series = [
    {"date": date["date"], "total": date["positive"]} for date in time_series
]

prev = 0
for date in time_series:
    if prev == 0:
        date["change"] = 0
        prev = date["total"]
        continue

    date["change"] = round((date["total"] / prev) - 1, 4) * 100
    prev = date["total"]

latest_change = time_series.pop()["change"]

states = requests.get("https://covidtracking.com/api/states").json()

positive = [state["positive"] for state in states]
us_total = sum(positive)
state_max = max(positive)

with open("states.css", "w") as css:
    with open("states.mustache", "r") as template:
        for state in states:
            with open(f"""states/{state["state"]}.html""", "w") as f:
                f.write(chevron.render(template, state))
                f.close()
            template.seek(0)

            proportion = state["positive"] / state_max
            not_red = round(211 * (1 - proportion))
            css.write(
                f""".{state["state"]}, .{state["state"]} * {{ fill: rgb(211, {not_red}, {not_red}); }}\n"""
            )
        template.close()
css.close()

with open("index.mustache", "r") as template:
    with open("index.html", "w") as index:
        index.write(
            chevron.render(
                template, {"percent_change": latest_change, "total": us_total}
            )
        )
        index.close()
    template.close()
