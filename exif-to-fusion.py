#!/usr/bin/env python
import DaVinciResolveScript as dvr_script
from pyexifinfo import information
from pprint import pprint

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
        clips = self.timeline.GetItemListInTrack(trackType, trackIndex)
        for clip in clips:
            mediaPoolItem = clip.GetMediaPoolItem()
            # Exif取得
            exif = self.GetExif(mediaPoolItem)
#            print(exif)
                        
            # Fusionタイトル タイムライン追加
            addTrackIndex = 3
            fusionComp = self.AddToTimeline(clip, srcFusionComp, addTrackIndex)
            
            # Fusionタイトルパラメーター設定
            values = {
                "Input1": "F99"
            }
            self.SetFusionParameter(fusionComp, values)
            
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
        filePath = mediaPoolItem.GetClipProperty("File Path")

        meta = []
        data = information(filePath)
#        print(f"{data}\n-----------------------------------")
        meta.append(["Camera", data.get("EXIF:Model")])
        meta.append(["Lens", data.get("Composite:LensID")])
        meta.append(["Aperture", data.get("Composite:Aperture")])
        meta.append(["ISO", data.get("EXIF:ISO")])
        meta.append(["Shutter Speed", data.get("Composite:ShutterSpeed")])
        meta.append(["Focal Point", data.get("Composite:FocalLength35efl")])
        meta.append(["Distance", data.get("Composite:HyperfocalDistance")])
        meta.append(["FPS", mediaPoolItem.GetClipProperty("FPS")])

        return meta

if __name__ == "__main__":
    obj = ExifToFusion().main()