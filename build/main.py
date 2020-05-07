from data import (
    get_dataframe_for_state,
    get_data_for_all_states,
    get_data_for_state,
    get_dataframe_for_us,
    get_data_for_us,
)
from graph import graph_data_to_file
from math import log
import seaborn
from state_data import names
from template import write_data_to_template

recent_days = 4
states_by_increase = []
for state in names.keys():
    df = get_dataframe_for_state(state)
    recent_change = (
        sum(df["positiveIncreaseRate"].tolist()[-recent_days:]) / recent_days
    )
    pct = 1 + (recent_change / 100)
    doubling = round(log(2, pct) if recent_change > 1 else 0, 1)
    in_seven = df["positive"].tolist()[-1] * (pct ** 7)
    states_by_increase.append(
        {
            "state": names[state],
            "rate": round(recent_change, 1) or 0,
            "doubling": round(doubling, 1),
            "today": f"{df['positive'].tolist()[-1]:,}",
            "seven_days": f"{round(in_seven):,}",
        }
    )

states_by_increase.sort(key=lambda d: d["rate"], reverse=True)
fastest = states_by_increase.pop(0)
second = states_by_increase.pop(0)

graph_data_to_file(get_dataframe_for_us(), "docs/graphs/USA")
write_data_to_template(
    get_data_for_us(),
    "docs/index.html",
    True,
    {
        "fastest_state": fastest,
        "second_fastest": second,
        "other_states": states_by_increase,
    },
)

for state in names.keys():
    data = get_data_for_state(state)
    data_frame = get_dataframe_for_state(state)

    graph_data_to_file(data_frame, f"docs/graphs/{state}")
    write_data_to_template(data, f"docs/{state}.html")
