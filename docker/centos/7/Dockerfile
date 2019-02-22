# 
# Docker environment for QSSLCAUDIT testing
# Uses standard OpenSSL libraries
#
# Prepare image: docker build -t centos-7 -f path/to/Dockerfile .
# Run instance:  docker run --name centos-7 --rm -it centos-7
#

FROM centos:7 as stage1
# prebuild stage
RUN yum -y update && \
yum -y install epel-release && \
yum -y install make glibc-devel gcc gcc-c++ zlib-devel zlib perl bzip2

# add files
ADD . /build
WORKDIR /build
# build stage
RUN ./build.sh
# postbuild stage
FROM cdrx/fpm-ubuntu:18.04 as stage-package
RUN apt-get update && apt-get -y install rpm vim
COPY --from=stage1 /build /build
RUN VERSION_ID=$(grep -h ^VERSION_ID= /etc/*release | awk -F= {'print $2'} | sed 's/"//g') && \
ID=$(grep -h ^ID= /etc/*release | awk -F= {'print $2'} | sed 's/"//g') && \
mkdir /pkg && \
cd /pkg && \
fpm -t rpm \
-n unsafeopenssl \
-v 0.1 \
-m "<an@zeppelinen.com>" \
--provides "unsafeopenssl" \
--description "Unsafe version of OpenSSL 1.0.2i.\nDependency for qsslcaudit tool." \
--url "https://github.com" \
--iteration "${ID}.${VERSION_ID}" \
-C /build/root \
-s dir ./


CMD ["/bin/true"]  
