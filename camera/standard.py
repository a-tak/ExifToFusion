from lib.base import ExifInfo, CameraExifSetterAbs
from pprint import pprint


class Standard(CameraExifSetterAbs):

    def GetName(self) -> str:
        return "standard"

    def GenerateExifText(self, exiftool: dict, mediaPoolItem) -> ExifInfo:
        pprint(exiftool)
        e = ExifInfo()
        e.Camera = exiftool.get("Model")
        e.Lens = exiftool.get("LensID")
        e.Aperture = exiftool.get("Aperture")
        e.ISO = exiftool.get("ISO")
        e.SS = exiftool.get("ShutterSpeed")
        e.FocalPoint = exiftool.get("FocalLength")
        e.WB = exiftool.get("WhiteBalance")
        e.PhotoStyle = exiftool.get("PhotoStyle")
        e.Size = exiftool.get("ImageSize")
        e.Format = exiftool.get("FileType")
        if e.Format != "JPEG" and e.Format != "DNG":
            e.FPS = mediaPoolItem.GetClipProperty("FPS")
        return e
