# ExifToFusion

動画や写真のEXIF情報を取得し各種Fusionタイトルにセットしてタイムラインに追加するスクリプトです

DaVinci Resolve 19 Studioで動作確認しています。

## フレーム調整設定

タイトルの配置期間を環境に応じて調整できます。`settings.json`ファイルで`frameAdjustment`の値を設定してください。

- **ドロップフレーム環境** (29.97fps, 59.94fps): `-1` を推奨
- **ノンドロップフレーム環境** (24fps, 25fps, 30fps, 60fps): `0` を推奨

設定例：
```json
{
    "frameAdjustment": -1
}
```

詳しい使い方は

https://github.com/a-tak/ExifToFusion/wiki

に記載していきます(作成中!)
