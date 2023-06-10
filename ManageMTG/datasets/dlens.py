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


def momir_legal(all_cards_df: pd.DataFrame) -> pd.DataFrame:
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
        "h19"
        "fh18"
        "ph18",
        "ph19",
        "ph20",
        "j17",
        "hho"
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


def get_missing(all_df: pd.DataFrame, collected_df: pd.DataFrame) -> pd.Series:
    missing_df = all_df[~all_df["name"].isin(collected_df["name"])]
    missing_names = missing_df['name'].drop_duplicates().reset_index(drop=True)

    return missing_names


def get_ck_by_card(df: pd.DataFrame) -> pd.DataFrame:
    name_df = df.set_index('name')
    name_df['set'] = name_df['sku'].str.split('-').str[0]
    name_df['price'] = name_df['price_retail']
    min_prices = name_df.sort_values('price').groupby('name')['price'].head(1)
    edition = name_df.groupby('name')['set'].apply(set)
    combined = pd.concat([min_prices, edition], axis=1)
    combined = combined.sort_values('name').reset_index()

    return combined


def main():
    apk_df = sql_to_df("downloads/delverlens_apk.db", "cards")
    dlens_df = sql_to_df("downloads/momir.dlens", "cards")
    scryfall_df = pd.read_json("downloads/scryfall.json").set_index("id")
    ck_df = pd.read_parquet('downloads/ck/100623.parquet')

    # Join scryfall id onto delverlens file, joining by name
    db_df = apk_df[["_id", "scryfall_id"]].set_index("_id", drop=False)
    db_df = db_df.join(scryfall_df, on="scryfall_id")
    momir_df = momir_legal(db_df)

    collected_df = dlens_df[["card"]].set_index("card").join(db_df, on="card").reset_index()
    missing_names = get_missing(momir_df, collected_df)
    missing_names_ck = missing_names.str.split(' // ').str[0]

    ck_df = get_ck_by_card(ck_df)
    missing_ck = ck_df[ck_df.name.isin(missing_names_ck)]


    # missing_ck = missing_ck.sort_values('price', ascending=False).reset_index()

    missing_ck.to_csv('downloads/missing.csv', index=False)


if __name__ == "__main__":
    main()
