import json
import pandas as pd

PATH = "/home/luke/Documents/Code/MTGManager/src/nzmagic/shufflencut.json"
CONDENSED_PATH = "/home/luke/Documents/Code/MTGManager/src/nzmagic/order.csv"

OWNERS = {0: "Luke", 1: "Sean", 2: "Isaac", 3: "Conrad"}


def parse_file(filepath):
    with open(filepath, "r", encoding="UTF-8") as f:
        data = json.load(f)

    formatted_data = []
    for node in data["data"]["orderDetailsPageOrder"]["lineItems"][0]["lineItems"][
        "nodes"
    ]:
        item = node["lineItem"]
        name = item["name"]
        quantity = item["quantity"]
        price = item["currentTotalPrice"]["amount"]
        formatted_data.append((name, quantity, price))

    df = pd.DataFrame(formatted_data, columns=["Name", "Quantity", "Price"])
    df["Owner"] = 0
    df.to_csv(CONDENSED_PATH, index=False)


def print_totals(csv_filepath):
    df = pd.read_csv(csv_filepath)

    for owner, subdf in df.groupby("Owner"):
        owner_str = OWNERS[owner]
        print(f"\n{owner_str}: {subdf['Price'].sum()}")
        for _, row in subdf.iterrows():
            print(f"{row.Price}: {row.Quantity} x {row.Name}")


def main():
    # parse_file(PATH)
    print_totals(csv_filepath=CONDENSED_PATH)


if __name__ == "__main__":
    main()
