# copy-pasted from https://packages.altlinux.org/en/Sisyphus/srpms/openssl10/spec

Name: openssl10-unsafe
Version: 1.0.2a
Release: alt2

Summary: OpenSSL - Secure Sockets Layer and cryptography shared libraries and tools, UNSAFE VERSION!
License: BSD-style
Group: System/Base
Url: http://www.openssl.org

Source: openssl-%version.tar
Source1: cc.sh

Patch03: openssl-alt-config.patch
Patch04: openssl-alt-fips_premain_dso.patch
Patch05: openssl-gosta-pkcs12-fix.patch
Patch06: openssl-rh-alt-soversion.patch
Patch07: openssl-rh-enginesdir.patch
Patch08: openssl-rh-no-rpath.patch
Patch09: openssl-rh-test-use-localhost.patch
Patch11: openssl-rh-pod2man-timezone.patch
Patch12: openssl-rh-perlpath.patch
Patch13: openssl-rh-default-paths.patch
Patch14: openssl-rh-issuer-hash.patch
Patch15: openssl-rh-X509_load_cert_file.patch
Patch16: openssl-rh-version-add-engines.patch
Patch18: openssl-rh-ipv6-apps.patch
Patch19: openssl-rh-env-zlib.patch
Patch21: openssl-rh-algo-doc.patch
Patch22: openssl-rh-apps-dgst.patch
Patch23: openssl-rh-xmpp-starttls.patch
Patch24: openssl-rh-chil-fixes.patch
Patch25: openssl-rh-alt-secure-getenv.patch
Patch27: openssl-rh-padlock64.patch
Patch84: openssl-rh-trusted-first-doc.patch
Patch87: openssl-rh-cc-reqs.patch
Patch90: openssl-rh-enc-fail.patch
Patch92: openssl-rh-system-cipherlist.patch

Patch100: openssl-unsafe-rename.patch

%define shlib_soversion 10
%define openssldir /var/lib/unsafessl

BuildRequires: /usr/bin/pod2man bc zlib-devel

%package -n libunsafecrypto%shlib_soversion
Summary: OpenSSL libcrypto shared library, UNSAFE VERSION!
Group: System/Libraries
Provides: libunsafecrypto = %version-%release
Requires: ca-certificates

%package -n libunsafessl%shlib_soversion
Summary: OpenSSL libssl shared library, UNSAFE VERSION!
Group: System/Libraries
Provides: libunsafessl = %version
Requires: libunsafecrypto%shlib_soversion = %version-%release

%package -n libunsafessl-devel
Summary: OpenSSL include files and development libraries, UNSAFE VERSION!
Group: Development/C
Provides: openssl-unsafe-devel = %version
Requires: libunsafessl%shlib_soversion = %version-%release

%package -n libunsafessl-devel-static
Summary: OpenSSL static libraries, UNSAFE VERSION!
Group: Development/C
Provides: openssl-unsafe-devel-static = %version
Requires: libunsafessl-devel = %version-%release

%package -n openssl-unsafe
Summary: OpenSSL tools, UNSAFE VERSION!
Group: System/Base
Provides: %openssldir
Requires: libunsafessl%shlib_soversion = %version-%release

%package -n openssl-unsafe-doc
Summary: OpenSSL documentation and demos, UNSAFE VERSION!
Group: Development/C
Requires: openssl-unsafe = %version-%release
BuildArch: noarch

%description
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

UNSAFE VERSION!

%description -n libunsafecrypto%shlib_soversion
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

This package contains the OpenSSL libcrypto shared library.

UNSAFE VERSION!

%description -n libunsafessl%shlib_soversion
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

This package contains the OpenSSL libssl shared library.

UNSAFE VERSION!

%description -n libunsafessl-devel
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

This package contains the OpenSSL include files and development libraries
required when building OpenSSL-based applications.

UNSAFE VERSION!

%description -n libunsafessl-devel-static
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

This package contains static libraries required when developing
OpenSSL-based statically linked applications.

UNSAFE VERSION!

%description -n openssl-unsafe
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

This package contains the base OpenSSL cryptography and SSL/TLS tools.

UNSAFE VERSION!

%description -n openssl-unsafe-doc
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

This package contains the OpenSSL cryptography and SSL/TLS extra
documentation and demos required when developing applications.

UNSAFE VERSION!

%prep
%setup -n openssl-%version
%patch03 -p1
%patch04 -p1
%patch05 -p1
%patch06 -p1
%patch07 -p1
%patch08 -p1
%patch09 -p1

%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch18 -p1
%patch19 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1

%patch24 -p1

%patch25 -p1
%patch27 -p1
%patch84 -p1
%patch87 -p1
%patch90 -p1
%patch92 -p1

%patch100 -p1

find -type f -name \*.orig -delete

# Correct shared library name.
sed -i 's/@SHLIB_SOVERSION@/%shlib_soversion/g' Configure Makefile.*
sed -i 's/\\\$(SHLIB_MAJOR)\.\\\$(SHLIB_MINOR)/\\$(VERSION)/g' Configure
sed -i 's/\$(SHLIB_MAJOR)\.\$(SHLIB_MINOR)/\$(VERSION)/g' Makefile.org
sed -i 's/\(^#define[[:space:]]\+SHLIB_VERSION_NUMBER[[:space:]]\+\).*/\1"%version"/' crypto/opensslv.h

# Correct compilation options.
%add_optflags -fno-strict-aliasing -Wa,--noexecstack
sed -i 's/-O\([0-9s]\>\)\?\( -fomit-frame-pointer\)\?\( -m.86\)\?/\\\$(RPM_OPT_FLAGS)/' \
	Configure

# Be more verbose.
sed -i 's/^\([[:space:]]\+\)@[[:space:]]*/\1/' Makefile*

