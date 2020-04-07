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

        increase = data[-1]["positiveIncrease"]
        increase_rate = (
            round(100 * increase / data[-2]["positive"], 1)
            if data[-2]["positive"] > 0
            else 0
        )
        increase_yesterday = data[-2]["positiveIncrease"]
        increase_yesterday_rate = (
            round(100 * increase_yesterday / data[-3]["positive"], 1)
            if data[-3]["positive"] > 0
            else 0
        )

        increase_diff = increase_rate - increase_yesterday_rate
        increase_change = (
            "about the same as"
            if abs(increase_diff) < 0.2
            else ("a little higher than" if increase_diff < 1 else "higher than")
            if increase_diff > 0
            else ("a little lower than" if increase_diff > -1 else "lower than")
        )

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
                            "all_states": all_states,
                            "change_rate": {
                                "doubling": round(doubling_recent, 1),
                                "rate": round((recent_average_change - 1) * 100, 1),
                                "seven_days": f"{round(seven_days):,}",
                            },
                            "increase": f"{increase:,}",
                            "increase_change": increase_change,
                            "increase_rate": increase_rate,
                            "increase_yesterday": f"{increase_yesterday:,}",
                            "increase_yesterday_rate": increase_yesterday_rate,
                            "index": index,
                            "location": location_name,
                            "proportion": {"count": proportion, "per": f"{per:,}"},
                            "short_name": "USA" if index else data[0]["state"],
                            "total": f"{positive:,}",
                        },
                    )
                )
                output.close()
            template.close()
    except:
        print(f'failed on writing "{file}"')
