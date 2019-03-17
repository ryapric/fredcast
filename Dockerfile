FROM python:3.7-stretch

COPY . /root
WORKDIR /root

# Note that you'll need a dummy README so changes to the real one can be
# .dockerignored, and so package build runs
RUN touch README.md \
    && pip3 install . \
    && rm -rf $HOME/.cache/pip

CMD ["fcast-listen"]
