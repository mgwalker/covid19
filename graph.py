import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(15, 7.5))


def graph_data_to_file(*, data, file, withTotals=False):
    sns.set_context(rc={"lines.linewidth": 5})

    if withTotals:
        plot = sns.scatterplot(
            x="index",
            y="positive",
            data=data,
            hue="projected",
            palette={"no": "#0088FF", "yes": "#000000"},
            ci=None,
        )

        plot.set(ylabel="total infections", xlabel="time")
        plot.grid(True)

        plot.set_xticklabels(["" for x in plot.get_xticks()])
        plot.set_yticklabels([f"{y:,.0f}" for y in plot.get_yticks()])

        plot.get_figure().savefig(f"{file}-total-cases.png")
        plot.get_figure().clf()

        plot = sns.scatterplot(
            x="index",
            y="deaths",
            data=data,
            hue="projected",
            palette={"no": "#FF8800", "yes": "#000000"},
            ci=None,
        )

        plot.set(ylabel="total deaths", xlabel="time")
        plot.grid(True)

        plot.set_xticklabels(["" for x in plot.get_xticks()])
        plot.set_yticklabels([f"{y:,.0f}" for y in plot.get_yticks()])

        plot.get_figure().savefig(f"{file}-total-deaths.png")
        plot.get_figure().clf()

    plot = sns.scatterplot(
        x="index",
        y="positiveIncrease",
        data=data,
        # color="#0088FF",
        ci=None,
        hue="projected",
        palette={"no": "#0088FF", "yes": "#000000"},
    )
    plot = sns.lineplot(
        x="index",
        y="positiveIncreaseAverage",
        data=data.where(data["projected"] == "no"),
        color="#0088FF",
        ci=None,
    )

    plot.set(ylabel="infections per day", xlabel="time")
    plot.grid(True)

    plot.set_xticklabels(["" for x in plot.get_xticks()])
    plot.set_yticklabels([f"{y:,.0f}" for y in plot.get_yticks()])

    plot.get_figure().savefig(f"{file}-cases.png")
    plot.get_figure().clf()

    plot = sns.scatterplot(
        x="index",
        y="deathIncrease",
        data=data,
        color="#FF8800",
        ci=None,
        hue="projected",
        palette={"no": "#FF8800", "yes": "#000000"},
    )
    plot = sns.lineplot(
        x="index",
        y="deathIncreaseAverage",
        data=data.where(data["projected"] == "no"),
        color="#FF8800",
        ci=None,
    )

    plot.set(ylabel="deaths per day", xlabel="time")
    plot.grid(True)

    plot.set_xticklabels(["" for x in plot.get_xticks()])
    plot.set_yticklabels([f"{y:,.0f}" for y in plot.get_yticks()])

    plot.get_figure().savefig(f"{file}-deaths.png")
    plot.get_figure().clf()
