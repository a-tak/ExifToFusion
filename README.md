# ExifToFusion

詳しい使い方は

https://github.com/a-tak/ExifToFusion/wiki

に記載していきます(作成中!)

## はじめに

動画や写真のEXIF情報を取得し各種Fusionタイトルにセットしてタイムラインに追加するスクリプトです

DaVinci Resolve 19 Studioで動作確認しています。

## 注意事項

スクリプトの中にはデータの書き換えを行うものもあります。利用によってデータの消失がないとも言えません。利用する際には素材のバックアップをした上で行ってください。

## Pythonインストール

Windows環境での例を記載。

なぜかGUIのインストーラーではDaVinci Resolveから認識されなくて、Chocolateyだとうまくいった。

Chocolateyのインストールはこちら。
https://chocolatey.org/install#individual

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
choco install -y exiftool
```

## 作成したスクリプトの置き場

`C:\ProgramData\Blackmagic Design\DaVinci Resolve\Fusion\Scripts\Comp`
または
`%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Comp`

## 環境設定の変更

`環境設定` > `システム` > `一般` > `一般環境設定` > `外部スクリプトに使用` を `ローカル` に変更

## 使い方

### メディアプールにタイトルを登録

このスクリプトはメディアプールに登録してあるタイトルを使用します。
現在、対応しているタイトルは以下です。

* Text+
* [G-ExifText](https://note.com/gaipromotion/n/n6e55aa1a0d5f)

スクリプトで処理したいタイトルを`一度タイムラインにドロップして`、サイズや位置などを調整した後、タイムラインに入れたタイトルを`メディアプールにドロップして登録してください。`

### スクリプトの実行

`ワークスペース` の `スクリプト` から実行可能

#### 注意事項

* 既に追加先のトラックに他のFusionタイトルが追加されている状態だとエラーになります。一度Fusionタイトルを消すか別のトラックに作成してください。
* スクリプトが動作しないときは一度Fusionページを表示してから実行してください
* スクリプトにショートカットを割り当てて実行する場合、DaVinci Resolve起動後一回目は`ワークスペース` > `スクリプト` から実行してください。理由は分かりませんが初回はショートカットではスクリプトが実行されません。

