"""Data-preparation helpers for the ticket/passenger dataset.

Functions in this module clean column names and values, bucket ages into
ranges and generations, and report rows with excessive missing values.
Configurable values (generation bins/labels, null threshold) live in
``config``.
"""

import pandas as pd

import config


def prepare_df(df):
    """Rename and normalize the ticket-count column.

    Renames ``Number_of_Person`` to ``Tickets_Bought`` and converts the
    value ``"Alone"`` to ``1`` so the column is fully numeric.

    Args:
        df (pd.DataFrame): Raw data containing a ``Number_of_Person`` column.

    Returns:
        pd.DataFrame: The same DataFrame (modified in place) with an
        ``int64`` ``Tickets_Bought`` column.

    Raises:
        ValueError: If the column contains values that are neither numeric
            nor ``"Alone"``.
        pd.errors.IntCastingNaNError: If the column contains missing values.
    """
    df.rename(columns={"Number_of_Person": "Tickets_Bought"}, inplace=True)

    # Treat "Alone" as a single ticket, then cast the column to integers.
    df["Tickets_Bought"] = pd.to_numeric(
        df["Tickets_Bought"].replace("Alone", 1)
    ).astype("int64")

    return df


def sort_age_type(df):
    """Bucket ages into ranges: 18-25, then 5-year bands (26-30, 31-35, ...).

    The upper bound is the oldest age rounded up to the next multiple of 5,
    so every age from 18 to the maximum is assigned a band.

    Args:
        df (pd.DataFrame): Data containing a numeric ``Age`` column.

    Returns:
        pd.DataFrame: The same DataFrame with a categorical ``age_type``
        column added. Ages below 18 are set to NaN.
    """
    # Round the oldest age up to the nearest multiple of 5 (minimum 25).
    max_age = max(25, int(df["Age"].max()))
    upper_limit = ((max_age + 4) // 5) * 5

    # Edges: 17, 25, 30, 35, ... -> intervals (17, 25], (25, 30], (30, 35], ...
    bins = [17, 25] + list(range(30, upper_limit + 1, 5))
    labels = ["18-25"] + [
        f"{bins[i] + 1}-{bins[i + 1]}"
        for i in range(1, len(bins) - 1)
    ]

    # right=True (the default) makes the right edge inclusive, matching the labels.
    df["age_type"] = pd.cut(df["Age"], bins=bins, labels=labels, right=True)

    return df


def sort_generation(df):
    """Assign each row a generation label based on age.

    Bin edges and labels come from ``config.bins`` and ``config.labels``.

    Args:
        df (pd.DataFrame): Data containing a numeric ``Age`` column.

    Returns:
        pd.DataFrame: The same DataFrame with a categorical ``Generation``
        column added. Ages outside the configured bins are set to NaN.
    """
    df["Generation"] = pd.cut(
        df["Age"],
        bins=config.bins,
        labels=config.labels,
    )

    return df


def flag_nulls(df):
    """Report rows with at least ``config.null_count`` missing values.

    Prints an alert and the offending rows (with an added ``Null_Count``
    column) if any are found. This is a non-blocking check: the pipeline
    always continues.

    Args:
        df (pd.DataFrame): Data to inspect. Not modified.

    Returns:
        bool: Always ``True``.
    """
    threshold = config.null_count
    null_count = df.isnull().sum(axis=1)

    # Copy so adding Null_Count doesn't touch the original DataFrame.
    flagged_rows = df[null_count >= threshold].copy()
    flagged_rows["Null_Count"] = null_count[null_count >= threshold]

    if not flagged_rows.empty:
        print(f"ALERT: {len(flagged_rows)} row(s) have {threshold} or more nulls:")
        print(flagged_rows)
    else:
        print(f"No rows have {threshold} or more nulls.")

    print("Pipeline continuing...")
    return True
