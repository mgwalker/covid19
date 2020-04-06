import chevron
from math import log
from state_data import names, population

us_population = sum(population.values())

all_states = [
    {"full_name": names[state], "short_name": state} for state in names.keys()
]


def write_data_to_template(data, file, index=False, extra_data={}):
    try:
        location_name = "The United States" if index else names[data[0]["state"]]
        local_population = us_population if index else population[data[0]["state"]]

        recent_days = 4
        __nearer = [d["positive"] for d in data[-recent_days:]]
        __further = [d["positive"] for d in data[-1 - recent_days : -1]]
        recent_average_change = (
            sum([n / f if f > 0 else 0 for n, f in zip(__nearer, __further)])
            / recent_days
        )
        doubling_recent = (
            log(2, recent_average_change) if recent_average_change > 1 else 0
        )
        seven_days = data[-1]["positive"] * (recent_average_change ** 7)

        positive = data[-1]["positive"]
        proportion = positive / local_population

        per = 1
        while proportion < 1 and proportion > 0:
            proportion *= 10
            per *= 10
        proportion = round(proportion)

        with open("index.mustache", "r") as template:
            with open(file, "w") as output:
                output.write(
                    chevron.render(
                        template,
                        {
                            **extra_data,
                            "index": index,
                            "location": location_name,
                            "total": f"{positive:,}",
                            "proportion": {"count": proportion, "per": f"{per:,}"},
                            "change_rate": {
                                "doubling": round(doubling_recent, 1),
                                "rate": round((recent_average_change - 1) * 100, 1),
                                "seven_days": f"{round(seven_days):,}",
                            },
                            "short_name": "USA" if index else data[0]["state"],
                            "all_states": all_states,
                        },
                    )
                )
                output.close()
            template.close()
    except:
        print(f'failed on writing "{file}"')
