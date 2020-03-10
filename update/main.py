import chevron
from data import get_raw_data
import json

raw_data = get_raw_data()
total = raw_data["total"]

css = open("states.css", "w")

max_state = max([s["total"]["active"] for s in raw_data["states"].values()])
print(max_state)

for state in raw_data["states"].keys():
    state_total = raw_data["states"][state]["total"]
    proportion = state_total["active"] / max_state

    not_red = round(192 * (1 - proportion))

    css.write(f""".{state}, .{state} * {{ fill: rgb(211, {not_red}, {not_red}); }}\n""")
css.close()

with open("index.mustache", "r") as mustache:
    index = open("index.html", "w")
    index.write(
        chevron.render(mustache, {"total_us_active": raw_data["total"]["active"],},)
    )
    index.close()

with open("data.json", "w") as json_file:
    json_file.write(json.dumps(raw_data, indent=2, sort_keys=True))
    json_file.close()
