import os
import subprocess
from setuptools import setup, find_packages


def getInstallPackages():
    '''获取'''
    res = []
    path = './requirement.txt'
    if not os.path.exists(path):
        # 生成requirement文件
        subprocess.check_output(['python', 'freeze >', 'requirement.txt'])
    with open('./requirement.txt', 'r') as f:
        installed_packages = f.readlines()
    for package in installed_packages:
        package = package.strip()
        res.append(package)
    return res

#
# current_installed_packages = getInstallPackages()
# print(current_installed_packages)
setup(
    # 指明包名称
    name='flask-pro1',
    version=f'0.1.0',
    author='benny',
    author_email='123456@qq.com',
    url='http://base.com',
    include_package_data=True,
    packages=find_packages(),
    install_requires=['click==7.1.2', 'Flask==1.1.2', 'gunicorn==20.0.4', 'itsdangerous==1.1.0', 'Jinja2==2.11.2',
                      'MarkupSafe==1.1.1', 'python-dotenv==0.14.0', 'Werkzeug==1.0.1']
)
