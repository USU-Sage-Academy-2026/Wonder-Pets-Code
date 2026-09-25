!mamba install pandas
import pandas as pd
import config
df = pd.read_csv('cinema_hall_ticket_sales.csv')

#changes number of persons to tickets bought
df.rename(columns={"Number_of_Person": "Tickets_Bought"},inplace=True)

#changes the word alone to the number one
df['Tickets_Bought'] = pd.to_numeric(
  df['Tickets_Bought'].replace('Alone', 1)    
).astype("int64")

#code taken out of jupiter 
max_age = max(25, int(df['Age'].max()))
upper_limit = ((max_age + 4) // 5) * 5

bins = [17, 25] + list(range(30, upper_limit + 1, 5))
labels = ['18-25'] + [
    f'{bins[i] + 1}-{bins[i + 1]}'
    for i in range(1, len(bins) - 1)
]
df['age_type'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)

# Define your bin boundaries and matching labels
df['Generation'] = pd.cut(
    df['Age'],
    bins=config.bins,
    labels=config.labels
)
display(df)

#check for null values
null_count = df.isnull().sum(axis=1)

flagged_rows = df[null_count >=config.null_count].copy()
flagged_rows["Null_Count"] = null_count[null_count >= config.null_count]

if not flagged_rows.empty:
  print(f"ALERT: len{len(flagged_rows)} row(s) have "+str(config.null_count)+" or more nulls:")
  print("flagged_rows")

else:
  print("No rows have "+str(config.null_count)+" or more nulls.")

print("Pipeline continuing...")
