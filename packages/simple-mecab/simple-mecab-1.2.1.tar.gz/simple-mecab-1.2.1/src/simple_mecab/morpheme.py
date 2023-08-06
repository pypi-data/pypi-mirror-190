# nopep8
from typing import NamedTuple, Optional, Tuple


class Morpheme(NamedTuple):
    """MeCabの解析結果を要素別に格納するためのNamedTupleです。

    Variables
    ---------
    token : str
        形態素 （例：'東京', '行っ'）

    pos0 : str | None
        品詞大分類 (part of speech)
        （例：'名詞', '動詞'）

    pos1 : str | None
        品詞細分類1
        （例：'固有名詞', '自立'）

    pos2 : str | None
        品詞細分類2
        （例：'地域'）

    pos3 : str | None
        品詞細分類3
        （例：'一般'）

    conjugation_type : str | None
        活用型
        （例：'五段・カ行促音便'）

    conjugation : str | None
        活用形
        （例：'連用タ接続'）

    stem_form : str | None
        原形
        （例：'東京', '行く'）

    pronunciation : tuple[str] | None
        発音
        （例：('トウキョウ', 'トーキョー'), ('イッ')）

    unknown : str | None
        正常に抽出できなかった場合はここに入ります。

    **それぞれの要素に入る値は使用する辞書によって異なります。**
    """

    token: str
    """形態素の文字列

    Example
    -------
    '東京', '行っ'
    """

    pos0: Optional[str] = None
    """品詞大分類

    存在しない場合は`None`

    Example
    -------
    '名詞', '動詞', None

    格納される値は使用する辞書によって異なります。
    """

    pos1: Optional[str] = None
    """品詞細分類1

    存在しない場合は`None`

    Example
    -------
    '固有名詞', '自立', None

    格納される値は使用する辞書によって異なります。
    """

    pos2: Optional[str] = None
    """品詞細分類2

    存在しない場合は`None`

    Example
    -------
    '地域', None

    格納される値は使用する辞書によって異なります。
    """

    pos3: Optional[str] = None
    """品詞細分類3

    存在しない場合は`None`

    Example
    -------
    '一般', None

    格納される値は使用する辞書によって異なります。
    """

    conjugation_type: Optional[str] = None
    """活用型

    存在しない場合は`None`を返します。

    Example
    -------
    '五段・カ行促音便', None

    格納される値は使用する辞書によって異なります。
    """

    conjugation: Optional[str] = None
    """活用形

    存在しない場合は`None`を返します。

    Example
    -------
    '連用タ接続', None

    格納される値は使用する辞書によって異なります。
    """

    stem_form: Optional[str] = None
    """原型（レンマ）

    存在しない場合は`None`を返します。

    Example
    -------
    '東京', '行く', None

    格納される値は使用する辞書によって異なります。
    """

    pronunciation: Optional[Tuple[str]] = None
    """発音

    形態素の発音（カタカナ表記）
    存在しない場合は`None`

    Example
    -------
    ('トウキョウ', 'トーキョー'), ('イッ'), None

    格納される値は使用する辞書によって異なります。
    """

    unknown: Optional[str] = None
    """不明な値

    MeCabの解析結果を要素毎にを分類できなかった場合に、
    MeCabの出力のfeature部分の文字列が格納されます。

    通常は`None`

    Example
    -------
    "名詞,固有名詞,地域,一般,*,*,渋谷,シブヤ,シブヤ", None

    格納される値は使用する辞書によって異なります。
    """

    def __str__(self) -> str:
        return (f"Morpheme(token={self.token.__repr__()}, "
                f"pos0={self.pos0.__repr__()}, "  # type: ignore
                f"pos1={self.pos1.__repr__()}, "  # type: ignore
                f"pos2={self.pos2.__repr__()}, "  # type: ignore
                f"pos3={self.pos3.__repr__()}, "  # type: ignore
                f"conjugation_type={self.conjugation_type.__repr__()}, "  # type: ignore
                f"conjugation={self.conjugation.__repr__()}, "  # type: ignore
                f"stem_form={self.stem_form.__repr__()}, "  # type: ignore
                f"pronunciation={self.pronunciation.__repr__().replace(',)', ')')}, "    # type: ignore
                f"unknown={self.unknown.__repr__()})")  # type: ignore

    def __repr__(self) -> str:
        return (f"Morpheme({self.token.__repr__()}, "
                f"{self.pos0.__repr__()}, "  # type: ignore
                f"{self.pos1.__repr__()}, "  # type: ignore
                f"{self.pos2.__repr__()}, "  # type: ignore
                f"{self.pos3.__repr__()}, "  # type: ignore
                f"{self.conjugation_type.__repr__()}, "  # type: ignore
                f"{self.conjugation.__repr__()}, "  # type: ignore
                f"{self.stem_form.__repr__()}, "  # type: ignore
                f"{self.pronunciation.__repr__().replace(',)', ')')}, "  # type: ignore
                f"{self.unknown.__repr__()})")  # type: ignore
