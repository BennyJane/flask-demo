# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : example_02
# Time       ：2021/1/3 21:23
# Warning    ：The Hard Way Is Easier
import yaml  # pip install pyyaml


def read_yaml(config_path):
    """
    config_path:配置文件路径
    """
    if config_path:
        with open(config_path, 'r', encoding='utf-8') as f:
            conf = yaml.safe_load(f.read())
            return conf
    else:
        raise ValueError('请输入正确的配置名称或配置文件路径')
