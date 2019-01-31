# faiss-search服务部署介绍
## 开发模式
直接运行app.py来启动web服务
## 生产模式
运行bin目录下的faiss_web_service.sh来通过uwsgi启动服务
sh bin/faiss_web_service.sh production
## 目录介绍
- bin:启动脚本文件
- faiss-docker:用来创建带有anconda环境的虚拟机
- log:日志目录
- src:源代码目录
- tmp:存放索引文件目录
- buildDocker.sh Dockerfile:在前一个虚拟机基础上部署本程序
- requirements.txt:项目依赖
