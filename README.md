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

* 既に追加先のトラックに他のFusionタイトルが追加されている状態だとエラーになります。一度Fusionタイトルを消すか別のトラックに作成してください。
* スクリプトが動作しないときは一度Fusionページを表示してから実行してください
* スクリプトにショートカットを割り当てて実行する場合、DaVinci Resolve起動後一回目は`ワークスペース` > `スクリプト` から実行してください。理由は分かりませんが初回はショートカットではスクリプトが実行されません。

## 使い方

## 参考

