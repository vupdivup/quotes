import pandas as pd
import os

df = pd.read_json("raw/quotes.json")

df.quote = df.quote.apply(
    # the split and rejoin removes any extra whitespace
    lambda x: " ".join(x.split()).removesuffix(" ~")
)

# limit quote length
df = df[
    (df.quote.str.len() > 100) &
    (df.quote.str.len() < 250)
]

# TODO: replace hyphens
# TODO: filter out untypable chars

dest = input("Destination: ")

os.makedirs(os.path.dirname(dest), exist_ok=True)

# write to json
with open(dest + ".json", "w") as f:
    df.to_json(f, orient="records", indent=4)