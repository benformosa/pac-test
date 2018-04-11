FROM debian:jessie

# Install pacparser Python module, and Python
# We use Debian's packaged version of Python, which can find this module
RUN apt-get update && apt-get install -y --no-install-recommends \
        python-pacparser \
    && rm -rf /var/lib/apt/lists/*

COPY . .

CMD [ "sh", "./test.sh" ]
