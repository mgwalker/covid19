import pandas as pd
import requests


def __clean_data(data):
    return {
        **data,
        "death": data["death"] if "death" in data else 0,
        "positive": data["positive"] or 0 if "positive" in data else 0,
    }


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

__days_for_average = 7


def __turn_data_into_frame(data):
    data = [
        {
            **s,
            "index": i,
            "deathIncreaseRate": round(
                (
                    s["deathIncrease"] / data[i - 1]["death"]
                    if i > 0 and data[i - 1]["death"]
                    else 0
                )
                * 100,
                2,
            ),
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
