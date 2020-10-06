import matplotlib.pyplot as plt


def visualize(data):
    xvalues = data["year"].tolist()
    yvalues = data["sum_violations"].tolist()

    x_pos = [i for i, _ in enumerate(xvalues)]
    plt.bar(x_pos, yvalues, color="#276FBF", label=data["facility"].tolist()[0])

    plt.title("Yearly non-critical violations", fontsize=16)
    plt.xlabel("Year", fontsize=14)
    plt.ylabel("Total # of non-critical violations", fontsize=14)
    plt.xticks(x_pos, xvalues)
    plt.legend(loc="best")

    # put the actual value labels on top of the bars - make it reader friendly
    for index, value in enumerate(yvalues):
        plt.text(index - 0.1, value + 2, str(int(value)))

    # plt.show()
    plt.savefig("../barchart.png", bbox_inches="tight")
