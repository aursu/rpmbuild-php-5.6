#
# Interface versions exposed by PHP:
# 
%php_core_api @PHP_APIVER@
%php_zend_api @PHP_ZENDVER@
%php_pdo_api  @PHP_PDOVER@
%php_version  @PHP_VERSION@

%php_extdir    %{_libdir}/php5/modules

%php_inidir    %{_sysconfdir}/php5/php.d

%php_incldir    %{_includedir}/php5

%__php         %{_bindir}/php5
