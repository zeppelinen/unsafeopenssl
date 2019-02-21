# 
# Docker environment for QSSLCAUDIT testing
# Uses standard OpenSSL libraries
#
# Prepare image: docker build -t mint-17 -f path/to/Dockerfile .
# Run instance:  docker run --name mint-17 --rm -it mint-17
#

FROM vcatechnology/linux-mint:17 as stage1
# prebuild stage
RUN apt-get update && apt-get -y install make gcc zlib1g-dev zlib1g bzip2 perl
# add files
ADD . /build
WORKDIR /build
# build stage
RUN ./build.sh
# postbuild stage
RUN echo post build

FROM vcatechnology/linux-mint:17
WORKDIR /root/


CMD ["/bin/true"]  