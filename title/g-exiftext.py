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
    def GetName(self) -> str:
        return "G_CameraExif-Text"
    
    def GenerateFusionParameter(self, exifinfo: ExifInfo) -> dict:
        txt = textwrap.dedent(f"""Camera : {exifinfo.Camera}
Lens : {exifinfo.Lens}
F.Number : {exifinfo.Aperture}
SS : {exifinfo.SS}
ISO : {exifinfo.ISO}
WB : {exifinfo.WB}
Format : {exifinfo.Format}
Size : {exifinfo.Size}
LUT : {exifinfo.LUT}
        """)
        return {
            "Input1": txt,
        }
