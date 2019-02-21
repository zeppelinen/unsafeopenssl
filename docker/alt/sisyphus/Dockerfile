# 
# Docker environment for QSSLCAUDIT testing
# Uses standard OpenSSL libraries
#
# Prepare image: docker build -t alt-sisyphus -f path/to/Dockerfile .
# Run instance:  docker run --name alt-sisyphus --rm -it alt-sisyphus
#

FROM alt:sisyphus as stage1
# prebuild stage
RUN apt-get update && apt-get -y install make gcc zlib-devel zlib
# add files
ADD . /build
WORKDIR /build
# build stage
RUN ./build.sh
# postbuild stage
RUN echo post build

FROM alt:sisyphus
WORKDIR /root/


CMD ["/bin/true"]  