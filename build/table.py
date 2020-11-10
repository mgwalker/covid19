import chevron
from data import get_dataframe_for_state
from state_data import names, population


def write_table():
    all_states = []
    for state in names.keys():
        d = get_dataframe_for_state(state)
        d.drop(d[d.projected == "yes"].index, inplace=True)

        avg_cases_per_day = (
            1000000 * d["positiveIncreaseAverage"].tolist()[-1] / population[state]
        )
        avg_deaths_per_day = (
            1000000 * d["deathIncreaseAverage"].tolist()[-1] / population[state]
        )
        avg_positive_test_rate = d["positiveTestRateAverage"].tolist()[-1]

        all_states.append(
            {
                "state": names[state],
                "avg_cases_per_day": f"{round(avg_cases_per_day):,}",
                "avg_deaths_per_day": f"{round(avg_deaths_per_day):,}",
                "avg_positive_test_rate": f"{round(avg_positive_test_rate*100,2)}%",
            }
        )

    with open("table.mustache", "r") as template:
        with open("docs/table.html", "w") as output:
            output.write(
                chevron.render(
                    template,
                    {
                        "data": all_states,
                        "all_states": [
                            {"full_name": full, "short_name": short}
                            for (short, full) in names.items()
                        ],
                    },
                )
            )
            output.close()
        template.close()
