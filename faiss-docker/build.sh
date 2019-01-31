docker build \
    --build-arg IMAGE=ubuntu:16.04 \
    --build-arg FAISS_CPU_OR_GPU=cpu \
    --build-arg FAISS_VERSION=1.2.1 \
    --tag hqq/faiss-docker:1.2.1-cpu \
     .