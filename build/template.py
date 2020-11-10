import chevron
from math import floor, log, log10
from state_data import names, population

us_population = sum(population.values())

all_states = [
    {"full_name": names[state], "short_name": state} for state in names.keys()
]


def write_data_to_template(data, file, index=False, extra_data={}):
    # try:
    location_name = "The United States" if index else names[data[0]["state"]]
    local_population = us_population if index else population[data[0]["state"]]

    recent_days = 4

    positive = data[-1]["positive"]

    __nearer = [d["positive"] for d in data[-recent_days:]]
    __further = [d["positive"] for d in data[-1 - recent_days : -1]]
    recent_average_change = (
        sum([n / f if f > 0 else 0 for n, f in zip(__nearer, __further)]) / recent_days
    )
    increase_recent = sum([d["positiveIncrease"] for d in data[-5:]]) / 5
    seven_days = positive + (increase_recent * 7)
    if seven_days > 0:
        seven_days = round(seven_days, 1 - int(floor(log10(seven_days))))

    proportion = positive / local_population

    increase = data[-1]["positiveIncrease"]
    increase_rate = (
        round(100 * increase / data[-2]["positive"], 1)
        if data[-2]["positive"] > 0
        else 0
    )

    per = 1
    while proportion < 1 and proportion > 0:
        proportion *= 10
        per *= 10
    proportion = round(proportion)

    deaths = data[-1]["death"]

    __nearer = [d["death"] for d in data[-recent_days:]]
    __further = [d["death"] for d in data[-1 - recent_days : -1]]
    death_recent_average_change = (
        sum([n / f if f > 0 else 0 for n, f in zip(__nearer, __further)]) / recent_days
    )
    death_increase_recent = sum([d["deathIncrease"] for d in data[-5:]]) / 5
    death_seven_days = deaths + (death_increase_recent * 7)
    if death_seven_days > 0:
        death_seven_days = round(
            death_seven_days, 1 - int(floor(log10(death_seven_days)))
        )

    with open("index.mustache", "r") as template:
        with open(file, "w") as output:
            output.write(
                chevron.render(
                    template,
                    {
                        **extra_data,
                        "all_states": all_states,
                        "cases": {
                            "change_rate": {
                                "rate": f"{round(increase_recent):,}",
                                "seven_days": f"{round(seven_days):,}",
                            },
                            "proportion": {"count": proportion, "per": f"{per:,}"},
                            "total": f"{positive:,}",
                        },
                        "deaths": {
                            "change_rate": {
                                "rate": f"{round(death_increase_recent):,}",
                                "seven_days": f"{round(death_seven_days):,}",
                            },
                            "fatality_rate": round(100 * deaths / positive, 2)
                            if positive > 0
                            else 0,
                            "total": f"{deaths:,}",
                        },
                        "index": index,
                        "location": location_name,
                        "short_name": "USA" if index else data[0]["state"],
                    },
                )
            )
            output.close()
        template.close()


# except e:
#     print(f'failed on writing "{file}"')
