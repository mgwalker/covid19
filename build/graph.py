import pandas as pd
import matplotlib.pyplot as plt
import requests
import seaborn as sns


plt.figure(figsize=(15, 7.5))


def graph_data_to_file(data, file):
    sns.set_context(rc={"lines.linewidth": 5})
    plot = sns.scatterplot(
        x="index", y="positiveIncrease", data=data, color="#0088FF", ci=None,
    )
    plot = sns.lineplot(
        x="index", y="positiveIncreaseAverage", data=data, color="#0088FF", ci=None
    )

    # plot = sns.scatterplot(
    #     x="index", y="deathIncrease", data=data, color="#FF8800", ci=None,
    # )
    # plot = sns.lineplot(
    #     x="index", y="deathIncreaseAverage", data=data, color="#FF8800", ci=None
    # )

    plot.set(ylabel="infections per day", xlabel="time")
    plot.grid(True)

    plot.set_xticklabels(["" for x in plot.get_xticks()])
    plot.set_yticklabels([f"{y:,.0f}" for y in plot.get_yticks()])

    plot.get_figure().savefig(f"{file}-cases.png")
    plot.get_figure().clf()

    plot = sns.scatterplot(
        x="index", y="deathIncrease", data=data, color="#FF8800", ci=None,
    )
    plot = sns.lineplot(
        x="index", y="deathIncreaseAverage", data=data, color="#FF8800", ci=None
    )

    plot.set(ylabel="deaths per day", xlabel="time")
    plot.grid(True)

    plot.set_xticklabels(["" for x in plot.get_xticks()])
    plot.set_yticklabels([f"{y:,.0f}" for y in plot.get_yticks()])

    plot.get_figure().savefig(f"{file}-deaths.png")
    plot.get_figure().clf()
