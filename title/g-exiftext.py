from lib.base import ExifInfo, TitleSetterAbs

class ApertureText_06_ex(TitleSetterAbs):
    def GetName(self) -> str:
        return "G_ApertureText-06-ex"
    
    def GenerateFusionParameter(self, exifinfo: ExifInfo) -> dict:
        return {
            "Input1": exifinfo.Aperture,
            "Input13": f"SS:{exifinfo.SS} ISO:{exifinfo.ISO}"
        }

