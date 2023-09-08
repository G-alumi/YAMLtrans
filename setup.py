from setuptools import setup, find_packages

setup(
    name="YAMLtrans",
    version="0.1.0",
    description="YAMLをsimutrans datファイルに変換するための機能",
    author="G_lumi",
    packages=find_packages(),
    license="LGPL",
    install_requires=[
        "PyYAML",
    ],
)