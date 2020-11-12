from io import StringIO
import requests
import pandas
from graph import graph_data_to_file
from table import write_table
from template import write_data_to_template

__meta = "https://mgwalker.github.io/covid19-csv/index.json"
__meta = requests.get(__meta).json()

all_states = [{"code": state, "name": __meta[state]["name"]} for state in __meta.keys()]
table_data = []

for (state, meta) in __meta.items():

    __state_data = requests.get(meta["link"])
    __state_data = pandas.read_csv(StringIO(__state_data.text))
    __state_data["index"] = range(len(__state_data))

    __state_data["projected"] = [
        "yes" if d is True else "no" for d in __state_data["projected"]
    ]

    graph_data_to_file(
        data=__state_data, file=f"docs/graphs/{state}", withTotals=state == "US"
    )

    # For now, just assume there are 14 projected days. Index starts at 0,
    # so go back 15 from the length.
    current = __state_data.iloc[len(__state_data.index) - 15]
    current = current.to_dict()
    future = __state_data.iloc[len(__state_data.index) - 8]
    future = future.to_dict()

    table_data.append(
        {
            "state": meta["name"],
            "deaths_per_million_per_day": (
                f"{round(current['deathIncreaseAveragePerMillion']):,}"
            ),
            "positive_per_million_per_day": (
                f"{round(current['positiveIncreaseAveragePerMillion']):,}"
            ),
        }
    )

    filename = "index" if state == "US" else state

    write_data_to_template(
        state=state,
        current=current,
        future=future,
        file=f"docs/{filename}.html",
        index=state == "US",
        state_list=all_states,
    )

write_table(data=table_data, state_list=all_states)
