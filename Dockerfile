FROM debian:jessie

# Install pacparser Python module
# We use Debian's included version of Python, which can find this module
RUN apt-get update && apt-get install -y --no-install-recommends \
        python-pacparser \
    && rm -rf /var/lib/apt/lists/*

COPY . .

CMD [ "python", "./test.py", "-p proxy.pac", "-f test-data.csv" ]
