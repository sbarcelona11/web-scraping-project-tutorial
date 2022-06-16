# your app code here
import pandas as pd
import requests
from bs4 import BeautifulSoup
import sqlite3

url = 'https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue'
data = requests.get(url).text
bs = BeautifulSoup(data, 'html.parser')
tables = bs.find_all('table')

pd_tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])
for index, table in enumerate(tables):
    if ("Tesla Quarterly Revenue" in str(table)):
        for row in table.tbody.find_all("tr"):
            col = row.find_all("td")
            # if col have len and revenue
            if len(col) and col[1].text != '':
                Date = col[0].text
                Revenue = col[1].text.replace("$", "").replace(",", "")
                aux_df = pd.DataFrame([{"Date": Date, "Revenue": Revenue}])
                pd_tesla_revenue = pd.concat([pd_tesla_revenue, aux_df], axis=0)

# List of records
records_to_store = list(pd_tesla_revenue.to_records(index=False))
# Generate DB
db = sqlite3.connect('Tesla.db')
cursor = db.cursor()

# Create Table
create_table = '''CREATE TABLE IF NOT EXISTS revenue (Date, Revenue)'''
cursor.execute(create_table)

# Insert data
cursor.executemany('INSERT INTO revenue VALUES (?,?)', records_to_store)
db.commit()

# Review data stored
select = '''SELECT * FROM revenue'''
data_stored = cursor.execute(select)
for el in data_stored:
    print(el)

