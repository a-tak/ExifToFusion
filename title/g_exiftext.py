from lib.base import ExifInfo, TitleSetterAbs

class G_ApertureText_06(TitleSetterAbs):
    def GetName(self) -> str:
        return "G-ApertureText-06"

    def GetFirstToolName(self) -> str:
        return "GApertureText06_new11"

    def GenerateFusionParameter(self, exifinfo: ExifInfo) -> dict:
        return {
            "Input1": super().Concat("", super().GetFNumber(exifinfo), exifinfo.Aperture),
        }
class G_ApertureText_06_ex(TitleSetterAbs):
    def GetName(self) -> str:
        return "G-ApertureText-06-ex"

    def GetFirstToolName(self) -> str:
        return "GApertureText06ex_new"


    def GenerateFusionParameter(self, exifinfo: ExifInfo) -> dict:
        aperture = super().Concat("", super().GetFNumber(exifinfo), exifinfo.Aperture)
        txt = super().Concat("", f"SS:{exifinfo.SS}", exifinfo.SS)
        txt = super().Concat(txt, f"ISO:{exifinfo.ISO}", exifinfo.ISO)
        return {
            "Input1": aperture,
            "Input13": txt,
        }

class G_ApertureText_08(TitleSetterAbs):
    def GetName(self) -> str:
        return "G-ApertureText-08"

    def GetFirstToolName(self) -> str:
        return "GApertureText08_new"

    def GenerateFusionParameter(self, exifinfo: ExifInfo) -> dict:
        return {
            "Input1": super().Concat("", super().GetFNumber(exifinfo), exifinfo.Aperture),
        }
class G_ApertureText_08_ex(TitleSetterAbs):
    def GetName(self) -> str:
        return "G-ApertureText-08-ex"

    def GetFirstToolName(self) -> str:
        return "GApertureText08ex_new"


    def GenerateFusionParameter(self, exifinfo: ExifInfo) -> dict:
        aperture = super().Concat("", f"{super().GetFNumber(exifinfo)}", exifinfo.Aperture)
        txt = super().Concat("", f"SS:{exifinfo.SS}", exifinfo.SS)
        txt = super().Concat(txt, f"ISO:{exifinfo.ISO}", exifinfo.ISO)
        return {
            "Input1": aperture,
            "Input13": txt,
        }

class G_ApertureText_12(TitleSetterAbs):
    def GetName(self) -> str:
        return "G-ApertureText-12"

    def GetFirstToolName(self) -> str:
        return "GApertureText12_new"

    def GenerateFusionParameter(self, exifinfo: ExifInfo) -> dict:
        return {
            "Input1": super().Concat("", f"{super().GetFNumber(exifinfo)}", exifinfo.Aperture),
        }
class G_ApertureText_12_ex(TitleSetterAbs):
    def GetName(self) -> str:
        return "G-ApertureText-12-ex"

    def GetFirstToolName(self) -> str:
        return "GApertureText12ex_new1"


    def GenerateFusionParameter(self, exifinfo: ExifInfo) -> dict:
        aperture = super().Concat("", super().GetFNumber(exifinfo), exifinfo.Aperture)
        txt = super().Concat("", f"SS:{exifinfo.SS}", exifinfo.SS)
        txt = super().Concat(txt, f"ISO:{exifinfo.ISO}", exifinfo.ISO)
        return {
            "Input1": aperture,
            "Input13": txt,
        }


class G_CameraExif_Text(TitleSetterAbs):

    def __init__(self):
        self.lines = []

    def GetName(self) -> str:
        return "G-CameraExif-Text"

    def GetFirstToolName(self) -> str:
        return "GCameraExifText_new1"

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
        
        result = "\n".join(self.lines)
        return {
            "Input1": result,
        }

    def SetValue(self, name: str, value: str):
        if value is None or value == "":
            return
        self.lines.append(f"{name} : {value}")
