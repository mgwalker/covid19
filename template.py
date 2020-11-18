import chevron


def write_data_to_template(
    *,
    state,
    state_name,
    current,
    future,
    far_future,
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
                "seven_days": f"{round(future['positiveIncrease']):,}",
                "fourteen_days": f"{round(far_future['positiveIncrease']):,}",
            },
            "proportion": {
                "count": f"{current['positivePerMillion']:,}",
                "per": f"{1_000_000:,}",
            },
            "today_plural": False if current["positiveIncrease"] == 1 else True,
            "today": f"{current['positiveIncrease']:,}",
            "total": f"{positive:,}",
        },
        "deaths": {
            "change_rate": {
                "rate": f"{round(current['deathIncreaseAverage']):,}",
                "seven_days": f"{round(future['deathIncrease']):,}",
                "fourteen_days": f"{round(far_future['deathIncrease']):,}",
            },
            "fatality_rate": round(100 * deaths / positive, 2) if positive > 0 else 0,
            "today_plural": False if current["deathIncrease"] == 1 else True,
            "today": f"{current['deathIncrease']:,}",
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
