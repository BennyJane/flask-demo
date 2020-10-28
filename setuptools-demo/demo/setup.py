from setuptools import setup, find_packages

setup(
    name='firstApp',  # 应用名
    version='0.0.3',  # 版本号
    # scripts=['python myapp/hello.py'],
    packages=find_packages(),  # 包裹在安装包内的Python包
)
