# 
# Docker environment for QSSLCAUDIT testing
# Uses standard OpenSSL libraries
#
# Prepare image: docker build -t centos-6 -f path/to/Dockerfile .
# Run instance:  docker run --name centos-6 --rm -it centos-6
#

FROM centos:6 as stage1
# prebuild stage
RUN yum -y update && \
yum -y install epel-release && \
yum -y install make glibc-devel gcc gcc-c++ zlib-devel zlib perl bzip2

# add files
ADD . /build
WORKDIR /build
# build stage
RUN find . -type f -print0 | xargs -0 sed -i -e "s/secure_getenv/getenv/g"
RUN ./build.sh
# postbuild stage
RUN echo post build

FROM centos:6
WORKDIR /root/


CMD ["/bin/true"]  