from lib.base import ExifInfo, CameraExifSetterAbs
from pprint import pprint

class Standard(CameraExifSetterAbs):
    def GetName(self) -> str:
        return "standard"
    
    def GenerateExifText(self, exiftool: dict, mediaPoolItem) -> ExifInfo:
        pprint(exiftool)
        e = ExifInfo()
        e.Camera = exiftool.get("")
        e.Lens = mediaPoolItem.GetMetadata("Lens Type")
        e.Aperture =mediaPoolItem.GetMetadata("Camera Aperture")
        e.ISO = mediaPoolItem.GetMetadata("ISO")
        e.SS = ss
        e.FocalPoint = mediaPoolItem.GetMetadata("Focal Point (mm)")
        e.Distance = mediaPoolItem.GetMetadata("Distance")
        e.FPS = mediaPoolItem.GetClipProperty("FPS")
        e.WB = mediaPoolItem.GetMetadata("White Point (Kelvin)")
        e.Tint =  mediaPoolItem.GetMetadata("White Balance Tint")

        return e