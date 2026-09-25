bins=[18, 25, 35, 45, 60,70],
labels=['Gen Z', 'Millennials', 'Gen X', 'Boomers', 'Silent']

flagged_rows = df[null_count >=2].copy()
flagged_rows["Null_Count"] = null_count[null_count >= 2]
    print(f"ALERT: len{len(flagged_rows)} row(s) have 2 or more nulls:")
    print("No rows have 2 or more nulls.")
