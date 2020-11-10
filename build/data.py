from math import nan
import pandas as pd
import requests
from datetime import datetime, timedelta


def __clean_data(data):
    return {
        **data,
        "death": data["death"] if "death" in data else 0,
        "positive": data["positive"] or 0 if "positive" in data else 0,
        "totalTestResults": data["totalTestResults"] or 0
        if "totalTestResults" in data
        else 0,
    }


try:
    __all_us_data = "https://covidtracking.com/api/us/daily"
    __all_us_data = requests.get(__all_us_data).json()[::-1]
    __all_us_data = [__clean_data(d) for d in __all_us_data]
    __all_us_data = [
        {
            **d,
            "positiveTestRate": d["positive"] / d["totalTestResults"]
            if d["totalTestResults"] > 0
            else 0,
        }
        for i, d in enumerate(__all_us_data)
    ]

    __all_states_data = "https://covidtracking.com/api/states/daily"
    __all_states_data = requests.get(__all_states_data).json()[::-1]
    __all_states_data = [__clean_data(d) for d in __all_states_data]
    __all_states_data = [
        {
            **d,
            "positiveTestRate": d["positive"] / d["totalTestResults"]
            if d["totalTestResults"] > 0
            else 0,
        }
        for i, d in enumerate(__all_states_data)
    ]
except:  # noqa: E722
    print("there was an error")
    exit(0)

__days_for_average = 7


def __turn_data_into_frame(data):
    data = [
        {
            **s,
            "index": i,
            "projected": "no",
            "deathIncreaseRate": round(
                (
                    s["deathIncrease"] / data[i - 1]["death"]
                    if i > 0 and data[i - 1]["death"]
                    else 0
                )
                * 100,
                2,
            ),
            "deathDailyIncrease": s["deathIncrease"] - data[i - 1]["deathIncrease"]
            if i > 0
            else 0,
            "deathIncreaseAverage": sum(
                [d["deathIncrease"] for d in data[i - __days_for_average : i]]
            )
            / __days_for_average
            if i > __days_for_average
            else s["deathIncrease"],
            "positiveIncreaseRate": round(
                (
                    s["positiveIncrease"] / data[i - 1]["positive"]
                    if i > 0 and data[i - 1]["positive"]
                    else 0
                )
                * 100,
                2,
            ),
            "positiveDailyIncrease": s["positiveIncrease"]
            - data[i - 1]["positiveIncrease"]
            if i > 0
            else 0,
            "positiveIncreaseAverage": sum(
                [d["positiveIncrease"] for d in data[i - __days_for_average : i]]
            )
            / __days_for_average
            if i > __days_for_average
            else s["positiveIncrease"],
            "positiveTestRateAverage": sum(
                [d["positiveTestRate"] for d in data[i - __days_for_average : i]]
            )
            / __days_for_average
            if i > __days_for_average
            else 0,
        }
        for i, s in enumerate(data)
    ]

    most_recent = data[-1]
    positive_increase = most_recent["positiveIncreaseAverage"]
    death_increase = most_recent["deathIncreaseAverage"]

    daily_increase_rate = sum([d["positiveDailyIncrease"] for d in data[-7:]]) / 7
    daily_death_increase_rate = sum([d["deathDailyIncrease"] for d in data[-7:]]) / 7

    for i in range(21):
        most_recent = data[-1]

        date = datetime.strptime(f'{most_recent["date"]}', "%Y%m%d")
        date = date + timedelta(1)

        positive_increase = positive_increase + daily_increase_rate
        death_increase = death_increase + daily_death_increase_rate

        positive_increase = positive_increase if positive_increase > 0 else 0
        death_increase = death_increase if death_increase > 0 else 0

        projected = {
            **most_recent,
            "index": most_recent["index"] + 1,
            "date": int(f"{date:%Y%m%d}"),
            "positive": most_recent["positive"] + positive_increase,
            "positiveIncrease": positive_increase,
            "positiveIncreaseAverage": nan,
            "death": most_recent["death"] + death_increase,
            "deathIncrease": death_increase,
            "deathIncreaseAverage": nan,
            "positiveTestRate": nan,
            "positiveTestRateAverage": nan,
            "projected": "yes",
        }

        data.append(projected)

    return pd.DataFrame(data, columns=data[0].keys())


def get_data_for_us():
    return __all_us_data


def get_dataframe_for_us():
    return __turn_data_into_frame(__all_us_data)


def get_data_for_all_states():
    return __all_states_data


def get_data_for_state(state_name):
    state_data = [s for s in __all_states_data if s["state"] == state_name]
    return state_data


def get_dataframe_for_state(state_name):
    state_data = get_data_for_state(state_name)
    return __turn_data_into_frame(state_data)
