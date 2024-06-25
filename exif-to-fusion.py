#!/usr/bin/env python
import DaVinciResolveScript as dvr_script
from pyexifinfo import information
from pprint import pprint
import pathlib
import sys
import json
import os

class ExifToFusion():
    def __init__(self):
        self.resolve = dvr_script.scriptapp("Resolve")
        self.projectManager = self.resolve.GetProjectManager()
        self.project = self.projectManager.GetCurrentProject()
        self.mediaPool = self.project.GetMediaPool()
        self.timeline = self.project.GetCurrentTimeline()
        self.fusion = self.resolve.Fusion()
        scriptPath = os.path.abspath(sys.argv[0])
        scriptDir = os.path.dirname(scriptPath)
        self.settingsFile = os.path.join(scriptDir, "settings.json")
                
    def main(self):
        ret: dict = self.ShowMainDialog()
        if ret is None:
            sys.exit()
            
        fusionClipName: str = ret.get("FusionTitle", None)
        if fusionClipName is None or fusionClipName == "":
            raise Exception("Fusion clip Name blank error.")
        
        trackIndex = ret.get("SrcTrack", None)
        if trackIndex is None or self.IsInt(trackIndex) == False:
            raise Exception(f"SrcTrack invalid.")
        trackIndex = int(trackIndex)
        
        if trackIndex <= 0 or self.timeline.GetTrackCount("video") < trackIndex:
            # raise Exception(f"SrcTrack Invalid. value={trackIndex}")
            self.ShowMessage(f"指定されたトラック`{trackIndex}`はありません\nExifの取得対象となるクリップが配置されているトラック番号を入れてください")
            sys.exit()

        addTrackIndex = ret.get("DstTrack", None)
        if addTrackIndex is None or self.IsInt(addTrackIndex) == False:
            raise Exception(f"DstTrack invalid.")
        addTrackIndex = int(addTrackIndex)
        
        # メディアプールのFusionコンポジット取得
        srcFusionComp = self.GetFusionComposite(fusionClipName)
        # Fusionタイトル削除
        self.DeleteFusionTitle(addTrackIndex, fusionClipName)

        # 対象のクリップを取得
        trackType = "video"
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
                "Input13": f"SS:{exif.get('Shutter Speed', 'Unknown')} ISO:{exif.get('ISO', 'Unknown')}"
            }
            self.SetFusionParameter(fusionComp, values)
    
    def SaveSettings(self, settings) -> None: 
        with open(self.settingsFile, 'w') as f:
            json.dump(settings, f)
    
    def LoadSettings(self) -> None:
        if os.path.exists(self.settingsFile):
            with open(self.settingsFile, 'r') as f:
                return json.load(f)
        return {}

    def GetFusionTitleNames(self) -> list[str]:
        """メディアプールのFusionタイトルのリストを取得する
        """
        folder = self.mediaPool.GetCurrentFolder()
        titles: list[str] = []
        for clip in folder.GetClipList():
            if clip.GetClipProperty("Type") == "Fusionタイトル":
                titles.append(clip.GetClipProperty("Clip Name"))
        return titles
            
    def IsInt(self, value) -> bool:
        try:
            int(value)
            return True
        except ValueError:
            return False
        
    def ShowMessage(self, message) -> None:
        """無理やり標準UIでメッセージ画面を出す
        """
        comp = self.fusion.GetCurrentComp()
        dialog = {
            1: {1: "text", "Name": "メッセージ", 2: "Text", "ReadOnly": True , "Wrap": True, "Default": message, "Lines": 7}
        }
        comp.AskUser("メッセージ", dialog)
        
    def ShowMainDialog(self) -> dict:
        """ダイアログを表示して対象のトラックをユーザーに選択させる
        """
        titles = self.GetFusionTitleNames()
        comp = self.fusion.GetCurrentComp()
        if len(titles) == 0:
            self.ShowMessage("メディアプールにFusionタイトルが一つもありません")
            return None
        titleOptions = {}
        for index, title in enumerate(titles):
            titleOptions[index] = title

        settings = self.LoadSettings()
        dialog = {
            1: {1: "fusionTitle", "Name": "追加するFusionタイトル", 2: "Dropdown", "Options": titleOptions, "Default": settings.get("FusionTitleIndex", 0)},
            2: {1: "srcTrack", "Name": "Exif取得するトラック番号", 2: "Text", "Lines": 1, "Default": settings.get("SrcTrack", "2")},
            3: {1: "dstTrack", "Name": "タイトル追加先トラック番号", 2: "Text", "Lines": 1, "Default": settings.get("DstTrack", "3")},
        }
        result = comp.AskUser("ExifToFusion", dialog)

        if result:
            settings_to_save = {
                "FusionTitle": titleOptions[result["fusionTitle"]],
                "FusionTitleIndex": result["fusionTitle"],
                "SrcTrack": result["srcTrack"],
                "DstTrack": result["dstTrack"]
            }
            self.SaveSettings(settings_to_save)
            return settings_to_save
        else:
            return None
    
    def DeleteFusionTitle(self, trackIndex, targetClipName) -> None:
        """指定したトラックのFusionタイトルをすべて削除する
        対象外のクリップがある場合は削除しない
        """
        clips = self.timeline.GetItemListInTrack("video", trackIndex)
        if clips is None:
            return
        for clip in clips:
            # 本当ならメディアプールのClip Nameと比較したがったがFusionタイトルとメディアプールが紐付いてないので出来なかった
            if clip.GetName() != targetClipName:
                raise Exception("Processing was interrupted due to the presence of another clip on the track")
        self.timeline.DeleteClips(clips)

    def SetFusionParameter(self, fusionComp, parameters) -> None:
        comp = fusionComp.GetFusionCompByIndex(1)
        # Fusionコンポジションの最初のツールを取得してくる
        toolList = comp.GetToolList()
        tool = list(toolList.values())[0]
        
        if tool is not None:
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
        
    def GetExif(self, mediaPoolItem) -> dict:
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
    
    def GetMovMeta(self, exifObj, mediaPoolItem) -> dict:
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
        
    def GetBrawMeta(self, mediaPoolItem) -> dict:
        """BRAWのメタデータを取得する
        """
        print(mediaPoolItem.GetMetadata())
        angle = mediaPoolItem.GetMetadata("Shutter Angle")[:-1] #末尾の「°」を消す
        fps = mediaPoolItem.GetClipProperty("FPS")
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
