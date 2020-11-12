ARG BUILD_FROM
FROM ${BUILD_FROM}

ENV LANG C.UTF-8

# Copy data for add-on
COPY run.sh pvoutput_uploader.py /

RUN apk add --no-cache python3 py3-pip
RUN pip3 install --no-cache-dir requests

RUN chmod a+x /run.sh
CMD [ "/run.sh" ]
