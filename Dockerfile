FROM python:3-jessie as pacparser

# Get pacparser from GitHub
WORKDIR /usr/src/
RUN git clone https://github.com/manugarg/pacparser.git

WORKDIR /usr/src/pacparser

RUN apt-get update && apt-get install -y --no-install-recommends \
    python-dev \
    python-setuptools

# Build pacparser
RUN make -C src all pymod install-pymod

COPY . .

CMD [ "python", "./test.py", "-p proxy.pac", "-f test-data.csv" ]
