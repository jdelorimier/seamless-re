FROM python:3.7-slim-bullseye

# Install pymgclient
RUN apt-get update && \
    apt-get install -y git cmake make gcc g++ libssl-dev && \
    git clone --recursive https://github.com/memgraph/pymgclient /pymgclient && \
    cd pymgclient && \
    git checkout v1.1.0 && \
    python3 setup.py install && \
    python3 -c "import mgclient"

# Install poetry
RUN python3 -m pip install -U pip \
 && python3 -c "import urllib.request; print(urllib.request.urlopen('https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py').read().decode('utf-8'))" | python3

ENV PATH="${PATH}:/root/.poetry/bin"

RUN git clone https://github.com/thunlp/OpenNRE.git && \
    # pip install -r OpenNRE/requirements.txt \
    # python3 OpenNRE/setup.py install \
    # bash OpenNRE/benchmark/download_fewrel.sh
    apt-get install wget && \
    mv OpenNRE ~/.opennre && \
    mkdir ~/.opennre/benchmark/wiki80 && \ 
    wget -P ~/.opennre/benchmark/wiki80 https://thunlp.oss-cn-qingdao.aliyuncs.com/opennre/benchmark/wiki80/wiki80_rel2id.json && \
    wget -P ~/.opennre/pretrain/bert-base-uncased https://thunlp.oss-cn-qingdao.aliyuncs.com/opennre/pretrain/bert-base-uncased/config.json  && \
    wget -P ~/.opennre/pretrain/bert-base-uncased https://thunlp.oss-cn-qingdao.aliyuncs.com/opennre/pretrain/bert-base-uncased/pytorch_model.bin  && \
    wget -P ~/.opennre/pretrain/bert-base-uncased https://thunlp.oss-cn-qingdao.aliyuncs.com/opennre/pretrain/bert-base-uncased/vocab.txt


WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Download spacy packages
RUN python3 -m spacy download en_core_web_lg

COPY . /app
EXPOSE 5000

ADD start.sh /
RUN chmod +x /start.sh

ENTRYPOINT [ "poetry", "run" ]
CMD ["/start.sh"]