#!/usr/bin/env python
import DaVinciResolveScript as dvr_script
from pyexifinfo import information
from pprint import pprint
import pathlib

class ExifToFusion():
    def __init__(self):
        self.resolve = dvr_script.scriptapp("Resolve")
        self.projectManager = self.resolve.GetProjectManager()
        self.project = self.projectManager.GetCurrentProject()
        self.mediaPool = self.project.GetMediaPool()
        self.timeline = self.project.GetCurrentTimeline()
        
    def main(self):
        # メディアプールのFusionコンポジット取得
        fusionClipName = "G_ApertureText-12-ex"
        srcFusionComp = self.GetFusionComposite(fusionClipName)

        # 対象のクリップを取得
        trackType = "video"
        trackIndex = 2  # 取得するトラックのインデックス
        addTrackIndex = 3
        # Fusionタイトル削除
        self.DeleteFusionTitle(addTrackIndex, fusionClipName)

        clips = self.timeline.GetItemListInTrack(trackType, trackIndex)
        for clip in clips:
            mediaPoolItem = clip.GetMediaPoolItem()
            # Exif取得
            exif = self.GetExif(mediaPoolItem)
            pprint(exif)
                        
            # Fusionタイトル タイムライン追加
            fusionComp = self.AddToTimeline(clip, srcFusionComp, addTrackIndex)
            
            # Fusionタイトルパラメーター設定
            values = {
                "Input1": exif.get("Aperture", "Unknown"),
                "Input13": f"SS:{exif.get("Shutter Speed", "Unknown")} ISO:{exif.get("ISO", "Unknown")}"
            }
            self.SetFusionParameter(fusionComp, values)
    
    def DeleteFusionTitle(self, trackIndex, targetClipName):
        """指定したトラックのFusionタイトルをすべて削除する
        対象外のクリップがある場合は削除しない
        """
        clips = self.timeline.GetItemListInTrack("video", trackIndex)
        for clip in clips:
            # 本当ならメディアプールのClip Nameと比較したがったがFusionタイトルとメディアプールが紐付いてないので出来なかった
            if clip.GetName() != targetClipName:
                raise Exception("Processing was interrupted due to the presence of another clip on the track")
        self.timeline.DeleteClips(clips)

    def SetFusionParameter(self, fusionComp, parameters):
        comp = fusionComp.GetFusionCompByIndex(1)
        # Fusionコンポジションの最初のツールを取得してくる
        toolList = comp.GetToolList()
        tool = list(toolList.values())[0]
        
        if tool is not None:
            print("find!")
            for key, value in parameters.items():
                tool[key] = value

    def AddToTimeline(self, baseClip, fusionComp, trackIndex):
        clipInfo = {
            "mediaPoolItem": fusionComp,
            "startFrame": 0,
            "endFrame": baseClip.GetDuration(), # 後をどこまで伸ばすか
            "trackIndex": trackIndex,
            "recordFrame": baseClip.GetStart() # タイムラインに配置する場所
        }
        results = self.mediaPool.AppendToTimeline([clipInfo])
        if results is None or len(results) != 1:
            raise Exception("Failed Add TimelineItem")
        if results[0].GetFusionCompByIndex(1) is None:
            raise Exception("Failed Add Fusion Comp")
        return results[0]


    def GetFusionComposite(self, clipName):
        """指定されたクリップ名のFusionコンポジットをメディアプールから取得する
        """
        folder = self.mediaPool.GetCurrentFolder()
        for clip in folder.GetClipList():
            if clip.GetClipProperty("Clip Name") == clipName:
                return clip
        raise Exception(f"Not Found Fusion Clip: {clipName}")
        
    def GetExif(self, mediaPoolItem):
        """指定されたメディアプールアイテムのExifを取得
        """
        meta = {}
        filePath = mediaPoolItem.GetClipProperty("File Path")
        if pathlib.Path(filePath).suffix.lower() == ".braw" :
            meta = self.GetBrawMeta(mediaPoolItem)
        else:
            data = information(filePath)
            meta = self.GetMovMeta(data, mediaPoolItem)
        return meta
    
    def GetMovMeta(self, exifObj, mediaPoolItem):
        """BRAW以外のメタデータ取得
        """
        meta = {
            "Camera": exifObj.get("EXIF:Model"),
            "Lens": exifObj.get("Composite:LensID"),
            "Aperture": exifObj.get("Composite:Aperture"),
            "ISO": exifObj.get("EXIF:ISO"),
            "Shutter Speed": exifObj.get("Composite:ShutterSpeed"),
            "Focal Point": exifObj.get("Composite:FocalLength35efl"),
            "Distance": exifObj.get("Composite:HyperfocalDistance"),
            "FPS": mediaPoolItem.GetClipProperty("FPS")
        }
        return meta
        
    def GetBrawMeta(self, mediaPoolItem):
        """BRAWのメタデータを取得する
        """
        print(mediaPoolItem.GetMetadata())
        angle = mediaPoolItem.GetMetadata("Shutter Angle")[:-1] #末尾の「°」を消す
        print(angle)
        fps =  mediaPoolItem.GetClipProperty("FPS")
        ss = f"1/{int(int(fps) * 360 / int(angle))}"
        meta = {
            "Camera": mediaPoolItem.GetMetadata("Camera Type"),
            "Lens": mediaPoolItem.GetMetadata("Lens Type"),
            "Aperture": mediaPoolItem.GetMetadata("Camera Aperture"),
            "ISO": mediaPoolItem.GetMetadata("ISO"),
            "Shutter Speed": ss,
            "Focal Point": mediaPoolItem.GetMetadata("Focal Point (mm)"),
            "Distance": mediaPoolItem.GetMetadata("Distance"),
            "FPS": mediaPoolItem.GetClipProperty("FPS"),
            "WB": mediaPoolItem.GetMetadata("White Point (Kelvin)"),
            "Tint": mediaPoolItem.GetMetadata("White Balance Tint")
        }
        return meta

if __name__ == "__main__":
    obj = ExifToFusion().main()