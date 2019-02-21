# 
# Docker environment for QSSLCAUDIT testing
# Uses standard OpenSSL libraries
#
# Prepare image: docker build -t ubuntu-bionic -f path/to/Dockerfile .
# Run instance:  docker run --name ubuntu-bionic --rm -it ubuntu-bionic
#

FROM ubuntu:bionic as stage1
# prebuild stage
RUN apt-get update && apt-get -y install make gcc zlib1g zlib1g-dev bzip2 perl
# add files
ADD . /build
WORKDIR /build
# build stage
RUN ./build.sh
# postbuild stage
RUN echo post build

FROM ubuntu:bionic
WORKDIR /root/


CMD ["/bin/true"]  