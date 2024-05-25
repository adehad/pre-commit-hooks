"""Character Mappings.

In Python so can make comments and still be valid.
"""

from __future__ import annotations

import enum

CHAR_MAP_TYPE = dict[str, dict[str, dict[str, str]]]

# spell-checker: disable
# ruff: noqa: E501, RUF001, RUF003
# fmt: off
CHAR_MAP: CHAR_MAP_TYPE = {
    # Contextual
    "ʾalif": {"rule": {"\u0627": "(\ufe8d|\ufe8e)"}},                       # "ا": "(ﺍ|ﺎ)"
    "bāʾ": {"rule": {"\u0628": "(\ufe8f|\ufe90|\ufe92|\ufe91)"}},           # "ب": "(ﺏ|ﺐ|ﺒ|ﺑ)"
    "tāʾ": {"rule": {"\u062a": "(\ufe95|\ufe96|\ufe98|\ufe97)"}},           # "ت": "(ﺕ|ﺖ|ﺘ|ﺗ)"
    "ṯāʾ": {"rule": {"\u062b": "(\ufe99|\ufe9a|\ufe9c|\ufe9b)"}},           # "ث": "(ﺙ|ﺚ|ﺜ|ﺛ)"
    "ǧīm": {"rule": {"\u062c": "(\ufe9d|\ufe9e|\ufea0|\ufe9f)"}},           # "ج": "(ﺝ|ﺞ|ﺠ|ﺟ)"
    "ḥāʾ": {"rule": {"\u062d": "(\ufea1|\ufea2|\ufea4|\ufea3)"}},           # "ح": "(ﺡ|ﺢ|ﺤ|ﺣ)"
    "ḫāʾ": {"rule": {"\u062e": "(\ufea5|\ufea6|\ufea8|\ufea7)"}},           # "خ": "(ﺥ|ﺦ|ﺨ|ﺧ)"
    "dāl": {"rule": {"\u062f": "(\ufea9|\ufeaa)"}},                         # "د": "(ﺩ|ﺪ)"
    "ḏāl": {"rule": {"\u0630": "(\ufeab|\ufeac)"}},                         # "ذ": "(ﺫ|ﺬ)"
    "rāʾ": {"rule": {"\u0631": "(\ufead|\ufeae)"}},                         # "ر": "(ﺭ|ﺮ)"
    "zayn/zāy": {"rule": {"\u0632": "(\ufeaf|\ufeb0)"}},                    # "ز": "(ﺯ|ﺰ)"
    "sīn": {"rule": {"\u0633": "(\ufeb1|\ufeb2|\ufeb4|\ufeb3)"}},           # "س": "(ﺱ|ﺲ|ﺴ|ﺳ)"
    "šīn": {"rule": {"\u0634": "(\ufeb5|\ufeb6|\ufeb8|\ufeb7)"}},           # "ش": "(ﺵ|ﺶ|ﺸ|ﺷ)"
    "ṣād": {"rule": {"\u0635": "(\ufeb9|\ufeba|\ufebc|\ufebb)"}},           # "ص": "(ﺹ|ﺺ|ﺼ|ﺻ)"
    "ḍād": {"rule": {"\u0636": "(\ufebd|\ufebe|\ufec0|\ufebf)"}},           # "ض": "(ﺽ|ﺾ|ﻀ|ﺿ)"
    "ṭāʾ": {"rule": {"\u0637": "(\ufec1|\ufec2|\ufec4|\ufec3)"}},           # "ط": "(ﻁ|ﻂ|ﻄ|ﻃ)"
    "ẓāʾ": {"rule": {"\u0638": "(\ufec5|\ufec6|\ufec8|\ufec7)"}},           # "ظ": "(ﻅ|ﻆ|ﻈ|ﻇ)"
    "ʿayn": {"rule": {"\u0639": "(\ufec9|\ufeca|\ufecc|\ufecb)"}},          # "ع": "(ﻉ|ﻊ|ﻌ|ﻋ)"
    "ġayn": {"rule": {"\u063a": "(\ufecd|\ufece|\ufed0|\ufecf)"}},          # "غ": "(ﻍ|ﻎ|ﻐ|ﻏ)"
    "fāʾ": {"rule": {"\u0641": "(\ufed1|\ufed2|\ufed4|\ufed3)"}},           # "ف": "(ﻑ|ﻒ|ﻔ|ﻓ)"
    "qāf": {"rule": {"\u0642": "(\ufed5|\ufed6|\ufed8|\ufed7)"}},           # "ق": "(ﻕ|ﻖ|ﻘ|ﻗ)"
    "kāf": {"rule": {"\u0643": "(\ufed9|\ufeda|\ufedc|\ufedb)"}},           # "ك": "(ﻙ|ﻚ|ﻜ|ﻛ)"
    "lām": {"rule": {"\u0644": "(\ufedd|\ufede|\ufee0|\ufedf)"}},           # "ل": "(ﻝ|ﻞ|ﻠ|ﻟ)"
    "mīm": {"rule": {"\u0645": "(\ufee1|\ufee2|\ufee4|\ufee3)"}},           # "م": "(ﻡ|ﻢ|ﻤ|ﻣ)"
    "nūn": {"rule": {"\u0646": "(\ufee5|\ufee6|\ufee8|\ufee7)"}},           # "ن": "(ﻥ|ﻦ|ﻨ|ﻧ)"
    "hāʾ": {"rule": {"\u0647": "(\ufee9|\ufeea|\ufeec|\ufeeb)"}},           # "ه": "(ﻩ|ﻪ|ﻬ|ﻫ)"
    "wāw": {"rule": {"\u0648": "(\ufeed|\ufeee)"}},                         # "و": "(ﻭ|ﻮ)"
    "yāʾ": {"rule": {"\u064a": "(\ufef0|\ufef1|\ufef2|\ufef4|\ufef3)"}},    # "ي": "(ﻱ|ﻲ|ﻴ|ﻳ)"
    # Presentation Form [A or B]
    "ʾalif with hamza [B]": {"rule": {"\u0625": "(\ufe87)"}},               # "إ": "(ﺇ)"
    "hamza [B]": {"rule": {"\u0621": "(\ufe80)"}},                          # "ء": "(ﺀ)"
    "yāʾ [B]": {"rule": {"\u064a": "(\ufef0|\ufeef)"}},                     # "ي": "(ﻯ|ﻰ)"
    "ʾalif lām [B]": {"rule": {"\u0644\u0627": "(\ufefc)"}},                # "لا": "(ﻼ)"
}
""""RuleName": {"rule": {"ReplacementCharacter(s)": "RegexOfApplicableCharacter(s)"}}"""
# fmt: on
# spell-checker: enable


