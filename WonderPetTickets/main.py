import config
import utils
import pandas as pd


def main():
    """Run the cinema ticket-sales data pipeline.

    Loads the raw CSV, cleans and enriches the data, prints a preview,
    and reports any rows with excessive missing values.
    """
    df = pd.read_csv(config.DATA_PATH)

    df = utils.prepare_df(df)       # Rename columns, normalize ticket counts
    df = utils.sort_age_type(df)    # Bucket ages into 5-year bands
    df = utils.sort_generation(df)  # Assign generation labels

    print(df)
    utils.flag_nulls(df)


if __name__ == "__main__":
    main()
