import yaml
import subprocess
import sys


class YamlTrans:
    """
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
    """
    __datPath: str = "output.dat"
    __pakPath: str = "output.pak"
    __pakset: str = "pak128"
    __autoPak: bool = False
    __imagePreview: bool = False
    __source: dict



    def __init__(self, YamlDict: dict):
        self.__source = self.__parse(YamlDict)

        source: dict = self.__source
        if "params" in source:
            if "datpath" in source["params"]:
                self.__datPath = source["params"]["datpath"]
            if "pakpath" in source["params"]:
                self.__pakPath = source["params"]["pakpath"]
            if "pakset" in source["params"]:
                self.__pakset = source["params"]["pakset"]
            if "autopak" in source["params"]:
                self.__autoPak = source["params"]["autopak"]

        print("datPath",self.__datPath)
        print("pakPath",self.__pakPath)
        print("pakset",self.__pakset)
        print("autopak",self.__autoPak)
                



    def convert(self) -> str:
        """
        読み込んだyamlのdictからdatファイルを生成します

        Returns
        -------
        dat : str
            生成されたdat
        """
        return self.__toDat(self.__source)
    


    def write(self) -> None:
        """
        読み込んだyamlのdictからdatファイルを生成し、書き出します\n
        yamlのparams.autpakがtrueの場合、makeobjを走らせますが、あらかじめpathを通しておく必要があります
        """
        with open(self.__datPath,"w") as datFile:
            datFile.write(self.convert())
        if self.__autoPak:
            subprocess.run(f"makeobj {self.__pakset} {self.__pakPath} {self.__datPath}")
        pass

    def __parse(self, obj: any) ->any:
        """
        特定語を探して変換する。

        Parameters
        ----------
        obj : any
            解析する物体。

        Returns
        -------
        result : any
            解析後の物体。特定語のdictでない限りは入力値と同じものが返ります。
        """

        def parseLIST(obj: any) ->list:
            """
            特定語"LIST"を変換する。
            入力されたlistを一次元化します。中の要素に関しても構文解析をします。

            Parameters
            ----------
            obj : any
                一次元化するlistまたはlistを返す特定語を含むdict

            Returns
            -------
            result : list
                解析後の物体。一次元化されたlistです。
            """
            result: list = []
            if type(obj) is dict:
                result.append(self.__parse(obj))
            elif type(obj) is list:
                for content in obj:
                    result.extend(parseLIST(content))
            else:
                result.append(obj)
            return result

        def parseTEXT(obj: any) ->str:
            """
            特定語"TEXT"を変換する。
            入力されたlistを1つの文字列に結合します。中の要素に関しても構文解析をします。

            Parameters
            ----------
            obj : any
                1つの文字列に連結するlistまたはlistを返す特定語を含むdict

            Returns
            -------
            result : str
                解析後の物体。連結されたstrです。
            """
            result: str = ""
            if type(obj) is dict or type(obj) is list:
                result = "".join(self.__parse(obj))
            else:
                result = str(obj)
            return result

        if type(obj) is dict:
            resultDict: dict = {}
            for key, value in obj.items():
                if key == "LIST":
                    return parseLIST(value)
                elif key == "TEXT":
                    return parseTEXT(value)
                else:
                    resultDict[key] = self.__parse(value)
            return resultDict
        
        elif type(obj) is list:
            resultLIST: list = []
            for elem in obj:
                resultLIST.append(self.__parse(elem))
            return resultLIST
        elif type(obj) is bool:
            return obj
        else:
            return str(obj)

    def __toDat(self, yamlObj: dict) -> str:
        """
        アドオンのdictをDatファイル形式のstrにします。

        Parameters
        ----------
        yamlObjct : dict
            アドオンのdict

        Returns
        -------
        result : str
            生成されたDat形式のstr
        """
        
        def unpack(parentKey: str,contents: any) ->str:
            """
            入力されたparentKeyとcontentsを"parentKey=contents"の形のstrにします
            contentsの中のdictはkey名を、listは先頭に0からのインデックスを付けます。

            Parameters
            ----------
            parentKey : str
                datの項目
            contents : any
                パラメータ
                dictの場合は[key]を、listの場合はインデックスをparentKeyの末尾に付けます。

            Returns
            -------
            result : str
                "parentKey=contents"の形のstr
            """
            
            def unpackDict(parentKey: str,contents: dict) ->str:
                """
                入力されたparentKeyとcontentsを"parentKey=contents"の形のstrにします
                contentsのkey名のインデックスを付けます。

                Parameters
                ----------
                parentKey : str
                    datの項目
                contents : dict
                    パラメータ
                    [key]をparentKeyの末尾に付けます。

                Returns
                -------
                result : str
                    "parentKey=contents"の形のstr
                """
                result: str = ""
                for key, value in contents.items():
                    genKey: str = f"{parentKey}[{key}]"
                    if type(value) is dict or type(value) is list:
                            result += unpack(genKey,value)
                    else:
                        result += f"{genKey}={value}\n"
                return result
            
            def unpackList(parentKey: str,contents: list) -> str:
                """
                入力されたparentKeyとcontentsを"parentKey=contents"の形のstrにします
                contentsのインデックスを付けます。

                Parameters
                ----------
                parentKey : str
                    datの項目
                contents : list
                    パラメータ
                    インデックスをparentKeyの末尾に付けます。

                Returns
                -------
                result : str
                    "parentKey=contents"の形のstr
                """
                result: str = ""
                index: int = 0
                for content in contents:
                    genKey: str = f"{parentKey}[{index}]"
                    if type(content) is dict or type(content) is list:
                        result += unpack(genKey,content)
                    else:
                        result += f"{genKey}={content}\n"
                    index += 1
                return result
            
            result: str = ""
            if type(contents) is dict:
                result += unpackDict(parentKey, contents)
            elif type(contents) is list:
                result += unpackList(parentKey, contents)
            else:
                result += f"{parentKey}={contents}\n"
            
            return result

        result: str = """    ############################
    #  Converted by YAMLtrans  #
    ############################

# https://github.com/G-alumi/YAMLtrans

"""
        for addon in yamlObj["addons"]:
            for key, value in addon.items():
                result += unpack(key, value)
            result += "--------\n"
        return result


def main() -> None:
    yamlPath: str
    args = sys.argv
    if len(args) > 1:
        yamlPath = args[1]
    else:
        yamlPath = input("Yaml file:")
    with open(yamlPath) as yamlFile:
        yamlTrans: YamlTrans = YamlTrans(yaml.safe_load(yamlFile))
        yamlTrans.write()



if __name__ == "__main__":
    main()