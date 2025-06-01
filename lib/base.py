from dataclasses import dataclass
from abc import ABC, abstractmethod
import re
from pprint import pprint

@dataclass
class ExifInfo:
    Camera: str = None
    Lens: str = None
    Aperture: str = None
    ISO: str = None
    SS: str = None
    WB: str = None
    Tint: str = None
    FPS: str = None
    FocalPoint: str = None
    Distance: str = None
    LUT: str = None
    Format: str = None  #JPEG / RAW
    Size: str = None  #3000x2500
    PhotoStyle: str = None
    PictureMode: str = None
    PictureModeStrength: str = None
    Fade: str = None
    Vignette: str = None
    Shadow: str = None
    Highlight: str = None
    Codec: str = None
    CompressionRatio: str = None #圧縮率。BRAW。

class TitleSetterAbs(ABC):
    @abstractmethod
    def GetNames(self) -> list[str]:
        """メディアプールのタイトルのクリップ名
        """
        pass

    @abstractmethod
    def GetFirstToolNames(self) -> list[str]:
        """Fusionページ開いたときの一番最初のツールの名前
        """
        pass

    @abstractmethod
    def GenerateFusionParameter(self, exifinfo: ExifInfo) -> dict:
        """Fusionに渡すパラメーター用の辞書を作る
        """
        pass

    def Concat(self, baseStr: str, addStr: str, noneCheckVar: str) -> str:
        """noneCheckVarがNone以外のときだけ文字列を結合する
        """
        if noneCheckVar is None:
            return baseStr
        return baseStr + addStr

    def GetFNumber(self, exifinfo: ExifInfo) -> str:
        """F値をフォーマットして表記を統一する
        """
        value = exifinfo.Aperture

        if value is None:
            return ""
        value = str(value)
        headChar = "F"

        # 数値部分のみ取り出し
        numbers = re.findall(r'\d+\.\d+|\d+', value)
        if len(numbers) == 0:
            return ""
        # 最初に見つかった数字にFつけて返す
        return headChar + numbers[0]

class CameraExifSetterAbs(ABC):
    @abstractmethod
    def GetNames(self) -> list[str]:
        pass

    @abstractmethod
    def GenerateExifText(self, exiftool: dict, mediaPoolItem) -> ExifInfo:
        pass
