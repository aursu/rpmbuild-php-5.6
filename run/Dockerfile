ARG image=7-base
FROM aursu/centos:${image}

COPY system/etc/yum.repos.d/bintray-custom.repo /etc/yum.repos.d/bintray-custom.repo

USER root
RUN yum -y --enablerepo=bintray-custom --enablerepo=bintray-php5custom install \
        php-bcmath \
        php-cli \
        php-fpm \
        php-opcache \
        php-pecl-apcu \
        php-pecl-geoip \
        php-pecl-imagick \
        php-pecl-memcached \
        php-pecl-redis \
        php-xml \
    && yum clean all && rm -rf /var/cache/yum /var/lib/rpm/__db*
