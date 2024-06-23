# ExifToFusion

## はじめに

Windows環境での使い方を記載。Macの場合は[こちら](https://note.com/littlebuddha/n/nf7325e8c16ea)参考にされると良いかもしれません。

DaVinci Resolve 19 Studioで動作確認しています。

## 注意事項

スクリプトの中にはデータの書き換えを行うものもあります。利用によってデータの消失がないとも言えません。利用する際には素材のバックアップをした上で行ってください。

## Pythonインストール

なぜかGUIのインストーラーではDaVinci Resolveから認識されなくて、Chocolateyだとうまくいった。

PowerShellを管理者権限で起動して以下実行。

```
choco install -y python3
```

## 環境変数設定

以下のドキュメントに沿って環境変数を指定。

`C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\README.txt`

ただし、PYTHONPATHについては絶対パスじゃない動作しなかったので以下のように設定した。

`%PYTHONPATH%;C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules`

つまりこれをWindowsの環境変数に入れる

```
RESOLVE_SCRIPT_API="%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
RESOLVE_SCRIPT_LIB="C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
PYTHONPATH="%PYTHONPATH%;C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules"
```

PowerShellで以下のコマンドを入れてもよい

```powershell
[Environment]::SetEnvironmentVariable('RESOLVE_SCRIPT_API','%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting', 'User')
[Environment]::SetEnvironmentVariable('RESOLVE_SCRIPT_LIB','C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll', 'User')
[Environment]::SetEnvironmentVariable('PYTHONPATH','%PYTHONPATH%;C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules', 'User')
```

## Exiftoolインストール

Exiftoolのインストールが必要になります。

```powershell
choco install exiftool
```

##  Pythonモジュール
```powershell
pip install pyexifinfo
```

## 作成したスクリプトの置き場

`C:\ProgramData\Blackmagic Design\DaVinci Resolve\Fusion\Scripts\Comp`
または
`%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Comp`

## 環境設定の変更

`環境設定` > `システム` > `一般` > `一般環境設定` > `外部スクリプトに使用` を `ローカル` に変更

## スクリプトの実行

`ワークスペース` の `スクリプト` から実行可能

## エラーが出る場合

```python
Traceback (most recent call last):
  File "<nofile>", line 5, in <module>
ModuleNotFoundError: No module named 'pyexifinfo'
```

DaVinci Resolveから参照出来ない場所にpyexifinfoモジュールがインストールされています。

インストール先の確認は以下コマンド

```
pip show pyexifinfo
```

```
Name: pyexifinfo
Version: 0.4.0
Summary: Simple Metadata extraction using Exiftool
Home-page: https://github.com/guinslym/pyexifinfo
Author: Guinslym
Author-email: guinslym@gmail.com
License: GNU GPLv2
Location: C:\Python311\Lib\site-packages
Requires:
Required-by:
```

`Location`がインストール先です。

DaVinci Resolveが参照する場所は以下をDaVinci Resolveの`ワークスペース` > `コンソール` を開き、上の `Py3` ボタンを押した後に下記を入力して確認出来ます。

```python
import sys
print(sys.path)
```

```
['C:\\Program Files\\Blackmagic Design\\DaVinci Resolve', 'C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\%PYTHONPATH%', 'C:\\ProgramData\\Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting\\Modules', 'C:\\tools\\Anaconda3\\python311.zip', 'C:\\tools\\Anaconda3\\DLLs', 'C:\\tools\\Anaconda3\\Lib', 'C:\\Program Files\\Blackmagic Design\\DaVinci Resolve', 'C:\\tools\\Anaconda3', 'C:\\tools\\Anaconda3\\Lib\\site-packages', 'C:\\tools\\Anaconda3\\Lib\\site-packages\\win32', 'C:\\tools\\Anaconda3\\Lib\\site-packages\\win32\\lib', 'C:\\tools\\Anaconda3\\Lib\\site-packages\\Pythonwin']
```

`Location`のパスが含まれていない場合は環境変数に追加が必要です。こんな感じです。

```
PYTHONPATH="%PYTHONPATH%;C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules;C:\Python311\Lib\site-packages"
```
PowerShellの場合以下のようにコマンドを変更すればよいです。

```powershell
[Environment]::SetEnvironmentVariable('PYTHONPATH','%PYTHONPATH%;C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules;C:\Python311\Lib\site-packages' , 'User')
```

DaVinci Resolveは再起動してください。

## 注意事項


## 使い方

## 参考

### GH6のメタデータ

```
{'SourceFile': 'E:/DaVinci Resolve Data/2022-04-02_?X?N???v?g?e?X?g/P1010025.MOV',
'ExifTool:ExifToolVersion': 12.4,
 'ExifTool:Warning': 'FileName encoding not specified',
 'File:Directory': 'E:/DaVinci Resolve Data/2022-04-02_?X?N???v?g?e?X?g',
 'File:FileAccessDate': '2022:04:02 20:36:17+09:00',
 'File:FileCreateDate': '2022:04:02 14:15:33+09:00',
 'File:FileModifyDate': '2022:04:02 14:08:07+09:00',
 'File:FileName': 'P1010025.MOV',
 'File:FilePermissions': '-rw-rw-rw-',
 'File:FileSize': '248 MiB',
 'File:FileType': 'MOV',
 'File:FileTypeExtension': 'mov',
 'File:MIMEType': 'video/quicktime',
 'File:ZoneIdentifier': 'Exists',
 'QuickTime:AudioBitsPerSample': 16,
 'QuickTime:AudioChannels': 3,
 'QuickTime:AudioFormat': 'lpcm',
 'QuickTime:AudioSampleRate': 1,
 'QuickTime:BackgroundColor': '0 0 0',
 'QuickTime:Balance': 0,
 'QuickTime:BitDepth': 24,
 'QuickTime:CompatibleBrands': ['qt  ',
 'pana'],
 'QuickTime:CompressorID': 'hvc1',
 'QuickTime:CreateDate': '2022:03:29 23:57:56',
 'QuickTime:CurrentTime': '0 s',
 'QuickTime:Duration': '7.01 s',
 'QuickTime:FontName': '',
 'QuickTime:GenBalance': 0,
 'QuickTime:GenFlags': '0 0 0',
 'QuickTime:GenGraphicsMode': 'ditherCopy',
 'QuickTime:GenMediaVersion': 0,
 'QuickTime:GenOpColor': '32768 32768 32768',
 'QuickTime:GraphicsMode': 'ditherCopy',
 'QuickTime:HandlerClass': 'Data Handler',
 'QuickTime:HandlerType': 'Metadata Tags',
 'QuickTime:ImageHeight': 2160,
 'QuickTime:ImageWidth': 3840,
 'QuickTime:MajorBrand': 'Apple QuickTime (.MOV/QT)',
 'QuickTime:MatrixStructure': '1 0 0 0 1 0 0 0 1',
 'QuickTime:MediaCreateDate': '2022:03:29 23:57:56',
 'QuickTime:MediaDataOffset': 2490880,
 'QuickTime:MediaDataSize': 257967538,
 'QuickTime:MediaDuration': '7.01 s',
 'QuickTime:MediaHeaderVersion': 0,
 'QuickTime:MediaLanguageCode': 'und',
 'QuickTime:MediaModifyDate': '2022:03:29 23:57:56',
 'QuickTime:MediaTimeScale': 120000,
 'QuickTime:MinorVersion': '2011.7.0',
 'QuickTime:ModifyDate': '2022:03:29 23:57:56',
 'QuickTime:MovieHeaderVersion': 0,
 'QuickTime:NextTrackID': 7,
 'QuickTime:OpColor': '32768 32768 32768',
 'QuickTime:OtherFormat': 'tmcd',
 'QuickTime:PanasonicSemi-ProMetadataXml': '
 <?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<ClipMain xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns="urn:schemas-Professional-Plug-in:Semi-Pro:ClipMetadata:v1.0">
  <ClipContent>
    <GlobalClipID>1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF</GlobalClipID>
    <Duration>840</Duration>
    <EditUnit>1001/120000</EditUnit>
    <EssenceList>
      <Video>
        <Codec BitRate="300">H265_420_LongGOP</Codec>
        <ActiveLine>2160</ActiveLine>
        <ActivePixel>3840</ActivePixel>
        <BitDepth>10</BitDepth>
        <FrameRate>119.88p</FrameRate>
        <TimecodeType>Drop</TimecodeType>
        <StartTimecode>00:02:39:03</StartTimecode>
      </Video>
      <Audio>
        <Channel>4</Channel>
        <SamplingRate>48000</SamplingRate>
        <BitsPerSample>24</BitsPerSample>
      </Audio>
    </EssenceList>
    <ClipMetadata>
      <Rating>0</Rating>
      <Access>
        <CreationDate>2022-03-30T08:57:56+09:00</CreationDate>
        <LastUpdateDate>2022-03-30T08:57:56+09:00</LastUpdateDate>
      </Access>
      <Device>
        <Manufacturer>Panasonic</Manufacturer>
        <ModelName>DC-GH6</ModelName>
      </Device>
      <Shoot>
        <StartDate>2022-03-30T08:57:56+09:00</StartDate>
      </Shoot>
    </ClipMetadata>
  </ClipContent>
  <UserArea>
    <AcquisitionMetadata xmlns="urn:schemas-Professional-Plug-in:P2:CameraMetadata:v1.2">
      <CameraUnitMetadata>
        <ISOSensitivity>250</ISOSensitivity>
        <WhiteBalanceColorTemperature>5600K</WhiteBalanceColorTemperature>
        <Gamma>
          <CaptureGamma>V-Log</CaptureGamma>
        </Gamma>
        <Gamut>
          <CaptureGamut>V-Gamut</CaptureGamut>
        </Gamut>
      </CameraUnitMetadata>
    </AcquisitionMetadata>
  </UserArea>
</ClipMain>
',
 'QuickTime:PanasonicSemi-ProMetadataXml-jpn-JP': '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<ClipMain xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns="urn:schemas-Professional-Plug-in:Semi-Pro:ClipMetadata:v1.0">
  <ClipContent>
    <GlobalClipID>1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF</GlobalClipID>
    <Duration>840</Duration>
    <EditUnit>1001/120000</EditUnit>
    <EssenceList>
      <Video>
        <Codec BitRate="300">H265_420_LongGOP</Codec>
        <ActiveLine>2160</ActiveLine>
        <ActivePixel>3840</ActivePixel>
        <BitDepth>10</BitDepth>
        <FrameRate>119.88p</FrameRate>
        <TimecodeType>Drop</TimecodeType>
        <StartTimecode>00:02:39:03</StartTimecode>
      </Video>
      <Audio>
        <Channel>4</Channel>
        <SamplingRate>48000</SamplingRate>
        <BitsPerSample>24</BitsPerSample>
      </Audio>
    </EssenceList>
    <ClipMetadata>
      <Rating>0</Rating>
      <Access>
        <CreationDate>2022-03-30T08:57:56+09:00</CreationDate>
        <LastUpdateDate>2022-03-30T08:57:56+09:00</LastUpdateDate>
      </Access>
      <Device>
        <Manufacturer>Panasonic</Manufacturer>
        <ModelName>DC-GH6</ModelName>
      </Device>
      <Shoot>
        <StartDate>2022-03-30T08:57:56+09:00</StartDate>
      </Shoot>
    </ClipMetadata>
  </ClipContent>
  <UserArea>
    <AcquisitionMetadata xmlns="urn:schemas-Professional-Plug-in:P2:CameraMetadata:v1.2">
      <CameraUnitMetadata>
        <ISOSensitivity>250</ISOSensitivity>
        <WhiteBalanceColorTemperature>5600K</WhiteBalanceColorTemperature>
        <Gamma>
          <CaptureGamma>V-Log</CaptureGamma>
        </Gamma>
        <Gamut>
          <CaptureGamut>V-Gamut</CaptureGamut>
        </Gamut>
      </CameraUnitMetadata>
    </AcquisitionMetadata>
  </UserArea>
</ClipMain>
',
 'QuickTime:PosterTime': '0 s',
 'QuickTime:PreferredRate': 1,
 'QuickTime:PreferredVolume': '100.00%',
 'QuickTime:PreviewDuration': '0 s',
 'QuickTime:PreviewTime': '0 s',
 'QuickTime:SelectionDuration': '0 s',
 'QuickTime:SelectionTime': '0 s',
 'QuickTime:SourceImageHeight': 2160,
 'QuickTime:SourceImageWidth': 3840,
 'QuickTime:TextColor': '0 0 0',
 'QuickTime:TextFace': 'Plain',
 'QuickTime:TextFont': 'System',
 'QuickTime:TextSize': 12,
 'QuickTime:TimeCode': 6,
 'QuickTime:TimeScale': 120000,
 'QuickTime:TrackCreateDate': '2022:03:29 22:22:22',
 'QuickTime:TrackDuration': '7.01 s',
 'QuickTime:TrackHeaderVersion': 0,
 'QuickTime:TrackID': 1,
 'QuickTime:TrackLayer': 0,
 'QuickTime:TrackModifyDate': '2022:03:29 22:22:22',
 'QuickTime:TrackVolume': '0.00%',
 'QuickTime:VideoFrameRate': 119.88,
 'QuickTime:XResolution': 72,
 'QuickTime:YResolution': 72,
 'MakerNotes:Model': 'DC-GH6',
 'Composite:AvgBitrate': '295 Mbps',
 'Composite:ImageSize': '3840x2160',
 'Composite:Megapixels': 8.3,
 'Composite:Rotation': 0}
```
