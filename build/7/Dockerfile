FROM aursu/rpmbuild:7-build

USER root
RUN yum -y install --enablerepo custom \
        "php-cli < 7" \
        "php-common < 7" \
        "php-devel < 7" \
        "php-process < 7" \
        "php-xml < 7" \
    && yum clean all && rm -rf /var/cache/yum
