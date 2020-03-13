import chevron
import requests

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
        index.write(chevron.render(template, {"total": us_total}))
        index.close()
    template.close()
