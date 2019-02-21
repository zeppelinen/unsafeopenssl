#!/usr/bin/env bash
set -e
export BUILDROOT=/build/root
export OPENSSLDIR=/var/lib/unsafessl
mkdir -p ${BUILDROOT}

cd openssl-1.0.2i

arch=$(arch)
if [[ $arch == x86_64 ]]; then
    ADD_ARGS="linux-x86_64"
elif [[ $arch == i*86 ]]; then
    ADD_ARGS="$ADD_ARGS linux_elf 386"
elif  [[ $arch == arm* ]]; then
    linux-generic32
fi

if echo 'extern __uint128_t i;' |
   gcc -fno-strict-aliasing -Wa,--noexecstack -Werror -c -o/dev/null -xc -; then
        ADD_ARGS="enable-ec_nistp_64_gcc_128 $ADD_ARGS"
fi

./Configure shared \
        --prefix=/usr \
        --libdir=lib \
        --openssldir=/var/lib/unsafessl \
        --enginesdir=/usr/lib/openssl-unsafe/engines \
        --system-ciphers-file=/etc/openssl-unsafe/cipher-list.conf \
        enable-md2 \
        enable-rfc3779 \
        enable-ssl2 \
        zlib \
        enable-ssl2 enable-ssl3 enable-ssl3-method enable-weak-ssl-ciphers \
        $ADD_ARGS

# rename shared libraries
find . -name 'Makefile' -exec sed -i -e 's/libcrypto/libunsafecrypto/g' {} \;
find . -name 'Makefile' -exec sed -i -e 's/libssl/libunsafessl/g' {} \;
find . -name 'Makefile' -exec sed -i -e 's/openssl.pc/openssl-unsafe.pc/g' {} \;
find . -name 'Makefile' -exec sed -i -e 's/LIBNAME=$$i/LIBNAME=unsafe$$i/g' {} \;
find . -name 'Makefile' -exec sed -i -e 's/-l$$i/-lunsafe$$i/g' {} \;
find . -name 'Makefile' -exec sed -i -e 's/-lcrypto/-lunsafecrypto/g' {} \;
find . -name 'Makefile' -exec sed -i -e 's/-lssl/-lunsafessl/g' {} \;
find . -name 'shlib_wrap.sh' -exec sed -i -e 's/libcrypto.so/libunsafecrypto.so/g' {} \;
find . -name 'shlib_wrap.sh' -exec sed -i -e 's/libssl.so/libunsafessl.so/g' {} \;
find . -name 'Makefile' -exec sed -i -e 's/Name: OpenSSL-libcrypto/Name: OpenSSLUnsafe-libcrypto/g' {} \;
find . -name 'Makefile' -exec sed -i -e 's/Name: OpenSSL-libssl/Name: OpenSSLUnsafe-libssl/g' {} \;
find . -name 'Makefile' -exec sed -i -e 's/Name: OpenSSL/Name: OpenSSLUnsafe/g' {} \;

# SMP-incompatible build.
make

# Make soname symlinks.
/sbin/ldconfig -nv .

# Save library timestamps for later check.
touch -r libunsafecrypto.so.1.0.2i libunsafecrypto-stamp
touch -r libunsafessl.so.1.0.2i libunsafessl-stamp

LD_LIBRARY_PATH=`pwd` make rehash


echo Install stage

# The make_install macro doesn't work here.
make -j1 install \
        CC=../cc.sh \
        DESTDIR=$BUILDROOT \
	INSTALL_PREFIX=$BUILDROOT \
        MANDIR=/usr/share/man

# Fail if one of shared libraries was rebuit.
if [ libunsafecrypto.so.1.0.2i -nt libunsafecrypto-stamp -o \
     libunsafessl.so.1.0.2i -nt libunsafessl-stamp ]; then
        echo 'Shared library was rebuilt by "make install".'
        exit 1
fi

# Fail if the openssl binary is statically linked against OpenSSL at this
# stage (which could happen if "make install" caused anything to rebuild).
LD_LIBRARY_PATH=`pwd` ldd $BUILDROOT/usr/bin/openssl-unsafe |tee openssl.libs
grep -qw libunsafessl openssl.libs
grep -qw libunsafecrypto openssl.libs

# Relocate shared libraries from %_libdir/ to /lib/.
mkdir -p $BUILDROOT{/lib,/usr/lib/openssl-unsafe,/sbin}
for f in $BUILDROOT/usr/lib/*.so; do
        t=$(readlink "$f") || continue
        ln -snf ../../lib/"$t" "$f"
done
mv $BUILDROOT/usr/lib/*.so.* $BUILDROOT/lib/

# Relocate engines.
mv $BUILDROOT/usr/lib/engines $BUILDROOT/usr/lib/openssl-unsafe/

# Relocate openssl.cnf from %/etc/openssl/ to %_sysconfdir/openssl/.
mkdir -p $BUILDROOT/etc/openssl-unsafe
mv $BUILDROOT/$OPENSSLDIR/openssl.cnf $BUILDROOT/etc/openssl-unsafe/
cd  $BUILDROOT/etc/openssl-unsafe 
ln -s openssl.cnf ../../$OPENSSLDIR
cd -

#ln -s -r $BUILDROOT/usr/share/ca-certificates/ca-bundle.crt \
#        $BUILDROOT/etc/openssl/cert.pem

mv $BUILDROOT/$OPENSSLDIR/misc/CA{.sh,}
rm $BUILDROOT/$OPENSSLDIR/misc/CA.pl

mkdir -p $BUILDROOT%docdir
install -pm644 CHANGES* LICENSE NEWS README* engines/ccgost/README.gost \
        $BUILDROOT%docdir/
bzip2 -9 $BUILDROOT%docdir/CHANGES*
#cp -a demos doc $BUILDROOT%docdir/
rm -rf $BUILDROOT%docdir/doc/{apps,crypto,ssl}

# we do not need these binaries
rm -f $BUILDROOT/$OPENSSLDIR/misc/tsget
rm -f $BUILDROOT/usr/bin/c_rehash

# we do not need man pages
rm -rf $BUILDROOT/usr/share/man

# we do not need engines
rm -rf $BUILDROOT/usr/lib/openssl-unsafe/engines

# rename include directory
mv $BUILDROOT/usr/include/openssl{,-unsafe}

# fix include paths in the renamed include directory
find $BUILDROOT/usr/include/openssl-unsafe -name '*.h' -exec sed -i -e 's/<openssl\//<openssl-unsafe\//g' {} \;

# Create default cipher-list.conf from SSL_DEFAULT_CIPHER_LIST
sed -n -r 's,^#.*SSL_DEFAULT_CIPHER_LIST[[:space:]]+"([^"]+)",\1,p' \
        ssl/ssl.h > $BUILDROOT/etc//openssl-unsafe/cipher-list.conf
