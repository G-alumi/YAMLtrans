# Module YAMLtrans.main

## Classes

### YamlTrans {: #YamlTrans }

```python
class YamlTrans(self, YamlDict: dict)
```

Yamlファイルからdatファイルに変換するためのクラス

Parameters
----------
__datPath : str
    出力datファイルのパス

__pakPath : str
    出力pakファイルのパス

__pakset : str
    pak化する際にmakeobjに渡すpaksetの引数

__autoPak : bool
    書き出し時にpak化までするかどうか

__imagePreview : bool
    画像プレビューをするかどうか(未実装・要OpenCV?)

__source : dict
    解析語のアドオンソース

Initialize self.  See help(type(self)) for accurate signature.

------

#### Methods {: #YamlTrans-methods }

[**convert**](#YamlTrans.convert){: #YamlTrans.convert }

```python
def convert(self) -> str
```

読み込んだyamlのdictからdatファイルを生成します

Returns
-------
dat : str
    生成されたdat

------

[**write**](#YamlTrans.write){: #YamlTrans.write }

```python
def write(self) -> None
```

読み込んだyamlのdictからdatファイルを生成し、書き出します

yamlのparams.autpakがtrueの場合、makeobjを走らせますが、あらかじめpathを通しておく必要があります