@enum.unique
class ArabicUnicodeGroup(enum.Enum):
    """Unicode Groups for Arabic Characters as of Unicode 15.1."""

    Unknown = enum.auto()
    """Maybe not Arabic."""

    Arabic = enum.auto()
    """256 characters"""
    ArabicSupplement = enum.auto()
    """48 characters"""
    ArabicExtendedB = enum.auto()
    """41 characters"""
    ArabicExtendedA = enum.auto()
    """96 characters"""
    ArabicPresentationFormsA = enum.auto()
    """631 characters"""
    ArabicPresentationFormsB = enum.auto()
    """141 characters"""
    RumiNumeralSymbols = enum.auto()
    """31 characters"""
    ArabicExtendedC = enum.auto()
    """3 characters"""
    IndicSiyaqNumbers = enum.auto()
    """68 characters"""
    OttomanSiyaqNumbers = enum.auto()
    """61 characters"""
    ArabicMathematicalAlphabeticSymbols = enum.auto()
    """143 characters"""

    @classmethod
    def get_type(cls: ArabicUnicodeGroup, input_char: str) -> ArabicUnicodeGroup:
        """Return the Arabic Unicode Group."""
        if "\u0600" <= input_char <= "\u06ff":
            return cls.Arabic
        elif "\u0750" <= input_char <= "\u077f":
            return cls.ArabicSupplement
        elif "\u0870" <= input_char <= "\u089f":
            return cls.ArabicExtendedB
        elif "\u08a0" <= input_char <= "\u08ff":
            return cls.ArabicExtendedA
        elif "\ufb50" <= input_char <= "\ufdff":
            return cls.ArabicPresentationFormsA
        elif "\ufe70" <= input_char <= "\ufeff":
            return cls.ArabicPresentationFormsB
        elif "\u10e60" <= input_char <= "\u10e7F":
            return cls.RumiNumeralSymbols
        elif "\u10ec0" <= input_char <= "\u10efF":
            return cls.ArabicExtendedC
        elif "\u1ec70" <= input_char <= "\u1ecbF":
            return cls.IndicSiyaqNumbers
        elif "\u1ed00" <= input_char <= "\u1ed4F":
            return cls.OttomanSiyaqNumbers
        elif "\u1ee00" <= input_char <= "\u1eefF":
            return cls.ArabicMathematicalAlphabeticSymbols
        else:
            return cls.Unknown


def is_contains_non_general_form(char: str) -> bool:
    """True if the character is not generally supported."""
    return ArabicUnicodeGroup.get_type(max(char)) not in {
        ArabicUnicodeGroup.Unknown,
        ArabicUnicodeGroup.Arabic,
        ArabicUnicodeGroup.ArabicSupplement,
        ArabicUnicodeGroup.ArabicExtendedB,
        ArabicUnicodeGroup.ArabicExtendedC,
        ArabicUnicodeGroup.RumiNumeralSymbols,
        ArabicUnicodeGroup.IndicSiyaqNumbers,
        ArabicUnicodeGroup.OttomanSiyaqNumbers,
        ArabicUnicodeGroup.ArabicMathematicalAlphabeticSymbols,
    }
