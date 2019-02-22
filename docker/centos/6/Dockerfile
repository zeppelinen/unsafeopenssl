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
yum -y install make glibc-devel gcc gcc-c++ zlib-devel zlib perl bzip2 redhat-lsb


# add files
ADD . /build
WORKDIR /build

# build stage
RUN find . -type f -print0 | xargs -0 sed -i -e "s/secure_getenv/getenv/g"
RUN ./build.sh && \
echo Store distro for packager && \
lsb_release -i | awk {'print $3'} > /build/distro && \
echo Store distro version for packager && \
lsb_release -r | awk {'print $2'} | sed -e 's/n\/a/unstable/g' > /build/distro_version && \
echo /build && \
ls -al /build && \
echo build root contents && \
find /build/root



# postbuild stage
FROM cdrx/fpm-ubuntu:18.04 as stage-package
RUN apt-get update && apt-get -y install rpm vim
COPY --from=stage1 /build /build
RUN mkdir /pkg && \
DISTRO=$(cat /build/distro) && \
DISTRO_VERSION=$(cat /build/distro_version) && \
cd /pkg && \
fpm -t rpm \
-n unsafeopenssl \
-v 0.1 \
-m "<an@zeppelinen.com>" \
--provides "unsafeopenssl" \
--description "Unsafe version of OpenSSL 1.0.2i.\nDependency for qsslcaudit tool." \
--url "https://github.com" \
--iteration "${DISTRO}.${DISTRO_VERSION}" \
-a "x86_64" \
-C /build/root \
-s dir ./


CMD ["/bin/true"]  
