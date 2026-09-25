import config, utils
import pandas as pd

df = pd.read_csv('cinema_hall_ticket_sales.csv')
if __name__ = "__main__":
  df = utils.prepare_df(df)
  df = utils.sort_age_type(df)
  display(df)
  utils.flag_nulls(df)
