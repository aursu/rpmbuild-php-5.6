FROM rpmbuild:6-build

USER root
RUN yum -y install \
        bzip2-devel \
        cyrus-sasl-devel \
        db4-devel \
        freetds-devel \
        freetype-devel \
        gdbm-devel \
        libacl-devel \
        libc-client-devel \
        libcurl-devel \
        libicu-devel \
        libjpeg-turbo-devel \
        libmcrypt-devel \
        libpng-devel \
        libtool-ltdl-devel \
        libxml2-devel \
        libxslt-devel \
        mysql-devel \
        nginx-filesystem \
        openldap-devel \
        openssl-devel \
        pcre-devel \
        postgresql-devel \
        sendmail \
        sqlite-devel \
        systemtap-sdt-devel \
        unixODBC-devel \
        zlib-devel \
    && yum clean all && rm -rf /var/cache/yum

#RUN yum -y --enablerepo custom install \
#        libcurl-devel \
#        postgresql-devel \
#    && yum clean all && rm -rf /var/cache/yum

RUN yum -y --enablerepo custom install \
        "httpd-devel < 2.4" \
    && yum clean all && rm -rf /var/cache/yum

COPY SOURCES ${BUILD_TOPDIR}/SOURCES
COPY SPECS ${BUILD_TOPDIR}/SPECS

RUN chown -R $BUILD_USER ${BUILD_TOPDIR}/{SOURCES,SPECS}

USER $BUILD_USER
ENTRYPOINT ["/usr/bin/rpmbuild", "php.spec", "--with", "cgi", "--with", "fpm"]
CMD ["-ba"]
