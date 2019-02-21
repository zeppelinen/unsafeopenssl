# 
# Docker environment for QSSLCAUDIT testing
# Uses standard OpenSSL libraries
#
# Prepare image: docker build -t fedora-29 -f path/to/Dockerfile .
# Run instance:  docker run --name fedora-29 --rm -it fedora-29
#

FROM fedora:29 as stage1
# prebuild stage
RUN dnf -y update && \
dnf -y install make gcc perl zlib-devel zlib bzip2

# add files
ADD . /build
WORKDIR /build
# build stage
RUN ./build.sh
# postbuild stage
RUN echo post build

FROM fedora:29
WORKDIR /root/


CMD ["/bin/true"]  