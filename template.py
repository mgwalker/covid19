import chevron


def write_data_to_template(
    *,
    state,
    state_name,
    current,
    future,
    file,
    index=False,
    state_list=[],
    extra_data={},
):
    location_name = "The United States" if index else state_name

    deaths = current["deaths"]
    positive = current["positive"]

    data = {
        **extra_data,
        "all_states": state_list,
        "cases": {
            "change_rate": {
                "rate": f"{round(current['positiveIncreaseAverage']):,}",
                "seven_days": f"{round(future['positive']):,}",
            },
            "proportion": {
                "count": f"{current['positivePerMillion']:,}",
                "per": f"{1_000_000:,}",
            },
            "total": f"{positive:,}",
        },
        "deaths": {
            "change_rate": {
                "rate": f"{round(current['deathIncreaseAverage']):,}",
                "seven_days": f"{round(future['deaths']):,}",
            },
            "fatality_rate": round(100 * deaths / positive, 2) if positive > 0 else 0,
            "total": f"{deaths:,}",
        },
        "index": index,
        "location": location_name,
        "short_name": state,
    }

    with open("index.mustache", "r") as template:
        with open(file, "w") as output:
            output.write(chevron.render(template, data))
            output.close()
        template.close()


# except e:
#     print(f'failed on writing "{file}"')
