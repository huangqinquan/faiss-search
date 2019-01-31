sudo docker run -d \
    --privileged \
    --volume /www/faiss-search/logs:/var/log/faiss_web_service \
    --publish 25000:5000 \
    hqq/faiss-web-service:0.0.1-cpu $*