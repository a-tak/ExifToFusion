from lib.base import ExifInfo, TitleSetterAbs
import textwrap

class G_ApertureText_06_ex(TitleSetterAbs):
    def GetName(self) -> str:
        return "G_ApertureText-06-ex"
    
    def GenerateFusionParameter(self, exifinfo: ExifInfo) -> dict:
        return {
            "Input1": exifinfo.Aperture,
            "Input13": f"SS:{exifinfo.SS} ISO:{exifinfo.ISO}"
        }

class G_ApertureText_06(TitleSetterAbs):
    def GetName(self) -> str:
        return "G_ApertureText-06"
    
    def GenerateFusionParameter(self, exifinfo: ExifInfo) -> dict:
        return {
            "Input1": exifinfo.Aperture,
        }
class G_CameraExif_Text(TitleSetterAbs):
    def __init__(self):
        self.lines = []

    def GetName(self) -> str:
        return "G_CameraExif-Text"
    
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
