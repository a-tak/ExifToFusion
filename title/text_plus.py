from lib.base import ExifInfo, TitleSetterAbs

class Text_Plus(TitleSetterAbs):
    def __init__(self):
        self.lines = []

    def GetName(self) -> str:
        return "Text+"
    
    def GetFirstToolName(self) -> str:
        return "Template"
    
    def GenerateFusionParameter(self, exifinfo: ExifInfo) -> dict:
        self.SetValue("Camera", exifinfo.Camera)
        self.SetValue("Lens", exifinfo.Lens)
        self.SetValue("F.Number", super().GetFNumber(exifinfo))
        self.SetValue("SS", exifinfo.SS)
        self.SetValue("ISO", exifinfo.ISO)
        self.SetValue("WB", exifinfo.WB)
        self.SetValue("Format", exifinfo.Format)
        self.SetValue("Size", exifinfo.Size)
        self.SetValue("LUT", exifinfo.LUT)
        
        result = "\n".join(self.lines)
        return {
            "StyledText": result,
        }
    
    def SetValue(self, name: str, value: str):
        if value is None or value == "":
            return
        self.lines.append(f"{name} : {value}")
