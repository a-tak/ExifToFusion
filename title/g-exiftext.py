from lib.base import ExifInfo, TitleSetterAbs

class G_ApertureText_06_ex(TitleSetterAbs):
    def GetName(self) -> str:
        return "G_ApertureText-06-ex"
    
    def GetFirstToolName(self) -> str:
        return "GApertureText06ex"
    

    def GenerateFusionParameter(self, exifinfo: ExifInfo) -> dict:
        aperture = super().Concat("", f"{exifinfo.Aperture}", exifinfo.Aperture)
        txt = super().Concat("", f"SS:{exifinfo.SS}", exifinfo.SS)
        txt = super().Concat(txt, f"ISO:{exifinfo.ISO}", exifinfo.ISO)
        return {
            "Input1": aperture,
            "Input13": txt,
        }

class G_ApertureText_06(TitleSetterAbs):
    def GetName(self) -> str:
        return "G_ApertureText-06"
    
    def GetFirstToolName(self) -> str:
        return "GApertureText6"
    
    def GenerateFusionParameter(self, exifinfo: ExifInfo) -> dict:
        return {
            "Input1": super().Concat("", f"{exifinfo.Aperture}", exifinfo.Aperture),
        }
class G_CameraExif_Text(TitleSetterAbs):
    def __init__(self):
        self.lines = []

    def GetName(self) -> str:
        return "G_CameraExif-Text"

    def GetFirstToolName(self) -> str:
        return "G_CameraExifText"
    
    def GenerateFusionParameter(self, exifinfo: ExifInfo) -> dict:
        self.SetValue("Camera", exifinfo.Camera)
        self.SetValue("Lens", exifinfo.Lens)
        self.SetValue("F.Number", exifinfo.Aperture)
        self.SetValue("SS", exifinfo.SS)
        self.SetValue("ISO", exifinfo.ISO)
        self.SetValue("WB", exifinfo.WB)
        self.SetValue("Format", exifinfo.Format)
        self.SetValue("Size", exifinfo.Size)
        self.SetValue("LUT", exifinfo.LUT)
        
        result = "\n".join(self.lines)
        return {
            "Input1": result,
        }
    
    def SetValue(self, name: str, value: str):
        if value is None:
            return
        self.lines.append(f"{name} : {value}")
