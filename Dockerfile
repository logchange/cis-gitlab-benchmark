FROM alpine:3

# Labels.
LABEL org.opencontainers.image.authors='peter.zmilczak@gmail.com' \
      org.opencontainers.image.url='https://github.com/logchange/cis-gitlab-benchmark' \
      org.opencontainers.image.documentation='https://github.com/logchange/cis-gitlab-benchmark/blob/master/README.md' \
      org.opencontainers.image.source='https://github.com/logchange/cis-gitlab-benchmark' \
      org.opencontainers.image.vendor='The logchange Community' \
      org.opencontainers.image.licenses='Apache-2.0'

RUN apk --update --no-cache add  \
    bash  \
    git  \
    git-lfs \
    python3 \
    py3-pip \
    maven  \
    openjdk8

ENV OPT="/opt/cis-gitlab-benchmark/"
ADD requirements.txt $OPT
RUN pip3 install --break-system-packages --user -r ${OPT}requirements.txt
ADD src $OPT/src
ADD __main__.py $OPT
ENV PYTHONPATH="${PYTHONPATH}:${OPT}"

ARG WORKING_REPO_PATH="/repository"
RUN mkdir $WORKING_REPO_PATH
WORKDIR $WORKING_REPO_PATH


CMD ["python3", "-u", "/opt/cis-gitlab-benchmark"]
