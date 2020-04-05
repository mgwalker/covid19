import seaborn
from data import (
    get_dataframe_for_state,
    get_data_for_state,
    get_dataframe_for_us,
    get_data_for_us,
)
from graph import graph_data_to_file
from state_data import names, population
from template import write_data_to_template

graph_data_to_file(get_dataframe_for_us(), "docs/graphs/USA.png")
write_data_to_template(get_data_for_us(), "docs/index.html", True)

for state in names.keys():
    data = get_data_for_state(state)
    data_frame = get_dataframe_for_state(state)

    graph_data_to_file(data_frame, f"docs/graphs/{state}.png")
    write_data_to_template(data, f"docs/{state}.html")
