import pandas as pd
import requests

__all_us_data = [
    {**d, "death": d["death"] if "death" in d else 0, "positive": d["positive"] or 0}
    for d in requests.get("https://covidtracking.com/api/us/daily").json()[::-1]
]

__all_states_data = [
    {**d, "death": d["death"] if "death" in d else 0, "positive": d["positive"] or 0}
    for d in requests.get("https://covidtracking.com/api/states/daily").json()[::-1]
]


def __turn_data_into_frame(data):
    data = [
        {
            **s,
            "deathIncreaseRate": round(
                (
                    s["deathIncrease"] / data[i - 1]["death"]
                    if i > 0 and data[i - 1]["death"]
                    else 0
                )
                * 100,
                2,
            ),
            "positiveIncreaseRate": round(
                (
                    s["positiveIncrease"] / data[i - 1]["positive"]
                    if i > 0 and data[i - 1]["positive"]
                    else 0
                )
                * 100,
                2,
            ),
            "totalTestResultsIncreaseRate": round(
                (
                    s["totalTestResultsIncrease"] / data[i - 1]["totalTestResults"]
                    if i > 0 and data[i - 1]["totalTestResults"]
                    else 0
                )
                * 100,
                2,
            ),
        }
        for i, s in enumerate(data)
    ]

    return pd.DataFrame(data, columns=data[0].keys())


def get_data_for_us():
    return __all_us_data


def get_dataframe_for_us():
    return __turn_data_into_frame(__all_us_data)


def get_data_for_state(state_name):
    state_data = [s for s in __all_states_data if s["state"] == state_name]
    return state_data


def get_dataframe_for_state(state_name):
    state_data = get_data_for_state(state_name)
    return __turn_data_into_frame(state_data)
