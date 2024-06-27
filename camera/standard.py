from lib.base import ExifInfo, CameraExifSetterAbs
from pprint import pprint

class Standard(CameraExifSetterAbs):
    def GetName(self) -> str:
        return "standard"
    
    def GenerateExifText(self, exiftool: dict, mediaPoolItem) -> ExifInfo:
        e = ExifInfo()
        e.Camera = exiftool.get("Model")
        e.Lens = exiftool.get("LensModel")
        e.Aperture= exiftool.get("Aperture")
        e.ISO = exiftool.get("ISO")
        e.SS = exiftool.get("ShutterSpeedValue")
        e.FocalPoint = exiftool.get("FocalLength")
        e.FPS = mediaPoolItem.GetClipProperty("FPS")
        e.WB = exiftool.get("WhiteBalance")

        return e