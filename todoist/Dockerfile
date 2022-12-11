ARG BUILD_FROM
FROM $BUILD_FROM

RUN \
    apk add --no-cache \
      python3.9 \
      python3.9-dev

RUN \
    python3.9 -m pip install --upgrade pip; \
    python3.9 -m pip install \
        todoist-python

WORKDIR /data

# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
