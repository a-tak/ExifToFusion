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

class TitleSetterAbs(ABC):
    @abstractmethod
    def GetName(self) -> str:
        pass

    @abstractmethod
    def GenerateFusionParameter(self, exifinfo: ExifInfo) -> dict:
        pass
