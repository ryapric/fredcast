FROM python:3.7-stretch

COPY . /root
WORKDIR /root

RUN pip3 install -r requirements.txt \
    && rm -rf $HOME/.cache/pip

CMD ["python3", "main.py"]
