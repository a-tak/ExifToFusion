from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class ExifInfo:
    Camera: str = None
    Lens: str = None
    Aperture: str = None
    ISO: str = None
    SS: str = None
    WB: str = None
    Tint: str = None
    FPS: str  = None
    FocalPoint: str = None
    Distance: str = None
    LUT: str = None
    Format: str = None #JPEG / RAW
    Size: str = None #3000x2500

class TitleSetterAbs(ABC):
    @abstractmethod
    def GetName(self) -> str:
        """メディアプールのタイトルのクリップ名
        """
        pass
    
    @abstractmethod
    def GetFirstToolName(self) -> str:
        """Fusionページ開いたときの一番最初のツールの名前
        """
        pass

    @abstractmethod
    def GenerateFusionParameter(self, exifinfo: ExifInfo) -> dict:
        """Fusionに渡すパラメーター用の辞書を作る
        """
        pass

    def Concat(self, baseStr: str, addStr: str, noneCheckVar: str):
        """noneCheckVarがNone以外のときだけ文字列を結合する
        """
        if noneCheckVar is None:
            return baseStr
        return baseStr + addStr

class CameraExifSetterAbs(ABC):
    @abstractmethod
    def GetName(self) -> str:
        pass

    @abstractmethod
    def GenerateExifText(self, exiftool: dict, mediaPoolItem) -> ExifInfo:
        pass
    