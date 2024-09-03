from lib.base import ExifInfo, CameraExifSetterAbs

class Bmpcc(CameraExifSetterAbs):
    def GetName(self) -> str:
        return "BMPCC"
    
    def GenerateExifText(self, exiftool: dict, mediaPoolItem) -> ExifInfo:
        print(f"BRAW Metadata: {mediaPoolItem.GetMetadata()}")
        
        angle = mediaPoolItem.GetMetadata("Shutter Angle")[:-1] #末尾の「°」を消す
        fps = mediaPoolItem.GetClipProperty("FPS")
        ss = f"1/{int(int(fps) * 360 / int(angle))}"

        e = ExifInfo()
        e.Camera = mediaPoolItem.GetMetadata("Camera Type")
        e.Lens = mediaPoolItem.GetMetadata("Lens Type")
        e.Aperture =mediaPoolItem.GetMetadata("Camera Aperture")
        e.ISO = mediaPoolItem.GetMetadata("ISO")
        e.SS = ss
        e.FocalPoint = mediaPoolItem.GetMetadata("Focal Point (mm)")
        e.Distance = mediaPoolItem.GetMetadata("Distance")
        e.FPS = mediaPoolItem.GetClipProperty("FPS")
        e.WB = mediaPoolItem.GetMetadata("White Point (Kelvin)")
        e.Tint =  mediaPoolItem.GetMetadata("White Balance Tint")
        e.CompressionRatio = mediaPoolItem.GetMetadata("Compression Ratio")

        return e