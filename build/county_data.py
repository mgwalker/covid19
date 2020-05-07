import csv
from math import floor, log, log10
import requests
from io import StringIO

__url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"

__csv_data = requests.get(__url)
__csv_reader = csv.reader(StringIO(__csv_data.text))
next(__csv_reader)  # remove headers

__counties_json = {}
for row in __csv_reader:
    date, county, state, fips, cases, deaths = row
    if county == "Unknown":
        continue

    locale = f"{county}, {state}"
    if not locale in __counties_json:
        __counties_json[locale] = {"fips": fips, "cases": [], "deaths": []}
    __counties_json[locale]["cases"].append(int(cases))
    __counties_json[locale]["deaths"].append(int(deaths))

__recent_days = 7

for locale in __counties_json:
    c = __counties_json[locale]
    c["new_cases"] = [
        cases - c["cases"][i - 1] if i > 0 else cases
        for i, cases in enumerate(c["cases"])
    ]
    c["new_deaths"] = [
        deaths - c["deaths"][i - 1] if i > 0 else deaths
        for i, deaths in enumerate(c["deaths"])
    ]

    c["new_case_rate"] = []
    c["new_death_rate"] = []

    for i in range(0, len(c["cases"])):
        if i == 0:
            c["new_case_rate"].append(0)
            c["new_death_rate"].append(0)
        else:
            cases_rate = (
                c["new_cases"][i] / c["cases"][i - 1] if c["cases"][i - 1] > 0 else 0
            )
            c["new_case_rate"].append(round(100 * cases_rate, 2))

            death_rate = (
                c["new_deaths"][i] / c["deaths"][i - 1] if c["deaths"][i - 1] > 0 else 0
            )
            c["new_death_rate"].append(round(100 * death_rate, 2))

    recent_average_change = sum(c["new_case_rate"][-__recent_days:]) / __recent_days
    c["recent_new_case_rate"] = round(recent_average_change, 2)
    c["new_case_doubling"] = round(
        log(2, 1 + (recent_average_change / 100)) if recent_average_change > 0 else 0, 2
    )
    seven_days = round(c["cases"][-1] * ((1 + (recent_average_change / 100)) ** 7))
    if seven_days > 0:
        seven_days = round(seven_days, 1 - int(floor(log10(seven_days))))
    c["cases_in_7_days"] = f"{seven_days:,}"
    c["current_cases"] = f'{c["cases"][-1]:,}'

    recent_average_change = sum(c["new_death_rate"][-__recent_days:]) / __recent_days
    c["recent_new_death_rate"] = round(recent_average_change, 2)
    c["new_death_doubling"] = round(
        log(2, 1 + (recent_average_change / 100)) if recent_average_change > 0 else 0, 2
    )
    seven_days = round(c["deaths"][-1] * ((1 + (recent_average_change / 100)) ** 7))
    if seven_days > 0:
        seven_days = round(seven_days, 1 - int(floor(log10(seven_days))))
    c["death_in_7_days"] = f"{seven_days:,}"
    c["current_deaths"] = f'{c["deaths"][-1]:,}'

sorted_locales_by_cases = [
    locale
    for locale in list(__counties_json.keys())
    if __counties_json[locale]["cases"][-1] > 500
]
sorted_locales_by_cases.sort(
    key=lambda locale: __counties_json[locale]["recent_new_case_rate"], reverse=True
)

sorted_locales_by_death = [
    locale
    for locale in list(__counties_json.keys())
    if __counties_json[locale]["deaths"][-1] > 100
]
sorted_locales_by_death.sort(
    key=lambda locale: __counties_json[locale]["recent_new_death_rate"], reverse=True
)

all_counties = __counties_json
