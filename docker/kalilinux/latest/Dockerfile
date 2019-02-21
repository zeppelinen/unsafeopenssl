# 
# Docker environment for QSSLCAUDIT testing
# Uses standard OpenSSL libraries
#
# Prepare image: docker build -t kalilinux-latest -f path/to/Dockerfile .
# Run instance:  docker run --name kalilinux-latest --rm -it kalilinux-latest
#

FROM kalilinux/kali-linux-docker:latest as stage1
# prebuild stage
RUN apt-get update && apt-get -y install make gcc zlib1g zlib1g-dev bzip2 perl perl-base
# add files
ADD . /build
WORKDIR /build
# build stage
RUN ./build.sh
# postbuild stage
RUN echo post build

FROM kalilinux/kali-linux-docker:latest
WORKDIR /root/


CMD ["/bin/true"]  