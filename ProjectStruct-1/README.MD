### 单个App实例项目结构设计

### 待补充的内容
1. 添加蓝图模块
2. 优化.env环境变量的使用
3. 添加数据库配置

### 打包发布线上部署流程
```bash
# 项目根目录下
python setup.py sdist

# 将生成的dist目录下压缩文件复制到目标目录下(线上部署主机上)
# 先生成信达 虚拟环境；并激活 ；
virtual env
source ./env/bin/activate
# 将打包文件安装到当前python环境的site-packages 内
pip install ./flask-pro1.0.1.0.tar.gz
# 查看安装好的包
pip list

# 进入python虚拟环境, 测试
# python
# from proStruct import app
# app.run()

# 使用 gunicorn 运行
gunicorn packageName:app 
```

### 项目目录文件解释

### Dockerfile 生成镜像文件
```bash
sudo docker build -t 'proStruct'
sudo docker images

sudo docker run -it --rm -p 8001:80001 proStruct

sudo docker run -d -p 8001:8001 --name online-pro proStruct

```