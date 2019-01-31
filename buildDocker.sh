docker build \
    --build-arg "--sysctl net.core.somaxconn=65535" \
    --tag hqq/faiss-web-service:0.0.1-cpu .