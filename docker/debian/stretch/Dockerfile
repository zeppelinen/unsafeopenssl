# 
# Docker environment for QSSLCAUDIT testing
# Uses standard OpenSSL libraries
#
# Prepare image: docker build -t debian-stretch -f path/to/Dockerfile .
# Run instance:  docker run --name debian-stretch --rm -it debian-stretch
#

FROM debian:stretch as stage1
# prebuild stage
RUN apt-get update && apt-get -y install make gcc zlib1g zlib1g-dev bzip2 perl perl-base
# add files
ADD . /build
WORKDIR /build
# build stage
RUN ./build.sh
# postbuild stage
RUN echo post build

FROM debian:stretch
WORKDIR /root/


CMD ["/bin/true"]  