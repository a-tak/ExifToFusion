#!/usr/bin/env python
import DaVinciResolveScript as dvr_script
from pyexifinfo import information
from pprint import pprint
import pathlib
import sys
import json
import os
from lib.base import ExifInfo
from lib.base import TitleSetterAbs
from lib.base import CameraExifSetterAbs
import importlib
import pkgutil

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
        self.titlePkg = "title"
        self.titleDir = os.path.join(scriptDir, self.titlePkg)
        
        # カメラモジュールの取得
        self.cameraPkg = "camera"
        self.cameraDir = os.path.join(scriptDir, self.cameraPkg)
        self.cameraMods = self.LoadModulesFromFolder(self.cameraDir, self.cameraPkg)
                
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
            self.ShowMessage(f"指定されたトラック`{trackIndex}`はありません\nExifの取得対象となるクリップが配置されているトラック番号を入れてください")
            sys.exit()

        addTrackIndex = ret.get("DstTrack", None)
        if addTrackIndex is None or self.IsInt(addTrackIndex) == False:
            raise Exception(f"DstTrack invalid.")
        addTrackIndex = int(addTrackIndex)
        
        # メディアプールのFusionコンポジット取得
        srcFusionComp = self.GetFusionComposite(fusionClipName)
        
        # Fusionタイトル削除
        delRet = self.DeleteFusionTitle(addTrackIndex, fusionClipName)
        if delRet == False:
            self.ShowMessage("出力先のトラックに他のクリップが既に存在します。\n削除してやり直すか別のトラックを指定してください。")
            sys.exit()
        
        # 対象のタイトルパラメーター生成クラスを取得
        titleMods = self.LoadModulesFromFolder(self.titleDir, self.titlePkg)
        if len(titleMods) == 0:
            raise Exception("Title parameter generator module not found")
        titleIns: TitleSetterAbs  = self.FindSubclassInstanceWithName(titleMods, TitleSetterAbs, fusionClipName)
        if titleIns is None:
            self.ShowMessage(f"{fusionClipName}用のプラグインがありません")
            sys.exit()
        
        # 対象のクリップを取得
        trackType = "video"
        clips = self.timeline.GetItemListInTrack(trackType, trackIndex)
        for clip in clips:
                                    
            # Fusionタイトル タイムライン追加
            fusionComp = self.AddToTimeline(clip, srcFusionComp, addTrackIndex)

            mediaPoolItem = clip.GetMediaPoolItem()
            # Exif取得
            e = self.GetExif(mediaPoolItem)
            
            # Fusionタイトルパラメーター設定
            values = titleIns.GenerateFusionParameter(e)
            self.SetFusionParameter(fusionComp, values)            
            
    def LoadModulesFromFolder(self, folder, pkgName) -> dict:
        """指定したフォルダのモジュールを取得する

        Args:
            folder (string): 検索先のフォルダ。ルートからのパス。
            pkgName (string): パッケージ名。スクリプトのルートからのフォルダ構成をドットで繋いだものになるはず…

        Returns:
            dict: モジュールの一覧
        """
        modules = {}
        for _, module_name, is_pkg in pkgutil.iter_modules([folder]):
            if not is_pkg:
                module = importlib.import_module(f"{pkgName}.{module_name}")
                modules[module_name] = module
        return modules

    def FindSubclassInstanceWithName(self, modules, base_class, target_name):
        """モジュール群で特定のクラスを継承したクラスの中から指定した名前のクラスのインスタンスを取得する

        Args:
            modules (dict): 検索対象のモジュールが入った辞書
            base_class (class): クラス。ここで指定したクラスを継承しているクラスを探す
            target_name (string): 名前。ここで指定した名前のクラスインスタンスを取得する

        Returns:
            instance: クラスインスタンス
        """
        for module in modules.values():
            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)
                if isinstance(attribute, type) and issubclass(attribute, base_class) and attribute is not base_class:
                    # クラスが指定したベースクラスのサブクラスであることを確認
                    if hasattr(attribute, 'GetName') and callable(getattr(attribute, 'GetName')):
                        class_instance = attribute()
                        if class_instance.GetName() == target_name:
                            print(f"Found instance of {attribute_name} in module {module.__name__}")
                            return class_instance
        print(f"No subclass of {base_class.__name__} found with name {target_name}")
        return None
        
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
    
    def DeleteFusionTitle(self, trackIndex, targetClipName) -> bool:
        """指定したトラックのFusionタイトルをすべて削除する
        対象外のクリップがある場合は削除しない
        """
        clips = self.timeline.GetItemListInTrack("video", trackIndex)
        if clips is None:
            return
        for clip in clips:
            # 本当ならメディアプールのClip Nameと比較したがったがFusionタイトルとメディアプールが紐付いてないので出来なかった
            if clip.GetName() != targetClipName:
                return False
        self.timeline.DeleteClips(clips)
        return True

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
        
    def GetExif(self, mediaPoolItem) -> ExifInfo:
        """指定されたメディアプールアイテムのExifを取得
        """        
        cameraIns: CameraExifSetterAbs = None
        exif: dict = None
        camera: str = None
        
        filePath = mediaPoolItem.GetClipProperty("File Path")
        if pathlib.Path(filePath).suffix.lower() == ".braw" :
            camera = "BMPCC"
        else:
            exif = information(filePath)
            camera = "standard"
        cameraIns = self.FindSubclassInstanceWithName(self.cameraMods , CameraExifSetterAbs, camera)
        if cameraIns is None:
            self.ShowMessage(f"{camera}用のプラグインがありません")
            sys.exit()
        
        pprint(exif)
        exifinfo = cameraIns.GenerateExifText(exif, mediaPoolItem)
        if exifinfo is None:
            raise Exception("Exit text generate faild")
        return exifinfo
    
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
        
if __name__ == "__main__":
    obj = ExifToFusion().main()
