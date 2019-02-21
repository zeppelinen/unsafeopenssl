# 
# Docker environment for QSSLCAUDIT testing
# Uses standard OpenSSL libraries
#
# Prepare image: docker build -t ubuntu-precise -f path/to/Dockerfile .
# Run instance:  docker run --name ubuntu-precise --rm -it ubuntu-precise
#

FROM ubuntu:precise as stage1
# prebuild stage
RUN echo 'deb http://http.debian.net/debian wheezy-backports main' > /etc/apt/sources.list.d/wheezy-backports.list
RUN apt-get update && apt-get -y install make gcc zlib1g zlib1g-dev bzip2 perl
# add files
ADD . /build
WORKDIR /build
# build stage
RUN find . -type f -print0 | xargs -0 sed -i -e "s/secure_getenv/getenv/g"
RUN ./build.sh
# postbuild stage
RUN echo post build

FROM ubuntu:precise
WORKDIR /root/


CMD ["/bin/true"]  