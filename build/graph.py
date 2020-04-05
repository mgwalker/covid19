import pandas as pd
import matplotlib.pyplot as plt
import requests
import seaborn as sns


plt.figure(figsize=(15, 7.5))


def graph_data_to_file(data, file):
    sns.set_context(rc={"lines.linewidth": 5})
    plot = sns.lineplot(
        x="positive", y="positiveIncreaseRate", data=data, color="#0088FF", ci=None
    )
    plot = sns.lineplot(
        x="positive", y="deathIncreaseRate", data=data, color="#000000", ci=None
    )
    plot = sns.lineplot(
        x="positive",
        y="totalTestResultsIncreaseRate",
        data=data,
        color="#FF8800",
        ci=None,
    )
    plot.set(ylabel="percent change", xscale="log")
    plot.grid(True)

    plot.set_ylim(0, 100)

    plot.set_xticklabels([f"{x:,.0f}" for x in plot.get_xticks()])
    plot.set_yticklabels([f"{x:.0f}%" for x in plot.get_yticks()])

    # seaborn.set()
    # plot = seaborn.regplot(x="positive", y="increase", data=state_data, ci=None)
    # seaborn.regplot(x="positive", y="newTested", data=state_data, ci=None)
    # plot.set_title(f"{names[state]} new cases vs. total")
    plot.get_figure().savefig(file)
    plot.get_figure().clf()
