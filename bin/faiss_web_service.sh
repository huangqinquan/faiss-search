#!/bin/sh

sysctl net.core.somaxconn=65535
sysctl -p /usr/bin/supervisord

ROOT=$(realpath $(dirname ${0})/..)

development () {
  python ${ROOT}/src/app.py
}

production () {
    mkdir -p /var/log/faiss_web_service

    uwsgi \
        --ini /opt/faiss-web-service/bin/uWSGI.ini &
        #--http :5000 \
        #--chdir ${ROOT}/src \
        #--module app:app \
        #--master \
        #--enable-threads \
        #--processes 10 \
        #--threads 12 \
        #--listen 65535 \
        #--gevent 40 \
        #--gevent-monkey-patch \
        #--metric-dir /var/log/faiss_web_service \
        #--logto /var/log/faiss_web_service/app.log \
        #--daemonize /var/log/uwsgi.log &

}

case "${1}" in
   "production") production ;;
   *) production ;;
esac

touch /var/log/1.txt &&
tail -f /var/log/1.txt
