import pandas as pd
import requests


def __clean_data(data):
    return {
        **data,
        "death": data["death"] if "death" in data else 0,
        "positive": data["positive"] or 0,
    }


__all_us_data = "https://covidtracking.com/api/us/daily"
__all_us_data = requests.get(__all_us_data).json()[::-1]
__all_us_data = [__clean_data(d) for d in __all_us_data]

__all_states_data = "https://covidtracking.com/api/states/daily"
__all_states_data = requests.get(__all_states_data).json()[::-1]
__all_states_data = [__clean_data(d) for d in __all_states_data]


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


def get_data_for_all_states():
    return __all_states_data


def get_data_for_state(state_name):
    state_data = [s for s in __all_states_data if s["state"] == state_name]
    return state_data


def get_dataframe_for_state(state_name):
    state_data = get_data_for_state(state_name)
    return __turn_data_into_frame(state_data)
