#一套重新生成镜像的命令

#停止容器
docker ps |grep faiss| awk '{print $1}'|xargs docker stop
#删除镜像
docker images | grep 'faiss-web-service' | awk '{print $3}' |xargs docker rmi -f
#重新生成镜像
sh buildDocker.sh
#删除旧镜像
rm -rf /Users/huangqq/soft/docker/faiss/faiss-search.tar
#导出镜像
docker images | grep 'faiss-web-service' | awk '{print $3}' |xargs docker save > /Users/huangqq/soft/docker/faiss/faiss-search.tar
#上传跳板机
rsync -av /Users/huangqq/soft/docker/faiss/faiss-search.tar root@124.243.219.212::data_dev_upload/
