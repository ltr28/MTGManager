import sqlite3

import pandas as pd


"""
https://github.com/Jertzukka/dlensExporter/blob/master/main.py
"""


def sql_to_df(filename: str, table: str) -> pd.DataFrame:
    sql = sqlite3.connect(filename).cursor()
    sql.execute(f"SELECT * from {table};")
    all_data = sql.fetchall()

    sql.execute(f"PRAGMA table_info({table});")
    table_info = sql.fetchall()
    column_names = [column_info[1] for column_info in table_info]

    df = pd.DataFrame(all_data, columns=column_names)

    return df


def filter_all_to_momir_df(all_cards_df):
    all_sets = list(all_cards_df["set"].unique())
    bad_sets = [
        "und",
        "uns",
        "unf",
        "unh",
        "ugl",
        "40k",
        "ust",
        "uplist",
        "hbg",
        "sld",
        "cmb1",
        "cmb2",
        "bot",
        "ptg",
        "h17",
        "ph18",
        "ph19",
        "ph20",
        "j17",
    ]
    for mtg_set in all_sets:
        if isinstance(mtg_set, str) and "p" + mtg_set in all_sets:
            bad_sets.append("p" + mtg_set)

    all_momir_df = all_cards_df[
        all_cards_df["type_line"].str.split("//").str[0].str.contains("Creature")
        == True
    ]
    all_momir_df = all_momir_df[
        all_momir_df["type_line"].str.contains("Token") == False
    ]
    all_momir_df = all_momir_df[~all_momir_df["set"].isin(bad_sets)]
    all_momir_df = all_momir_df[~all_momir_df["name"].str.startswith("A-")]
    all_momir_df = all_momir_df[all_momir_df["games"].astype(str).str.contains("paper")]
    return all_momir_df


def get_missing_df():
    apk_df = sql_to_df("downloads/delverlens_apk.db", "cards")
    dlens_df = sql_to_df("downloads/momir.dlens", "cards")
    scryfall_df = pd.read_json("downloads/scryfall.json").set_index("id")

    # Join scryfall id onto delverlens file, joining by name
    db_df = apk_df[["_id", "scryfall_id"]].set_index("_id", drop=False)
    db_df = db_df.join(scryfall_df, on="scryfall_id")

    all_momir_df = filter_all_to_momir_df(db_df)
    collected_df = dlens_df[["card"]].set_index("card").join(db_df, on="card")
    not_collected_df = all_momir_df[~all_momir_df["name"].isin(collected_df["name"])]
    filtered_missing_df = not_collected_df.drop_duplicates(subset=["name", "set"])
    filtered_missing_df = filtered_missing_df.sort_values(["cmc", "name"])
    filtered_missing_df = filtered_missing_df.groupby("name")["set"].apply(",".join)
    filtered_missing_df.to_csv("downloads/missing.csv")


if __name__ == "__main__":
    get_missing_df()