%build

%set_gcc_version 5
%set_verify_elf_method skip

ADD_ARGS=%_os-%_arch
%ifarch %ix86
	ADD_ARGS=linux-elf
%ifarch i386
	ADD_ARGS="$ADD_ARGS 386"
%endif
%endif
%ifarch %arm
ADD_ARGS=linux-generic32
%endif
%ifarch x32
ADD_ARGS=linux-x32
%endif

if echo 'extern __uint128_t i;' |
   gcc %optflags -Werror -c -o/dev/null -xc -; then
	ADD_ARGS="enable-ec_nistp_64_gcc_128 $ADD_ARGS"
fi

./Configure shared \
	--prefix=%prefix \
	--libdir=%_lib \
	--openssldir=%openssldir \
	--enginesdir=%_libdir/openssl-unsafe/engines \
	--system-ciphers-file=%_sysconfdir/openssl-unsafe/cipher-list.conf \
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
touch -r libunsafecrypto.so.%version libunsafecrypto-stamp
touch -r libunsafessl.so.%version libunsafessl-stamp

LD_LIBRARY_PATH=`pwd` make rehash

%install
# The make_install macro doesn't work here.
make install \
	CC=%_sourcedir/cc.sh \
	INSTALL_PREFIX=%buildroot \
	MANDIR=%_mandir

# Fail if one of shared libraries was rebuit.
if [ libunsafecrypto.so.%version -nt libunsafecrypto-stamp -o \
     libunsafessl.so.%version -nt libunsafessl-stamp ]; then
	echo 'Shared library was rebuilt by "make install".'
	exit 1
fi

# Fail if the openssl binary is statically linked against OpenSSL at this
# stage (which could happen if "make install" caused anything to rebuild).
LD_LIBRARY_PATH=`pwd` ldd %buildroot%_bindir/openssl-unsafe |tee openssl.libs
grep -qw libunsafessl openssl.libs
grep -qw libunsafecrypto openssl.libs

# Relocate shared libraries from %_libdir/ to /lib/.
mkdir -p %buildroot{/%_lib,%_libdir/openssl-unsafe,%_sbindir}
for f in %buildroot%_libdir/*.so; do
	t=$(readlink "$f") || continue
	ln -snf ../../%_lib/"$t" "$f"
done
mv %buildroot%_libdir/*.so.* %buildroot/%_lib/

# Relocate engines.
mv %buildroot%_libdir/engines %buildroot%_libdir/openssl-unsafe/

# Relocate openssl.cnf from %%openssldir/ to %_sysconfdir/openssl/.
mkdir -p %buildroot%_sysconfdir/openssl-unsafe
mv %buildroot%openssldir/openssl.cnf %buildroot%_sysconfdir/openssl-unsafe/
ln -s -r %buildroot%_sysconfdir/openssl-unsafe/openssl.cnf %buildroot%openssldir/

ln -s -r %buildroot%_datadir/ca-certificates/ca-bundle.crt \
	%buildroot%openssldir/cert.pem

mv %buildroot%openssldir/misc/CA{.sh,}
rm %buildroot%openssldir/misc/CA.pl

%define docdir %_docdir/openssl-unsafe-%version
mkdir -p %buildroot%docdir
install -pm644 CHANGES* LICENSE NEWS README* engines/ccgost/README.gost \
	%buildroot%docdir/
bzip2 -9 %buildroot%docdir/CHANGES*
#cp -a demos doc %buildroot%docdir/
rm -rf %buildroot%docdir/doc/{apps,crypto,ssl}

# we do not need these binaries
rm -f %buildroot%openssldir/misc/tsget
rm -f %buildroot%_bindir/c_rehash

# we do not need man pages
rm -rf %buildroot%_mandir

# we do not need engines
rm -rf %buildroot%_libdir/openssl-unsafe/engines

# rename include directory
mv %buildroot%_includedir/openssl{,-unsafe}

# fix include paths in the renamed include directory
find %buildroot%_includedir/openssl-unsafe -name '*.h' -exec sed -i -e 's/<openssl\//<openssl-unsafe\//g' {} \;

# Create default cipher-list.conf from SSL_DEFAULT_CIPHER_LIST
sed -n -r 's,^#.*SSL_DEFAULT_CIPHER_LIST[[:space:]]+"([^"]+)",\1,p' \
	ssl/ssl.h > %buildroot%_sysconfdir/openssl-unsafe/cipher-list.conf

%files -n libunsafecrypto%shlib_soversion
/%_lib/libunsafecrypto*
%config(noreplace) %_sysconfdir/openssl-unsafe/openssl.cnf
%dir %_sysconfdir/openssl-unsafe/
%dir %openssldir
%openssldir/*.cnf
%openssldir/*.pem
%dir %docdir
%docdir/[A-Z]*

%files -n libunsafessl%shlib_soversion
%config(noreplace) %_sysconfdir/openssl-unsafe/cipher-list.conf
%dir %_sysconfdir/openssl-unsafe/
/%_lib/libunsafessl*

%files -n libunsafessl-devel
%_libdir/*.so
%_libdir/pkgconfig/*
%_includedir/*

%files -n libunsafessl-devel-static
%_libdir/*.a

%files -n openssl-unsafe
%_bindir/*
%dir %openssldir
%openssldir/misc
%openssldir/certs
%dir %attr(700,root,root) %openssldir/private

%changelog
* Thu Dec 20 2018 Pavel Nakonechnyi <pavel@gremwell.com> 1.0.2i-alt2
- packages and libraries renamed, files moved to follow FHS

* Mon May 14 2018 Pavel Nakonechnyi <pavel@gremwell.com> 1.0.2i-alt1
- Initial build based on 1.0.2i
