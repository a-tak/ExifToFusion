from lib.base import ExifInfo, CameraExifSetterAbs
from pprint import pprint
import xml.etree.ElementTree as ET


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
        #XML内の情報取得
        xmlText = exiftool.get("PanasonicSemi-ProMetadataXml")
        if xmlText:
            xml = ET.fromstring(xmlText)
            #Codec取得 バージョン大きい方を優先
            for item in xml.iter("{urn:schemas-Professional-Plug-in:Semi-Pro:ClipMetadata:v1.0}Codec"):
                e.Codec = item.text.replace("_", " ")
            for item in xml.iter("{urn:schemas-Professional-Plug-in:Semi-Pro:ClipMetadata:v1.1}Codec"):
                e.Codec = item.text.replace("_", " ")
        return e
