from lib.utils.rest_utils import download_json
from lib.utils.visualize_utils import visualize

import pandas as pd
import json


if __name__ == "__main__":
    url = "https://health.data.ny.gov/api/views/cnih-y5dw/rows.json?accessType=DOWNLOAD"
    data = download_json(url)

    # Print the Nested JSON
    print(json.dumps(data, indent=4))

    # Dump the data into a json file to be read later
    with open("../fs.json", "w") as fp:
        json.dump(data, fp, indent=4)

    # Read the data json file
    data = json.load(open("../fs.json"))

    # Convert the dataset into a pandas dataframe
    columns = [row["fieldName"] for row in data["meta"]["view"]["columns"]]
    df = pd.DataFrame(data["data"], columns=columns)

    # Get the year from Last Inspection Date
    df["year"] = pd.DatetimeIndex(df["date"]).year

    # Projection for only columns of interest
    columns_of_interest = ["facility", "total_noncritical_violations", "year"]
    df_non_critical = df[columns_of_interest]
    df_non_critical["total_noncritical_violations"] = pd.to_numeric(
        df_non_critical["total_noncritical_violations"], errors="coerce"
    )

    # Aggregating data over years for each facility
    grouped = df_non_critical.groupby(["facility", "year"]).agg({"total_noncritical_violations": ["sum"]})
    grouped.columns = ["sum_violations"]
    grouped = grouped.reset_index()

    # Finding the highest violations for every year
    idx = grouped.groupby(["year"])["sum_violations"].transform(max) == grouped["sum_violations"]
    grouped_max = grouped[idx]

    # Filtering this data to facility that were highest for more than one year
    grouped_more_than_one_year = grouped_max.groupby("facility").filter(lambda x: len(x) > 1)

    # Printing the result in console
    print(grouped_more_than_one_year)

    # Visualizing the result as a bar chart
    visualize(grouped_more_than_one_year)
