from county_data import draw_county_map
from data import (
    get_counties,
    get_dataframe_for_state,
    get_data_for_state,
    get_dataframe_for_us,
    get_data_for_us,
)
from graph import graph_data_to_file
from math import fabs
from state_data import names
from table import write_table
from template import write_data_to_template

# graph_data_to_file(get_dataframe_for_us(), "docs/graphs/USA")
# write_data_to_template(
#     get_data_for_us(), "docs/index.html", True,
# )

# for state in names.keys():
#     data = get_data_for_state(state)
#     data_frame = get_dataframe_for_state(state)

#     graph_data_to_file(data_frame, f"docs/graphs/{state}")
#     write_data_to_template(data, f"docs/{state}.html")

# write_table()

scaled = 0.75

red = min((max((4 * (0.75 - scaled), 0.0)), 1.0))
blue = min((max((4 * (scaled - 0.25), 0.0)), 1.0))
green = min((max((4 * fabs(scaled - 0.5) - 1.0, 0.0)), 1.0))

red = min(max(scaled * 2, 0), 1)
green = min(max(1 - 2 * (scaled - 0.5), 0), 1)

# print(f"{red * 255} | {green * 255} | {blue * 255}")

draw_county_map(get_counties(), "build/counties.svg", "docs/graphs/counties.svg")
