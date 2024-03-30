import urllib
from enum import StrEnum

import requests

from . import helper

__all__ = [
    "get_stats_list",
    "get_meta_info",
    "get_stats_data",
]


class _APIType(StrEnum):
    getStatsList = "getStatsList"
    getMetaInfo = "getMetaInfo"
    getStatsData = "getStatsData"


def _build_endpoint(api_type: _APIType, version: str = "3.0"):
    base = f"https://api.e-stat.go.jp/rest/{version}/app/json/"
    url = urllib.parse.urljoin(base, api_type)
    return url


def get_stats_list(
    appId: str,
    surveyYears: str | None = None,
    openYears: str | None = None,
    statsField: str | None = None,
    statsCode: str | None = None,
    searchWord: str | None = None,
    searchKind: int | None = None,
    collectArea: int | None = None,
    explanationGetFlg: str | None = None,
    statsNameList: str | None = None,
    startPosition: int | None = None,
    limit: int = 5,
    updatedDate: str | None = None,
) -> dict:
    """
    Parameters
    ----------
    appId : str
        アプリケーションID
        取得したアプリケーションIDを指定して下さい。

    surveyYears : str
        調査年月
        以下のいずれかの形式で指定して下さい。
        ・yyyy：単年検索
        ・yyyymm：単月検索
        ・yyyymm-yyyymm：範囲検索

    openYears : str
        公開年月
        調査年月と同様です。

    statsField : str
        統計分野
        以下のいずれかの形式で指定して下さい。
        ・数値2桁：統計大分類で検索
        ・数値4桁：統計小分類で検索

    statsCode : str
        政府統計コード
        以下のいずれかの形式で指定して下さい。
        ・数値5桁：作成機関で検索
        ・数値8桁：政府統計コードで検索

    searchWord : str
        検索キーワード
        任意の文字列。表題やメタ情報等に含まれている文字列を検索します。
        AND、OR 又は NOT を指定して複数ワードでの検索が可能です。 (東京 AND 人口、東京 OR 大阪 等)

    searchKind : int
        検索データ種別
        検索するデータの種別を指定して下さい。
        ・1：統計情報(省略値)
        ・2：小地域・地域メッシュ

    collectArea : int
        集計地域区分
        検索するデータの集計地域区分を指定して下さい。
        ・1：全国
        ・2：都道府県
        ・3：市区町村

    explanationGetFlg : str
        解説情報有無
        統計表及び、提供統計、提供分類の解説を取得するか否かを以下のいずれかから指定して下さい。
        ・Y：取得する (省略値)
        ・N：取得しない

    statsNameList : str
        統計調査名指定
        統計表情報でなく、統計調査名の一覧を取得する場合に指定して下さい。
        ・Y：統計調査名一覧
        統計調査名一覧を出力します。
        statsNameListパラメータを省略した場合、又はY以外の値を設定した場合は統計表情報を出力します。

    startPosition : int
        データ取得開始位置
        データの取得開始位置（1から始まる行番号）を指定して下さい。省略時は先頭から取得します。
        統計データを複数回に分けて取得する場合等、継続データを取得する開始位置を指定するために指定します。
        前回受信したデータの<NEXT\_KEY>タグの値を指定します。

    limit : int
        データ取得件数
        データの取得行数を指定して下さい。省略時は10万件です。
        データ件数が指定したlimit値より少ない場合、全件を取得します。データ件数が指定したlimit値より多い場合（継続データが存在する）は、受信したデータの<NEXT\_KEY>タグに継続データの開始行が設定されます。

    updatedDate : str
        更新日付
        更新日付を指定します。指定された期間で更新された統計表の情報）を提供します。
        以下のいずれかの形式で指定して下さい。
        ・yyyy：単年検索
        ・yyyymm：単月検索
        ・yyyymmdd：単日検索
        ・yyyymmdd-yyyymmdd：範囲検索
    """
    params = locals()

    endpoint = _build_endpoint(_APIType.getStatsList)

    response = requests.get(endpoint, params=params)
    return response.json()


def get_meta_info(
    appId: str,
    statsDataId,
    explanationGetFlg: str | None = None,
) -> dict:
    """
    Parameters
    ----------
    appId : str
        アプリケーションID
        取得したアプリケーションIDを指定して下さい。

    statsDataId : str
        統計表ID
        「統計表情報取得」で得られる統計表IDです。

    explanationGetFlg : str
        統計表及び、提供統計、提供分類、各事項の解説を取得するか否かを以下のいずれかから指定して下さい。
        ・Y：取得する (省略値)
        ・N：取得しない
    """
    params = locals()

    endpoint = _build_endpoint(_APIType.getMetaInfo)

    response = requests.get(endpoint, params=params)
    return response.json()


