# YAMLtransについて
YAMLファイルで書いたアドオン情報をdatファイルに変換してあわよくばpak化までしてくれるパッケージです。(jsonはYAMLのサブセットなので、同じ構造であれば読み込めるようです。)

# YAML仕様
```yaml
addons:
  - obj: objtype
    name: addonname
    # etc...(key=value)

    EmptyImage:
	  S: image.0.0
	  SE: image.0.1
	# etc...(key[subKey]=value)

	Constraint:
	  prev:
	    - vehicle_1
	    - vehicle_2
	    - vehicle_3
	  next:
	    - vehicle_1
	    - vehicle_2
	    - vehicle_3
	# etc...(key[subKey][index]=value)

	key:
	  subKey1:
	  	subKey2:
			#...
    #(key[subKey1][subKey2]...=value)

	key:
	  -
	    -
		  - value_0_0_0
          - value_0_0_1
		-
		  - value_0_1_0
		  - value_0_1_1
	  -
	    -
		  - value_1_0_0
		    #...
	#key[index][index][index]...=value

params:
  datpath: datfile.dat
  pakpath: pakfile.pak
  pakset: pak128
  autopak: false
  #imagepreview: false

images:
  - image
  - image
  #...
```
`addons`内のリストをアドオンとして出力します。
オブジェクトを入れ子にすると`[subKey]`として追加します。また、リストはインデックスを自動で追加するので手動でインデックスを振るわずらわしさから解放されます。

`params`内の項目はYAMLtransがdatファイルやpakファイルにする際に利用されます。
- `datpath` -> 出力先のdatfileを指定します
- `pakpath` -> makeobjを走らせた際の出力ファイル名になります(`autopak`を`true`にする必要があります)
- `pakset` -> makeobjを走らせた際のpakset指定になります(`autopak`を`true`にする必要があります)
- `autopak` -> `true`の場合、`YAMLtrans.write()`を実行した際に`makeobj {pakset} {datpath} {pakpath}`を実行します。makeobjの実行ファイルを`makeobj`として実行できるようにpathを設定しておく必要があります
- `imagepreview`(追加予定) -> `true`の場合、`YAMLtrans.convert()`および`YAMLtrans.write()`でリスト内の画像をプレビューします

`images`内のリスト内の画像について、今後プレビュー機能を実装する予定です。

そのほかのkeyについては処理等をしていないので、YAMLのアンカー等としてご活用ください。

なお、yamlのパース自体はPyYaml等のパーサーで行ってください。(逆に、他ライブラリにパースさせているので、パーサーがパースできる形式であればどのような記述でも構いません)
## 特定ワードについて
addons内で特定のワードのオブジェクトがある場合、特殊な処理を行います。なお、特定のワードを含むオブジェクトは必ずそのワード1つのみのオブジェクトにしてください。

また、それぞれの特定ワードは入れ子にすることが出来ます。
### TEXT
```
{TEXT:[str,str ,...]}
```
TEXT内のリストを一つの文字列として認識します。これはアドオン名や画像ファイル指定などでエイリアスを使用した場合等に文字列を連結するために設定されています。
### LIST
```
{LIST:[[content,content,...],[content,[...],[[...]]]]}
```
LIST内のネストされたリストを一次元のリストにします。これは連結設定等でエイリアスを使用した場合等に複数のリストを一つにまとめるために設定されています。
# 導入
このディレクトリで`$pip install .`するとYAMLtransがパッケージとして利用できます。

# 使用方法
## CLIとして
`python -m YAMLtrans`
または
`python -m YAMLtrans <YamlFile>`でYamlファイルを読み込み指定ファイルにdatを出力します。
(ファイルを指定しなかった場合、ファイル指定ダイアログが表示されます。)
## パッケージとして
```python
import YAMLtrans
yt = YAMLtrans.YamlTrans(YamlDict: dict)
```
でYamlTransクラスをインスタンス化できます。

というか実際に処理してるのはdictなのでYAMLじゃなくてもできます。YAMLファイルはPyYAML等でパースしてください。

### YamlTransクラス
[YAMLtrans.md](YAMLtrans.md)を参照