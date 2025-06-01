from lib.base import ExifInfo, TitleSetterAbs

class Text_Plus(TitleSetterAbs):
    def __init__(self):
        self.lines = []

    def GetNames(self) -> list[str]:
        return ["Text+"]
    
    def GetFirstToolNames(self) -> list[str]:
        return ["Template"]
    
    def GenerateFusionParameter(self, exifinfo: ExifInfo) -> dict:
        self.SetValue("Camera", exifinfo.Camera)
        self.SetValue("Lens", exifinfo.Lens)
        self.SetValue("Focal Length", exifinfo.FocalPoint)
        self.SetValue("F.Number", super().GetFNumber(exifinfo))
        self.SetValue("SS", exifinfo.SS)
        self.SetValue("ISO", exifinfo.ISO)
        self.SetValue("WB", exifinfo.WB)
        self.SetValue("Format", exifinfo.Format)
        self.SetValue("Compression Ratio", exifinfo.CompressionRatio)
        self.SetValue("Codec", exifinfo.Codec)
        if exifinfo.Format != "JPEG":
            self.SetValue("FPS",exifinfo.FPS)
        self.SetValue("Size", exifinfo.Size)
        self.SetValue("Photo Style", exifinfo.PhotoStyle)
        self.SetValue("Picture Mode", exifinfo.PictureMode)
        self.SetValue("Picture Mode Strength", exifinfo.PictureModeStrength)
        self.SetValue("Shadow", exifinfo.Shadow)
        self.SetValue("Highlight", exifinfo.Highlight)
        self.SetValue("Fade", exifinfo.Fade)
        self.SetValue("Vignette", exifinfo.Vignette)
        
        result = "\n".join(self.lines)
        return {
            "StyledText": result,
        }
    
    def SetValue(self, name: str, value: str):
        if value is None or value == "":
            return
        self.lines.append(f"{name} : {value}")
