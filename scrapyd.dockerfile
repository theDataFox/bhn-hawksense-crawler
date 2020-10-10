FROM python:3.7
MAINTAINER EasyPi Software Foundation

RUN set -xe \
    && apt-get update \
    && apt-get install -y autoconf \
                          build-essential \
                          curl \
                          git \
                          libffi-dev \
                          libssl-dev \
                          libtool \
                          libxml2 \
                          libxml2-dev \
                          libxslt1.1 \
                          libxslt1-dev \
                          vim-tiny \
    && apt-get install -y libtiff5 \
                          libtiff5-dev \
                          libfreetype6-dev \
                          libjpeg62-turbo \
                          libjpeg62-turbo-dev \
                          liblcms2-2 \
                          liblcms2-dev \
                          libwebp6 \
                          libwebp-dev \
                          zlib1g \
                          zlib1g-dev \
    && curl -sSL https://github.com/scrapy/scrapy/raw/master/extras/scrapy_bash_completion -o /etc/bash_completion.d/scrapy_bash_completion \
    && echo 'source /etc/bash_completion.d/scrapy_bash_completion' >> /root/.bashrc

# Install Poetry for external dependencies
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

RUN mkdir app/

COPY ./app /app

WORKDIR /app/

RUN poetry install --no-root --no-dev

RUN python -m nltk.downloader punkt && python -m nltk.downloader stopwords
#RUN [ "python", "-c", "import nltk; nltk.download('all')" ]

# set python path so alembic runs correctly but do not overwrite previous env variables set in docker compose
#RUN export PYTHONPATH="$PYTHONPATH:/app"
ENV PYTHONPATH="$PYTHONPATH:/app"

COPY ./app/scrapyd.conf /etc/scrapyd/
VOLUME /etc/scrapyd/ /var/lib/scrapyd/
EXPOSE 6800

CMD ["scrapyd", "--pidfile="]

#RUN chmod +x scripts/alembic-init.sh
# entrpoint only will work not RUN as this only works after build is complete
#CMD ["bash", "scripts/alembic-init.sh"]

#$ mkvirtualenv -p python3 webbot
#$ pip install scrapy scrapyd-client
#
#$ scrapy startproject myproject
#$ cd myproject
#$ setvirtualenvproject
#
#$ scrapy genspider myspider mydomain.com
#$ scrapy edit myspider
#$ scrapy list
#
#$ vi scrapy.cfg
#$ scrapyd-client deploy
#$ curl http://localhost:6800/schedule.json -d project=myproject -d spider=myspider
