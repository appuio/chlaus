FROM docker.io/centos/python-36-centos7:latest

COPY --chown=1001:0 src/ /tmp/src

ENV WEB_CONCURRENCY=2

RUN /usr/libexec/s2i/assemble

CMD /usr/libexec/s2i/run
