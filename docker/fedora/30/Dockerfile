# 
# Docker environment for QSSLCAUDIT testing
# Uses standard OpenSSL libraries
#
# Prepare image: docker build -t fedora-30 -f path/to/Dockerfile .
# Run instance:  docker run --name fedora-30 --rm -it fedora-30
#

FROM fedora:30 as stage1
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

FROM fedora:30
WORKDIR /root/


CMD ["/bin/true"]  