# 
# Docker environment for QSSLCAUDIT testing
# Uses standard OpenSSL libraries
#
# Prepare image: docker build -t debian-wheezy -f path/to/Dockerfile .
# Run instance:  docker run --name debian-wheezy --rm -it debian-wheezy
#

FROM debian:wheezy as stage1
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
FROM cdrx/fpm-ubuntu:18.04 as stage-package
RUN apt-get update && apt-get -y install rpm vim
COPY --from=stage1 /build /build
RUN VERSION_ID=$(grep -h ^VERSION_ID= /etc/*release | awk -F= {'print $2'} | sed 's/"//g') && \
ID=$(grep -h ^ID= /etc/*release | awk -F= {'print $2'} | sed 's/"//g') && \
mkdir /pkg && \
cd /pkg && \
fpm -t deb \
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
