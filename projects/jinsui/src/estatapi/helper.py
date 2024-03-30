import pandas as pd

__all__ = [
    "json_to_df",
]


def _get_single_mapper(series: pd.Series) -> dict:
    return {series["CLASS.@code"]: series["CLASS.@name"]}


def _get_multiple_mapper(series: pd.Series) -> dict:
    return pd.DataFrame(series["CLASS"]).set_index("@code")["@name"].to_dict()


def _get_mapper(series: pd.Series) -> dict:
    if pd.isna(series["CLASS.@code"]):
        return _get_multiple_mapper(series)
    else:
        return _get_single_mapper(series)


def _get_mappers(df_meta_info: pd.DataFrame) -> dict[str, dict]:
    mappers = {}
    for _index, row in df_meta_info.iterrows():
        column_name = "@" + row["@id"]
        mapper = _get_mapper(row)

        mappers[column_name] = mapper

    return mappers


def _get_column_name_mapper(df_meta_info: pd.DataFrame) -> dict:
    return df_meta_info.set_index("@id")["@name"].add_prefix("@").to_dict()


def json_to_df(meta_info: dict, stats_data: dict) -> pd.DataFrame:
    # meta_info to df
    df_meta_info = pd.json_normalize(
        meta_info,
        record_path="GET_META_INFO.METADATA_INF.CLASS_INF.CLASS_OBJ".split("."),
    )

    # get mappers
    mappers = _get_mappers(df_meta_info)
    column_name_mapper = _get_column_name_mapper(df_meta_info)
    del df_meta_info

    # stats_data to df
    df_stats_data = pd.json_normalize(
        stats_data,
        record_path="GET_STATS_DATA.STATISTICAL_DATA.DATA_INF.VALUE".split("."),
    )

    # apply mappers
    for column_name, mapper in mappers.items():
        df_stats_data[column_name] = df_stats_data[column_name].map(mapper)

    # rename columns
    df_stats_data.rename(columns=column_name_mapper, inplace=True)

    return df_stats_data
