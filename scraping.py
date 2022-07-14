from gc import collect
from cian_parser import parser
import pandas as pd

links = parser.collect_links(1,3)

df = pd.DataFrame()

for flat in links:
    new = parser.collect_flat_data(flat)
    df = df.append(new, ignore_index=True)
    print(f"link: {flat} is appended")

print(df)

