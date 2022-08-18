# furigana-maker

## Requirements
- brew
- nodebrew
- node


## Node のアップデート
```bash
# インストール可能なバージョンを確認
nodebrew ls-remote
```
```bash
# nodeのインストール
nodebrew install-binary <version>
```
```bash
# 使いたいバージョンを指定
nodebrew use v10.15.0
```

## package.json に記載されているパッケージのバージョンアップ方法
```bash
# アップデート可能なパッケージの確認
npx -p npm-check-updates  -c "ncu"
```
```bash
# package.json が更新する
npx -p npm-check-updates  -c "ncu -u"
```
```bash
# パッケージのインストール
npm install
```