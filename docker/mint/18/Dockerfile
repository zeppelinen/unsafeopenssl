# 
# Docker environment for QSSLCAUDIT testing
# Uses standard OpenSSL libraries
#
# Prepare image: docker build -t mint-18 -f path/to/Dockerfile .
# Run instance:  docker run --name mint-18 --rm -it mint-18
#

FROM vcatechnology/linux-mint:18 as stage1
# prebuild stage
RUN apt-get update && apt-get -y install make gcc zlib1g-dev zlib1g bzip2 perl
# add files
ADD . /build
WORKDIR /build
# build stage
RUN ./build.sh
# postbuild stage
RUN echo post build

FROM vcatechnology/linux-mint:18
WORKDIR /root/


CMD ["/bin/true"]  