def get_stats_data(
    appId: str,
    dataSetId=None,
    statsDataId=None,
    lvTab=None,
    cdTab=None,
    cdTabFrom=None,
    cdTabTo=None,
    lvTime=None,
    cdTime=None,
    cdTimeFrom=None,
    cdTimeTo=None,
    lvArea=None,
    cdArea=None,
    cdAreaFrom=None,
    cdAreaTo=None,
    lvCat01=None,
    cdCat01=None,
    cdCat01From=None,
    cdCat01To=None,
    startPosition=None,
    limit=100000,
    metaGetFlg="Y",
    cntGetFlg="N",
    explanationGetFlg="Y",
    annotationGetFlg="Y",
    replaceSpChar=0,
    sectionHeaderFlg=1,
    **kwargs,
):
    """
    統計データを取得する関数。

    Parameters
    ----------
    appId : str
        アプリケーションID
        取得したアプリケーションIDを指定して下さい。
    dataSetId : str, optional
        データセットID。「データセット登録」で登録したデータセットIDを指定します。
    statsDataId : str, optional
        統計表ID。「統計表情報取得」で得られる統計表IDを指定します。
    lvTab : str, optional
        絞り込み条件の階層レベル。「X」、「X-X」、「-X」、「X-」のいずれかの形式で指定します。
    cdTab : str, optional
        単一コードによる絞り込み条件。「メタ情報取得」で得られる項目コードを指定します。
        カンマ区切りで最大100個まで指定可能です。
    cdTabFrom : str, optional
        コードの範囲による絞り込み条件の開始値。
    cdTabTo : str, optional
        コードの範囲による絞り込み条件の終了値。
    lvTime : str, optional
        時間軸事項の階層レベル。表章事項の階層レベルと同様の形式で指定します。
    cdTime : str, optional
        時間軸事項の単一コード。表章事項の単一コードと同様の形式で指定します。
    cdTimeFrom : str, optional
        時間軸事項のコードの範囲の開始値。
    cdTimeTo : str, optional
        時間軸事項のコードの範囲の終了値。
    lvArea : str, optional
        地域事項の階層レベル。表章事項の階層レベルと同様の形式で指定します。
    cdArea : str, optional
        地域事項の単一コード。表章事項の単一コードと同様の形式で指定します。
    cdAreaFrom : str, optional
        地域事項のコードの範囲の開始値。
    cdAreaTo : str, optional
        地域事項のコードの範囲の終了値。
    lvCat01 : str, optional
        分類事項01の階層レベル。表章事項の階層レベルと同様の形式で指定します。
    cdCat01 : str, optional
        分類事項01の単一コード。表章事項の単一コードと同様の形式で指定します。
    cdCat01From : str, optional
        分類事項01のコードの範囲の開始値。
    cdCat01To : str, optional
        分類事項01のコードの範囲の終了値。
    startPosition : int, optional
        データ取得開始位置。1から始まる行番号を指定します。
    limit : int, optional
        データ取得件数の上限値。省略時は10万件です。
    metaGetFlg : str, optional
        メタ情報を取得するかどうかのフラグ。'Y'または'N'を指定します。
    cntGetFlg : str, optional
        件数のみを取得するかどうかのフラグ。'Y'または'N'を指定します。
    explanationGetFlg : str, optional
        解説情報を取得するかどうかのフラグ。'Y'または'N'を指定します。
    annotationGetFlg : str, optional
        注釈情報を取得するかどうかのフラグ。'Y'または'N'を指定します。
    replaceSpChar : int, optional
        特殊文字の置換方法。0(置換しない)、1(0に置換)、2(NULLに置換)、3(NAに置換)から選択します。
    callback : str, optional
        JSONPデータ呼出しの際のコールバック関数名を指定します。
    sectionHeaderFlg : int, optional
        CSVデータ呼出しの際のセクションヘッダの出力有無を指定します。1(出力する)、2(出力しない)から選択します。

    Returns
    -------
    data : dict or list
        取得した統計データ。

    Raises
    ------
    ValueError
        dataSetIdとstatsDataIdの両方が指定された場合、または
        どちらも指定されていない場合に発生します。

    """

    params = locals()
    params.pop("kwargs")
    params.update(kwargs)

    endpoint = _build_endpoint(_APIType.getStatsData)

    response = requests.get(endpoint, params=params)
    return response.json()
