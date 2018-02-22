# Fedora spec file for php
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
# API/ABI check

# Building of CGI SAPI is disabled by default. Use --with cgi to enable it
# tests are disabled by default. Use --with test to enable them

# https://github.com/rpm-software-management/rpm/blob/master/doc/manual/conditionalbuilds
# php-cgi SAPI
%global with_cgi 0%{?_with_cgi:1}
%global with_test 0%{?_with_test:1}
%global with_ap24 0%{?_with_ap24:1}
%global with_relocation 0%{?_with_relocation:1}

# with this flag set on we will build php-mysqlnd
%global with_mysqlnd 0%{?_with_mysqlnd:1}

%global with_fpm 0%{?_with_fpm:1}

# _rundir is defined in RHEL/CentOS 7
%if 0%{?rhel} < 7
%global _rundir     /var/run
%endif

%if %{with_relocation}
%global program_suffix      5
%global main_name           php5
%global fpm_name            php5-fpm
%global php_sysconfdir      %{_sysconfdir}/php5
%global php_datadir         %{_datadir}/php5
%global pear_datadir        %{php_datadir}/pear
%global php_docdir          %{_docdir}/php5
%global tests_datadir       %{php_datadir}/tests
# configured by relocation patch (in other words - hardcoded)
%global fpm_config_name     php5-fpm.conf
%global fpm_config_d        %{php_sysconfdir}/php%{program_suffix}-fpm.d
%global bin_phar            phar%{program_suffix}
%global bin_cli             php%{program_suffix}
%global bin_cgi             php%{program_suffix}-cgi
%global bin_phpize          phpize%{program_suffix}
%global bin_phpdbg          phpdbg%{program_suffix}
%global bin_fpm             php%{program_suffix}-fpm
%global bin_php_config      php%{program_suffix}-config
%global fpm_datadir         %{_datadir}/php%{program_suffix}-fpm
%global php_includedir      %{_includedir}/php5
%else
%global main_name           php
%global fpm_name            php-fpm
%global php_sysconfdir      %{_sysconfdir}
%global php_datadir         %{_datadir}/php
%global pear_datadir        %{_datadir}/pear
%global php_docdir          %{_docdir}
%global tests_datadir       %{_datadir}/tests
%global fpm_config_name     php-fpm.conf
%global fpm_config_d        %{php_sysconfdir}/php-fpm.d
%global bin_phar            phar
%global bin_cli             php
%global bin_cgi             php-cgi
%global bin_phpize          phpize
%global bin_phpdbg          phpdbg
%global bin_fpm             php-fpm
%global bin_php_config      php-config
%global fpm_datadir         %{_datadir}/fpm
%global php_includedir      %{_includedir}/php
%endif

%global php_main            %{main_name}
%global php_common          %{php_main}-common
%global php_cli             %{php_main}-cli
%global php_cgi             %{php_main}-cgi
%global php_xml             %{php_main}-xml
%global php_opcache         %{php_main}-opcache
%global php_bcmath          %{php_main}-bcmath
%global php_mysql           %{php_main}-mysql
%global php_mysqlnd         %{php_main}-mysqlnd
%global php_libdir          %{_libdir}/%{main_name}
%global fpm_rundir          %{_rundir}/%{fpm_name}
%global php_sharedstatedir  %{_sharedstatedir}/%{main_name}
%global fpm_sharedstatedir  %{_sharedstatedir}/%{fpm_name}
%global fpm_logdir          %{_localstatedir}/log/%{fpm_name}
%global fpm_config          %{php_sysconfdir}/%{fpm_config_name}
%global fpm_service         %{fpm_name}
%global fpm_tmpfiles_d      %{fpm_service}.conf
%global fpm_service_d       %{fpm_service}.service.d
%global fpm_unit            %{fpm_service}.service
%global fpm_logrotate       %{fpm_service}

# API/ABI check
%global apiver      20131106
%global zendver     20131226
%global pdover      20080721
# Extension version
%global opcachever  7.0.6-dev
%global jsonver     1.2.1


# Adds -z now to the linker flags
%global _hardened_build 1

# Use the arch-specific mysql_config binary to avoid mismatch with the
# arch detection heuristic used by bindir/mysql_config.
%if 0%{?fedora}
%global mysql_config %{_bindir}/mysql_config
%else
%global mysql_config %{_libdir}/mysql/mysql_config
%endif
%global mysql_sock %(mysql_config --socket 2>/dev/null || echo /var/lib/mysql/mysql.sock)

%if 0%{?fedora}
%global isasuffix -%{__isa_bits}
%else
%if 0%{?__isa:1}
%global isasuffix -%{__isa}
%else
%global isasuffix %nil
%endif
%endif

%global  _nginx_home    %{_localstatedir}/lib/nginx
# needed at srpm build time, when httpd-devel not yet installed
%{!?_httpd_mmn:         %{expand: %%global _httpd_mmn        %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}}

%global with_dtrace 1
%global with_zip    1
%global with_libzip 0

%if 0%{?fedora} < 18 && 0%{?rhel} < 7
%global db_devel  db4-devel
%else
%global db_devel  libdb-devel
%endif

%global rpmrel 1

%if %{with_ap24}
%global aptag .ap24
%endif

Summary: PHP scripting language for creating dynamic web sites
Name: %{php_main}
Version: 5.6.33
Release: %{rpmrel}%{?aptag}%{?dist}

# All files licensed under PHP version 3.01, except
# fileinfo is licensed under PHP version 3.0
# regex, libmagic, onigurama are licensed under BSD
# main/snprintf.c, main/spprintf.c and main/rfc1867.c are ASL 1.0
# libmbfl is licensed under LGPLv2
# ucgendat is licensed under OpenLDAP
License: PHP and BSD and ASL 1.0 and LGPLv2 and OpenLDAP
Group: Development/Languages
URL: http://www.php.net/

Source0: http://www.php.net/distributions/php-%{version}.tar.xz
Source1: php.conf
Source2: php.ini
Source3: macros.php
Source4: php-fpm.conf
Source5: php-fpm-www.conf
Source6: php-fpm.service
Source7: php-fpm.logrotate
Source9: php.modconf
Source10: php-fpm.init
Source13: nginx-fpm.conf
Source14: nginx-php.conf
Source15: php-cgi-fcgi.ini
Source16: https://downloads.ioncube.com/loader_downloads/ioncube_loaders_lin_x86-64.tar.gz
# zend loader discontinued starting from PHP 7
Source17: http://downloads.zend.com/guard/7.0.0/zend-loader-php5.6-linux-x86_64_update1.tar.gz
Source18: php-5.3.29-sqlite.tar.gz
# Configuration files for some extensions
Source50: opcache.ini
Source51: opcache-default.blacklist
Source53: mysql.ini
Source54: mysqli.ini

# relocation resources
Source101: php5-php.conf
Source103: php5-macros.php
Source104: php5-php-fpm.conf
Source105: php5-php-fpm-www.conf
Source106: php5-php-fpm.service
Source107: php5-php-fpm.logrotate
Source110: php5-php-fpm.init
Source113: php5-nginx-fpm.conf
Source114: php5-nginx-php.conf
Source115: php5-php-cgi-fcgi.ini
Source150: php5-opcache.ini

# Build fixes
Patch5: php-5.6.3-includedir.patch
Patch8: php-5.6.17-libdb.patch

# Functional changes
Patch40: php-5.4.0-dlopen.patch
Patch42: php-5.6.13-systzdata-v12.patch
# See http://bugs.php.net/53436
Patch43: php-5.4.0-phpize.patch
# Make php_config.h constant across builds
Patch46: php-5.6.3-fixheader.patch
# drop "Configure command" from phpinfo output
Patch47: php-5.6.3-phpinfo.patch
Patch49: php-5.6.31-no-scan-dir-override.patch

# Upstream fixes (100+)

# Security fixes (200+)

# Fixes for tests (300+)
# Factory is droped from system tzdata
Patch300: php-5.6.3-datetests.patch

# relocation (400+)
Patch405: php5-php-5.6.3-includedir.patch
Patch409: php-5.6.31-relocation.patch

# additional logging
Patch91: php-5.6.31-log-syserr.patch
Patch92: php-5.6.31-eval-warn.patch
Patch93: php-5.6.31-eval-warn-syserr.patch
Patch94: php-5.6.31-logging.patch
Patch96: php-5.6.31-logging-syserr.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# No interactive mode for CLI/CGI - disable libedit
BuildRequires: autoconf
BuildRequires: bison
BuildRequires: bzip2-devel
BuildRequires: curl-devel >= 7.29
BuildRequires: %{db_devel}
BuildRequires: flex
BuildRequires: freetds-devel
BuildRequires: freetype-devel
BuildRequires: gcc-c++
BuildRequires: gdbm-devel
%if %{with_ap24}
BuildRequires: httpd-devel >= 2.4
%else
BuildRequires: httpd-devel >= 2.2
BuildRequires: httpd-devel < 2.4
%endif
BuildRequires: libc-client-devel
BuildRequires: libicu-devel
BuildRequires: libjpeg-devel
BuildRequires: libmcrypt-devel
BuildRequires: libpng-devel
BuildRequires: libstdc++-devel
BuildRequires: libtool >= 1.4.3
BuildRequires: libtool-ltdl-devel
BuildRequires: libxml2-devel
%if %{with_libzip}
BuildRequires: libzip-devel >= 0.11
%endif
BuildRequires: openssl-devel
BuildRequires: pcre-devel >= 6.6
BuildRequires: perl
BuildRequires: smtpdaemon
BuildRequires: sqlite-devel >= 3.6.0
BuildRequires: unixODBC-devel
BuildRequires: zlib-devel
# to ensure we are using httpd with filesystem feature (see #1081453)
#BuildRequires: httpd-filesystem
%if %{with_fpm}
# to ensure we are using nginx with filesystem feature (see #1142298)
BuildRequires: nginx-filesystem
%endif
%if %{with_dtrace}
BuildRequires: systemtap-sdt-devel
%endif

Requires: httpd-mmn = %{_httpd_mmn}
%if %{with_ap24}
Requires: httpd-filesystem >= 2.4
%endif
Requires: %{php_common}%{?_isa} = %{version}-%{release}

# To ensure correct /var/lib/php/session ownership:
Requires(pre): httpd >= 2.2.26

# Don't provides extensions, which are not shared library, as .so
# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_libdir}/modules/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_libdir}/modules/.*\\.so$

# php engine for Apache httpd webserver
Provides: php(httpd)
Provides: mod_php = %{version}-%{release}

%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated web pages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts.

The php package contains the module (often referred to as mod_php)
which adds support for the PHP language to Apache HTTP Server.

%package common
Group: Development/Languages
Summary: Common files for PHP
# All files licensed under PHP version 3.01, except
# fileinfo is licensed under PHP version 3.0
# libmagic, onigurama are licensed under BSD
License: PHP and BSD
# New ABI/API check - Arch specific
Provides: php-api = %{apiver}, php-api = %{apiver}%{isasuffix}
Provides: php(api) = %{apiver}, php(api) = %{apiver}%{isasuffix}
Provides: php-zend-abi = %{zendver}, php-zend-abi = %{zendver}%{isasuffix}
Provides: php(zend-abi) = %{zendver}, php(zend-abi) = %{zendver}%{isasuffix}
Provides: php(language) = %{version}, php(language)%{?_isa} = %{version}
# Provides for all builtin/shared modules:
# Bzip2 support in PHP is not enabled by default. You will need to use the --with-bz2
Provides: php-bz2, php-bz2%{?_isa}
# To get these functions to work, you have to compile PHP with --enable-calendar
Provides: php-calendar, php-calendar%{?_isa}
Provides: php-core = %{version}, php-core%{?_isa} = %{version}
# Beginning with PHP 4.2.0 these functions are enabled by default
Provides: php-ctype, php-ctype%{?_isa}
# To use PHP's cURL support you must also compile PHP --with-curl
Provides: php-curl, php-curl%{?_isa}
Provides: php_database
# part of the PHP core
Provides: php-date, php-date%{?_isa}
# using the --enable-dba configuration option you can enable PHP for basic support of dbm-style databases
# To enable support for gdbm add --with-gdbm
# To enable support for Oracle Berkeley DB 4 or 5 add --with-db4
Provides: php-dba, php-dba%{?_isa}
# To enable regexp support configure PHP --with-regex
# DEPRECATED in PHP 5.3.0, and REMOVED in PHP 7.0.0
Provides: php-ereg, php-ereg%{?_isa}
# To enable exif-support configure PHP with --enable-exif
Provides: php-exif, php-exif%{?_isa}
# This extension is enabled by default as of PHP 5.3.0
Provides: php-fileinfo, php-fileinfo%{?_isa}
# the filter extension is enabled by default as of PHP 5.2.0
Provides: php-filter, php-filter%{?_isa}
# to use FTP functions with your PHP configuration, you should add the --enable-ftp
Provides: php-ftp, php-ftp%{?_isa}
# To enable GD-support configure PHP --with-gd
Provides: php-gd, php-gd%{?_isa}
# To include GNU gettext support in your PHP build you must add the option --with-gettext
Provides: php-gettext, php-gettext%{?_isa}
# As of PHP 5.1.2, the Hash extension is bundled and compiled into PHP by default
Provides: php-hash, php-hash%{?_isa}
# This extension is enabled by default
Provides: php-iconv, php-iconv%{?_isa}
# To get these functions to work, you have to compile PHP with --with-imap
Provides: php-imap, php-imap%{?_isa}
# extension may be installed using the bundled version as of PHP 5.3.0, --enable-intl will enable the bundled version
Provides: php-intl, php-intl%{?_isa}
# As of PHP 5.2.0, the JSON extension is bundled and compiled into PHP by default
Provides: php-json, php-json%{?_isa}
%if %{with_relocation}
Provides: %{php_main}-json, %{php_main}-json%{?_isa}
%endif
# The libxml extension is enabled by default
Provides: php-libxml, php-libxml%{?_isa}
# mbstring is a non-default extension. --enable-mbstring : Enable mbstring functions
Provides: php-mbstring, php-mbstring%{?_isa}
# You need to compile PHP with the --with-mcrypt[=DIR] parameter to enable this extension
Provides: php-mcrypt, php-mcrypt%{?_isa}
# To use PHP's OpenSSL support you must also compile PHP --with-openssl
Provides: php-openssl, php-openssl%{?_isa}
# core PHP extension, so it is always enabled
Provides: php-pcre, php-pcre%{?_isa}
Provides: php-pdo, php-pdo%{?_isa}
Provides: php-pdo-abi  = %{pdover}
Provides: php(pdo-abi) = %{pdover}
Provides: php-pdo-abi  = %{pdover}%{isasuffix}
Provides: php(pdo-abi) = %{pdover}%{isasuffix}
# PDO and the PDO_SQLITE driver is enabled by default as of PHP 5.1.0
Provides: php-pdo_sqlite, php-pdo_sqlite%{?_isa}
Provides: php-pecl-json          = %{jsonver}
Provides: php-pecl(json)         = %{jsonver}
Provides: php-pecl-json%{?_isa}  = %{jsonver}
Provides: php-pecl(json)%{?_isa} = %{jsonver}
# The Phar extension is built into PHP as of PHP version 5.3.0
Provides: php-phar, php-phar%{?_isa}
# they are part of the PHP core
Provides: php-reflection, php-reflection%{?_isa}
# Session support is enabled in PHP by default
Provides: php-session, php-session%{?_isa}
# enable SOAP support, configure PHP with --enable-soap
Provides: php-soap, php-soap%{?_isa}
# enabled at compile time by giving the --enable-sockets
Provides: php-sockets, php-sockets%{?_isa}
# As of PHP 5.3.0 this extension can no longer be disabled and is therefore always available
Provides: php-spl, php-spl%{?_isa}
# The SQLite3 extension is enabled by default as of PHP 5.3.0
Provides: php-sqlite3, php-sqlite3%{?_isa}
Provides: php-standard = %{version}, php-standard%{?_isa} = %{version}
# these functions are enabled by default
Provides: php-tokenizer, php-tokenizer%{?_isa}
# XML-RPC support in PHP is not enabled by default. You will need to use the --with-xmlrpc
Provides: php-xmlrpc, php-xmlrpc%{?_isa}
%if %{with_zip}
# compile PHP with zip support by using the --enable-zip
Provides: php-zip, php-zip%{?_isa}
%endif
# Zlib support in PHP is not enabled by default. You will need to configure PHP --with-zlib
Provides: php-zlib, php-zlib%{?_isa}

%description common
The %{php_common} package contains files used by both the php
package and the %{php_cli} package.

%package cli
Group: Development/Languages
Summary: Command-line interface for PHP
Requires: %{php_common}%{?_isa} = %{version}-%{release}
# No interactive mode for CLI/CGI (disabled libedit, readline)

%description cli
The php-cli package contains the command-line interface
executing PHP scripts, /usr/bin/php.

%if %{with_cgi}
%package cgi
Group: Development/Languages
Summary: CGI interface for PHP
# for monolithic config use we need ensure that all extensions are installed
Requires: %{php_common}%{?_isa} = %{version}-%{release}

%description cgi
The php-cgi package contains the CGI interface executing
PHP scripts, /usr/bin/php-cgi

%package ioncube
Summary: ionCube extension for PHP
Group: Development/Languages
Requires: %{php_common}%{?_isa} = %{version}-%{release}

%description ioncube
ionCube Loader extensions for PHP. The ionCube
Loader is loaded as a PHP engine extension. This extension
transparently detects and loads encoded files.

%package zend-guard-loader
Summary: Zend Guard Loader runtime
Group: Development/Languages
Requires: %{php_common}%{?_isa} = %{version}-%{release}

%description zend-guard-loader
Zend Guard Loader is a free runtime application that enables PHP to run the
scripts encoded by Zend Guard. It can be used freely by anyone looking to run
encoded applications.
%endif

%if %{with_fpm}
%package fpm
Group: Development/Languages
Summary: PHP FastCGI Process Manager
Requires: %{php_common}%{?_isa} = %{version}-%{release}
Requires(pre): /usr/sbin/useradd
BuildRequires: libacl-devel
%if 0%{?rhel} >= 7
BuildRequires: systemd-units
BuildRequires: systemd-devel
Requires: systemd-units
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%endif
# for /etc/nginx ownership
Requires(pre): nginx-filesystem
Requires: nginx-filesystem

%description fpm
PHP-FPM (FastCGI Process Manager) is an alternative PHP FastCGI
implementation with some additional features useful for sites of
any size, especially busier sites.
%endif

%package devel
Group: Development/Libraries
Summary: Files needed for building PHP extensions
Requires: %{php_cli}%{?_isa} = %{version}-%{release}
Requires: autoconf, automake
Requires: pcre-devel%{?_isa}

%description devel
The php-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.

%package opcache
Summary:   The Zend OPcache
Group:     Development/Languages
License:   PHP
Requires: %{php_common}%{?_isa} = %{version}-%{release}
Obsoletes: php-pecl-zendopcache
Provides:  php-pecl-zendopcache = %{opcachever}
Provides:  php-pecl-zendopcache%{?_isa} = %{opcachever}
Provides:  php-pecl(opcache) = %{opcachever}
Provides:  php-pecl(opcache)%{?_isa} = %{opcachever}

%description opcache
The Zend OPcache provides faster PHP execution through opcode caching and
optimization. It improves PHP performance by storing precompiled script
bytecode in the shared memory. This eliminates the stages of reading code from
the disk and compiling it on future access. In addition, it applies a few
bytecode optimization patterns that make code execution faster.

%package xml
Summary: A module for PHP applications which use XML
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{php_common}%{?_isa} = %{version}-%{release}
# This extension is enabled by default
Provides: php-dom, php-dom%{?_isa}
Provides: php-domxml, php-domxml%{?_isa}
# This extension is enabled by default.
Provides: php-simplexml, php-simplexml%{?_isa}
# compile PHP with --enable-wddx
Provides: php-wddx, php-wddx%{?_isa}
# enabled by default as of PHP 5.1.2
Provides: php-xmlreader, php-xmlreader%{?_isa}
# This extension is enabled by default.
Provides: php-xmlwriter, php-xmlwriter%{?_isa}
# PHP 5 includes the XSL extension by default and can be enabled by adding the argument --with-xsl
Provides: php-xsl, php-xsl%{?_isa}
BuildRequires: libxslt-devel, libxml2-devel
Requires: libxslt

%description xml
The php-xml package contains dynamic shared objects which add support
to PHP for manipulating XML documents using the DOM tree,
and performing XSL transformations on XML documents.

%package pgsql
Summary: A PostgreSQL database module for PHP
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
BuildRequires: postgresql-devel
Requires: %{php_common}%{?_isa} = %{version}-%{release}
Requires: postgresql-libs

%description pgsql
The php-pgsql package add PostgreSQL database support to PHP.
PostgreSQL is an object-relational database management
system that supports almost all SQL constructs. PHP is an
HTML-embedded scripting language. If you need back-end support for
PostgreSQL, you should install this package in addition to the main
php package.

%package odbc
Summary: A module for PHP applications that use ODBC databases
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# pdo_odbc is licensed under PHP version 3.0
License: PHP
Requires: %{php_common}%{?_isa} = %{version}-%{release}
BuildRequires: unixODBC-devel

%description odbc
The php-odbc package contains a dynamic shared object that will add
database support through ODBC to PHP. ODBC is an open specification
which provides a consistent API for developers to use for accessing
data sources (which are often, but not always, databases). PHP is an
HTML-embeddable scripting language. If you need ODBC support for PHP
applications, you will need to install this package and the php
package.

%package bcmath
Summary: A module for PHP applications for using the bcmath library
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libbcmath is licensed under LGPLv2+
License: PHP and LGPLv2+
# only available if PHP was configured with --enable-bcmath
Requires: %{php_common}%{?_isa} = %{version}-%{release}

%description bcmath
The php-bcmath package contains a dynamic shared object that will add
support for using the bcmath library to PHP.

%package ldap
Summary: A module for PHP applications that use LDAP
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{php_common}%{?_isa} = %{version}-%{release}
BuildRequires: cyrus-sasl-devel, openldap-devel

%description ldap
The php-ldap adds Lightweight Directory Access Protocol (LDAP)
support to PHP. LDAP is a set of protocols for accessing directory
services over the Internet. PHP is an HTML-embedded scripting
language.

%if %{with_mysqlnd}
# As of 5.4.0 The MySQL Native Driver is now the default for all MySQL extensions
%package mysqlnd
Summary: A module for PHP applications that use MySQL databases
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{php_common}%{?_isa} = %{version}-%{release}
Provides: php_database
# This extension was DEPRECATED in PHP 5.5.0, and it was removed in PHP 7.0.0
Provides: php-mysqli = %{version}-%{release}
Provides: php-mysqli%{?_isa} = %{version}-%{release}
Provides: php-pdo_mysql, php-pdo_mysql%{?_isa}

%description mysqlnd
The php-mysqlnd package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php package.

This package use the MySQL Native Driver
%else
# This extension was DEPRECATED in PHP 5.5.0, and it was removed in PHP 7.0.0
%package mysql
Summary: A module for PHP applications that use MySQL databases
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{php_common}%{?_isa} = %{version}-%{release}
Provides: php_database
Provides: php-mysqli = %{version}-%{release}
Provides: php-mysqli%{?_isa} = %{version}-%{release}
Provides: php-pdo_mysql, php-pdo_mysql%{?_isa}
Obsoletes: mod_php3-mysql, stronghold-php-mysql
BuildRequires: mysql-devel

%description mysql
The php-mysql package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php package.
%endif

%package sqlite
Summary: SQLite database bindings
Group: Development/Libraries
License: PHP
Requires: %{php_common}%{?_isa} = %{version}-%{release}

%description sqlite
SQLite is a C library that implements an embeddable SQL database engine.

%prep
%setup -q -n php-%{version}

# sqlite ext
%setup -q -n php-%{version} -T -D -a 18

%if %{with_cgi}
# ionCube Loader
%setup -q -n php-%{version} -T -D -a 16
# Zend Guard Loader
%setup -q -n php-%{version} -T -D -a 17
%endif

%if %{with_relocation}
%patch405 -p1
%else
%patch5 -p1
%endif
%patch8 -p1
%if %{with_relocation}
%patch409 -p1
%endif

%patch40 -p1
%patch42 -p1
%patch43 -p1
%patch46 -p1
%patch47 -p1
%patch49 -p1

# Fixes for tests
%patch300 -p1

%patch91 -p1
%patch92 -p1
%patch93 -p1
%patch94 -p1
%patch96 -p1

# Prevent %%doc confusion over LICENSE files
cp Zend/LICENSE Zend/ZEND_LICENSE
cp TSRM/LICENSE TSRM_LICENSE
cp ext/ereg/regex/COPYRIGHT regex_COPYRIGHT
cp sapi/fpm/LICENSE fpm_LICENSE
cp ext/mbstring/libmbfl/LICENSE libmbfl_LICENSE
cp ext/mbstring/oniguruma/COPYING oniguruma_COPYING
cp ext/mbstring/ucgendat/OPENLDAP_LICENSE ucgendat_LICENSE
cp ext/fileinfo/libmagic/LICENSE libmagic_LICENSE
cp ext/phar/LICENSE phar_LICENSE
cp ext/bcmath/libbcmath/COPYING.LIB libbcmath_COPYING

# Multiple builds for multiple SAPIs
mkdir build-apache
%if %{with_cgi}
mkdir build-cgi
%endif
%if %{with_fpm}
mkdir build-fpm
%endif

# ----- Manage known as failed test -------
# affected by systzdata patch
rm ext/date/tests/timezone_location_get.phpt
rm ext/date/tests/timezone_version_get.phpt
rm ext/date/tests/timezone_version_get_basic1.phpt
# fails sometime
rm -f ext/sockets/tests/mcast_ipv?_recv.phpt
# cause stack exhausion
rm Zend/tests/bug54268.phpt

# Safety check for API version change.
pver=$(sed -n '/#define PHP_VERSION /{s/.* "//;s/".*$//;p}' main/php_version.h)
if test "x${pver}" != "x%{version}%{?rcver}"; then
   : Error: Upstream PHP version is now ${pver}, expecting %{version}%{?rcver}.
   : Update the version/rcver macros and rebuild.
   exit 1
fi

vapi=`sed -n '/#define PHP_API_VERSION/{s/.* //;p}' main/php.h`
if test "x${vapi}" != "x%{apiver}"; then
   : Error: Upstream API version is now ${vapi}, expecting %{apiver}.
   : Update the apiver macro and rebuild.
   exit 1
fi

vzend=`sed -n '/#define ZEND_MODULE_API_NO/{s/^[^0-9]*//;p;}' Zend/zend_modules.h`
if test "x${vzend}" != "x%{zendver}"; then
   : Error: Upstream Zend ABI version is now ${vzend}, expecting %{zendver}.
   : Update the zendver macro and rebuild.
   exit 1
fi

# Safety check for PDO ABI version change
vpdo=`sed -n '/#define PDO_DRIVER_API/{s/.*[ 	]//;p}' ext/pdo/php_pdo_driver.h`
if test "x${vpdo}" != "x%{pdover}"; then
   : Error: Upstream PDO ABI version is now ${vpdo}, expecting %{pdover}.
   : Update the pdover macro and rebuild.
   exit 1
fi

# Check for some extension version
ver=$(sed -n '/#define PHP_ZENDOPCACHE_VERSION /{s/.* "//;s/".*$//;p}' ext/opcache/ZendAccelerator.h)
if test "$ver" != "%{opcachever}"; then
   : Error: Upstream OPCACHE version is now ${ver}, expecting %{opcachever}.
   : Update the opcachever macro and rebuild.
   exit 1
fi

ver=$(sed -n '/#define PHP_JSON_VERSION /{s/.* "//;s/".*$//;p}' ext/json/php_json.h)
if test "$ver" != "%{jsonver}"; then
   : Error: Upstream JSON version is now ${ver}, expecting %{jsonver}.
   : Update the jsonver macro and rebuild.
   exit 1
fi

# https://bugs.php.net/63362 - Not needed but installed headers.
# Drop some Windows specific headers to avoid installation,
# before build to ensure they are really not needed.
rm -f TSRM/tsrm_win32.h \
      TSRM/tsrm_config.w32.h \
      Zend/zend_config.w32.h \
      ext/mysqlnd/config-win.h \
      ext/standard/winver.h \
      main/win32_internal_function_disabled.h \
      main/win95nt.h

# Fix some bogus permissions
find . -name \*.[ch] -exec chmod 644 {} \;
chmod 644 README.*

# php-fpm configuration files for tmpfiles.d
%if %{with_fpm} && 0%{?rhel} >= 7
echo "d %{fpm_rundir} 755 root root" >php-fpm.tmpfiles
%endif

# Some extensions have their own configuration file
%if %{with_relocation}
cat %{SOURCE150} > 10-opcache.ini
%else
cat %{SOURCE50} > 10-opcache.ini
%endif
cp %{SOURCE53} 30-mysql.ini
cp %{SOURCE54} 30-mysqli.ini

# according to https://forum.remirepo.net/viewtopic.php?pid=8407#p8407
%if 0%{?rhel} >= 7
%ifarch x86_64
sed -e '/opcache.huge_code_pages/s/0/1/' -i 10-opcache.ini
%endif
%endif

%build
# Set build date from https://reproducible-builds.org/specs/source-date-epoch/
export SOURCE_DATE_EPOCH=$(date +%s -r NEWS)

# aclocal workaround - to be improved
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >>aclocal.m4

# Force use of system libtool:
libtoolize --force --copy
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >build/libtool.m4

# Regenerate configure scripts (patches change config.m4's)
touch configure.in
./buildconf --force

CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign"
export CFLAGS

# Install extension modules in %{php_libdir}/modules.
EXTENSION_DIR=%{php_libdir}/modules; export EXTENSION_DIR

# Set PEAR_INSTALLDIR to ensure that the hard-coded include_path
# includes the PEAR directory even though pear is packaged
# separately.
PEAR_INSTALLDIR=%{pear_datadir}; export PEAR_INSTALLDIR

# Shell function to configure and build a PHP tree.
build() {
# Old/recent bison version seems to produce a broken parser;
# upstream uses GNU Bison 2.3. Workaround:
mkdir Zend && cp ../Zend/zend_{language,ini}_{parser,scanner}.[ch] Zend

ln -sf ../configure
%configure \
    --cache-file=../config.cache \
    --disable-debug \
    --enable-calendar \
    --enable-dba --with-db4=%{_prefix} --with-gdbm \
    --enable-exif \
    --enable-ftp \
    --enable-gd-native-ttf \
    --enable-intl \
    --enable-mbstring \
    --enable-pdo \
    --enable-soap \
    --enable-sockets \
%if %{with_zip}
    --enable-zip \
%if %{with_libzip}
    --with-libzip \
%endif
%endif
    --libdir=%{php_libdir} \
%if %{with_relocation}
    --sysconfdir=%{php_sysconfdir} \
%endif
    --with-bz2 \
    --with-config-file-path=%{php_sysconfdir} \
    --with-curl=%{_prefix} \
    --with-freetype-dir=%{_prefix} \
    --with-gd \
    --with-gettext \
    --with-icu-dir=%{_prefix} \
%if 0%{?rhel}
    --with-imap \
    --with-imap-ssl \
%endif
    --with-jpeg-dir=%{_prefix} \
    --with-layout=GNU \
    --with-libdir=%{_lib} \
    --with-mcrypt=%{_prefix} \
    --with-mssql=%{_prefix} \
    --with-mysql-sock=%{mysql_sock} \
    --with-openssl \
    --without-pear \
    --with-pdo-odbc=unixODBC,%{_prefix} \
    --with-pic \
    --with-png-dir=%{_prefix} \
    --with-regex \
    --with-system-ciphers \
    --with-system-tzdata \
    --with-zlib \
%if %{with_dtrace}
    --enable-dtrace \
%endif
    --disable-posix \
    --enable-dom=shared \
%if %{with_mysqlnd}
    --enable-mysqlnd=shared \
    --with-mysqli=shared,mysqlnd \
    --with-mysql=shared,mysqlnd \
    --with-pdo-mysql=shared,mysqlnd \
%else
    --with-mysqli=shared,%{mysql_config} \
    --with-mysql=shared,%{_prefix} \
    --with-pdo-mysql=shared,%{_prefix} \
%endif
    --enable-opcache \
    --enable-simplexml=shared \
    --enable-wddx=shared \
    --enable-xmlreader=shared \
    --enable-xmlwriter=shared \
    --with-pdo-pgsql=shared,%{_prefix} \
    --with-pgsql=shared \
    --with-xmlrpc \
    --with-xsl=shared,%{_prefix} \
    --with-sqlite=shared --enable-sqlite-utf8 \
    --with-unixODBC=shared,%{_prefix} \
    --enable-bcmath=shared \
    --with-ldap=shared --with-ldap-sasl \
    $*

if test $? != 0; then
  tail -500 config.log
  : configure failed
  exit 1
fi

make -j4 %{?_smp_mflags}
}

# Build /usr/bin/php-cgi with the CGI SAPI, and most shared extensions
%if %{with_cgi}
pushd build-cgi

build \
%if %{with_relocation}
      --program-suffix=%{program_suffix} \
%endif
      --disable-cli \
      --with-config-file-scan-dir=%{php_sysconfdir}/php-cgi-fcgi.d
popd
%endif

without_shared="--disable-bcmath --disable-dom --disable-opcache \
      --disable-simplexml \
      --disable-wddx --disable-xmlreader --disable-xmlwriter --without-ldap \
      --without-mysql --without-mysqli --without-pdo-mysql \
      --without-pdo-pgsql --without-pgsql \
      --without-sqlite \
      --without-unixODBC --without-xsl"

# Build Apache module, and the CLI SAPI, /usr/bin/php
pushd build-apache
build --with-apxs2=%{_httpd_apxs} --disable-cgi \
%if %{with_relocation}
    --program-suffix=%{program_suffix} \
%endif
%if %{with_cgi}
    ${without_shared} \
%if %{with_mysqlnd}
    --disable-mysqlnd \
%endif
%endif
    --with-config-file-scan-dir=%{php_sysconfdir}/php.d
popd

# Build php-fpm
%if %{with_fpm}
pushd build-fpm
build --enable-fpm \
%if %{with_relocation}
      --program-suffix=%{program_suffix} \
%endif
      --with-fpm-acl \
%if 0%{?rhel} >= 7
      --with-fpm-systemd \
%endif
      --disable-cgi \
      --disable-cli \
      ${without_shared} \
      --with-config-file-scan-dir=%{php_sysconfdir}/php.d
popd
%endif

%check
%if %{with_test}
cd build-apache

# Run tests, using the CLI SAPI
export NO_INTERACTION=1 REPORT_EXIT_STATUS=1 MALLOC_CHECK_=2
export SKIP_ONLINE_TESTS=1
unset TZ LANG LC_ALL
if ! make test; then
  set +x
  for f in $(find .. -name \*.diff -type f -print); do
    if ! grep -q XFAIL "${f/.diff/.phpt}"
    then
      echo "TEST FAILURE: $f --"
      cat "$f"
      echo -e "\n-- $f result ends."
    fi
  done
  set -x
  #exit 1
fi
unset NO_INTERACTION REPORT_EXIT_STATUS MALLOC_CHECK_
%endif

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# Install everything from the CGI SAPI build
%if %{with_cgi}
make -C build-cgi install \
     INSTALL_ROOT=$RPM_BUILD_ROOT
%else
make -C build-apache  install-modules \
     INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# all except install-sapi - use apxs for rpmbuild is failed (httpd.conf is missed)
make -C build-apache  install-binaries install-build install-headers install-programs install-pharcmd install-pdo-headers \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# Install the php-fpm binary
%if %{with_fpm}
make -C build-fpm install-fpm \
     INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# Install the default configuration file and icons
install -m 755 -d $RPM_BUILD_ROOT%{php_sysconfdir}/
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{php_sysconfdir}/php.ini
install -m 755 -d $RPM_BUILD_ROOT%{_httpd_contentdir}/icons
install -m 644 *.gif $RPM_BUILD_ROOT%{_httpd_contentdir}/icons/php.gif

# For third-party packaging:
install -m 755 -d $RPM_BUILD_ROOT%{php_libdir}/pear \
                  $RPM_BUILD_ROOT%{php_datadir}

# install the DSO
install -m 755 -d $RPM_BUILD_ROOT%{_httpd_moddir}
install -m 755 build-apache/libs/libphp5.so $RPM_BUILD_ROOT%{_httpd_moddir}

# Apache config fragment
install -m 755 -d $RPM_BUILD_ROOT%{_httpd_confdir}
# Due to posibility of use apache 2.2 and 2.4 we copy it locally
%if %{with_relocation}
cat %{SOURCE101} > httpd-php.conf
%else
cat %{SOURCE1} > httpd-php.conf
%endif
install -D -m 644 httpd-php.conf $RPM_BUILD_ROOT%{_httpd_confdir}/02-php.conf

# Dual config file with httpd >= 2.4 (fedora >= 18)
%if %{with_ap24}
install -D -m 644 %{SOURCE9} $RPM_BUILD_ROOT%{_httpd_modconfdir}/15-php.conf
%else
cat %{SOURCE9} httpd-php.conf > $RPM_BUILD_ROOT%{_httpd_confdir}/02-php.conf
%endif

install -m 755 -d $RPM_BUILD_ROOT%{php_sysconfdir}/php.d
install -m 755 -d $RPM_BUILD_ROOT%{php_sharedstatedir}
install -m 700 -d $RPM_BUILD_ROOT%{php_sharedstatedir}/session

%if %{with_cgi}
# install ioncube
install -m 755 ioncube/ioncube_loader_lin_5.6.so $RPM_BUILD_ROOT%{php_libdir}/modules/ioncube_loader_lin_5.6.so
install -m 755 zend-loader-php5.6-linux-x86_64/ZendGuardLoader.so $RPM_BUILD_ROOT%{php_libdir}/modules/ZendGuardLoader.so

# install config
sed "s,@LIBDIR@,%{_libdir},g" \
    < %{SOURCE15} > php-cgi-fcgi.ini
install -m 644 php-cgi-fcgi.ini \
           $RPM_BUILD_ROOT%{php_sysconfdir}/php-cgi-fcgi.ini
%endif
install -m 755 -d $RPM_BUILD_ROOT%{php_sysconfdir}/php-cgi-fcgi.d

# PHP-FPM stuff
# Log
%if %{with_fpm}
install -m 700 -d $RPM_BUILD_ROOT%{fpm_sharedstatedir}/session
install -m 700 -d $RPM_BUILD_ROOT%{fpm_sharedstatedir}/wsdlcache
install -m 700 -d $RPM_BUILD_ROOT%{fpm_sharedstatedir}/opcache
install -m 755 -d $RPM_BUILD_ROOT%{fpm_logdir}
install -m 755 -d $RPM_BUILD_ROOT%{fpm_rundir}
# Config
install -m 755 -d $RPM_BUILD_ROOT%{fpm_config_d}
# LogRotate
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%if %{with_relocation}
install -m 644 %{SOURCE104} $RPM_BUILD_ROOT%{fpm_config}
install -m 644 %{SOURCE105} $RPM_BUILD_ROOT%{fpm_config_d}/www.conf
install -m 644 %{SOURCE107} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{fpm_logrotate}
# Nginx configuration
install -D -m 644 %{SOURCE113} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/%{fpm_name}.conf
install -D -m 644 %{SOURCE114} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/default.d/%{main_name}.conf
%else
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{fpm_config}
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{fpm_config_d}/www.conf
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{fpm_logrotate}
# Nginx configuration
install -D -m 644 %{SOURCE13} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/%{fpm_name}.conf
install -D -m 644 %{SOURCE14} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/default.d/%{main_name}.conf
%endif  # with_relocation
mv $RPM_BUILD_ROOT%{fpm_config}.default .
%if 0%{?rhel} >= 7
# tmpfiles.d
install -m 755 -d $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d
install -m 644 php-fpm.tmpfiles $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d/%{fpm_tmpfiles_d}
# install systemd unit files and scripts for handling server startup
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/%{fpm_service_d}
install -m 755 -d $RPM_BUILD_ROOT%{_unitdir}
%if %{with_relocation}
install -m 644 %{SOURCE106} $RPM_BUILD_ROOT%{_unitdir}/%{fpm_unit}
%else
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT%{_unitdir}/%{fpm_unit}
%endif  # with_relocation
%else
# Service
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/init.d
%if %{with_relocation}
install -m 755 %{SOURCE110} $RPM_BUILD_ROOT%{_sysconfdir}/init.d/%{fpm_service}
%else
install -m 755 %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/init.d/%{fpm_service}
%endif  # with_relocation
%endif  # rhel >= 7
%endif  # with_fpm

# Generate files lists and stub .ini files for each subpackage
for mod in \
    dom xsl bcmath xmlreader xmlwriter \
    simplexml \
    opcache \
    wddx \
    sqlite \
    pgsql pdo_pgsql odbc ldap \
%if %{with_mysqlnd}
    mysqlnd \
%endif
    mysql mysqli pdo_mysql \
    ; do
    case $mod in
      opcache)
        # Zend extensions
        ini=10-${mod}.ini;;
      # wddx requires libxml (http://php.net/manual/en/wddx.requirements.php)
      # xmlreader requires libxml (http://php.net/manual/en/xmlreader.requirements.php)
      pdo_mysql|mysql|mysqli|xsl|dom|wddx|xmlreader|xmlwriter|simplexml)
        # Extensions with dependencies on 20-*
        ini=30-${mod}.ini;;
      *)
        # Extensions with no dependency
        ini=20-${mod}.ini;;
    esac
    # some extensions have their own config file
    if [ -f ${ini} ]; then
      cp -p ${ini} $RPM_BUILD_ROOT%{php_sysconfdir}/php.d/${ini}
    else
      cat > $RPM_BUILD_ROOT%{php_sysconfdir}/php.d/${ini} <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF
    fi
%if %{with_cgi}
      cp -p $RPM_BUILD_ROOT%{php_sysconfdir}/{php.d,php-cgi-fcgi.d}/${ini}
      cat > files.${mod} <<EOF
%attr(755,root,root) %{php_libdir}/modules/${mod}.so
%config(noreplace) %attr(644,root,root) %{php_sysconfdir}/php.d/${ini}
%config(noreplace) %attr(644,root,root) %{php_sysconfdir}/php-cgi-fcgi.d/${ini}
EOF
%else
      cat > files.${mod} <<EOF
%attr(755,root,root) %{php_libdir}/modules/${mod}.so
%config(noreplace) %attr(644,root,root) %{php_sysconfdir}/php.d/${ini}
EOF
%endif
done

# The dom, xsl and xml* modules are all packaged in php-xml
cat files.dom files.xsl files.xml{reader,writer} files.wddx \
    files.simplexml >> files.xml

%if %{with_mysqlnd}
cat files.mysql files.mysqli files.pdo_mysql >> files.mysqlnd
%else
cat files.mysqli files.pdo_mysql >> files.mysql
%endif

# postgres support as separate php-pgsql package
cat files.pdo_pgsql >> files.pgsql

# The default Zend OPcache blacklist file
install -m 644 %{SOURCE51} $RPM_BUILD_ROOT%{php_sysconfdir}/php.d/opcache-default.blacklist

%if %{with_relocation}
cat %{SOURCE103} > macros.php
%else
cat %{SOURCE3} > macros.php
%endif

# Install the macros file:
sed -i -e "s/@PHP_APIVER@/%{apiver}%{isasuffix}/" \
    -e "s/@PHP_ZENDVER@/%{zendver}%{isasuffix}/" \
    -e "s/@PHP_PDOVER@/%{pdover}%{isasuffix}/" \
    -e "s/@PHP_VERSION@/%{version}/" macros.php
%if 0%{?rhel} >= 7
mkdir -p $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d
install -m 644 -D macros.php \
           $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.%{php_main}
%else
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm
install -m 644 -c macros.php \
           $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.%{php_main}
%endif

# Remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{php_libdir}/modules/*.a \
       $RPM_BUILD_ROOT%{_bindir}/{phptar} \
       $RPM_BUILD_ROOT%{pear_datadir} \
       $RPM_BUILD_ROOT%{_libdir}/libphp5.la

# Remove irrelevant docs
rm -f README.{Zeus,QNX,CVS-RULES}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
for i in files.* macros.php; do
    if [ -f "$i" ]; then
        rm -f $i
    fi
done

%if %{with_fpm}
%pre fpm
getent group nginx >/dev/null || \
  groupadd -r nginx
getent passwd nginx >/dev/null || \
    useradd -r -d %{_nginx_home} -g nginx \
    -s /sbin/nologin -c "Nginx web server" nginx
exit 0

%post fpm
%if 0%{?rhel} >= 7
%systemd_post %{fpm_unit}
%else
if [ $1 = 1 ]; then
    # Initial installation
    /sbin/chkconfig --add %{fpm_service} 2>/dev/null
fi
%endif

%preun fpm
%if 0%{?rhel} >= 7
%systemd_preun %{fpm_unit}
%else
if [ $1 = 0 ]; then
    # Package removal, not upgrade
    /usr/sbin/service %{fpm_service} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{fpm_service} 2>/dev/null
fi
%endif

%postun fpm
%if 0%{?rhel} >= 7
%systemd_postun_with_restart %{fpm_unit}
%else
if [ $1 -ge 1 ]; then
    /usr/sbin/service %{fpm_service} condrestart >/dev/null 2>&1 || :
fi
%endif
%endif

%files
%defattr(-,root,root)
%{_httpd_moddir}/libphp5.so
%config(noreplace) %{_httpd_confdir}/02-php.conf
%if %{with_ap24}
%config(noreplace) %{_httpd_modconfdir}/15-php.conf
%endif
%{_httpd_contentdir}/icons/*.gif

%files common
%config(noreplace) %{php_sysconfdir}/php.ini
%dir %{php_sysconfdir}/php.d
%dir %{php_sysconfdir}/php-cgi-fcgi.d
%dir %{php_libdir}
%dir %{php_sharedstatedir}
%dir %{php_datadir}
%attr(0770,root,nogroup) %dir %{php_sharedstatedir}/session

%files cli
%defattr(-,root,root)
%attr(0700,root,root) %{_bindir}/%{bin_cli}
%attr(0700,root,root) %{_bindir}/phar.%{bin_phar}
%attr(0700,root,root) %{_bindir}/%{bin_phar}
# provides phpize here (not in -devel) for pecl command
%attr(0700,root,root) %{_bindir}/%{bin_phpize}
%{_mandir}/man1/%{bin_cli}.1*
%{_mandir}/man1/%{bin_phar}.1*
%{_mandir}/man1/phar.%{bin_phar}.1*
%{_mandir}/man1/%{bin_phpize}.1*
%doc sapi/cgi/README* sapi/cli/README

%if %{with_cgi}
%files cgi
%{_bindir}/%{bin_cgi}
%config(noreplace) %{php_sysconfdir}/php-cgi-fcgi.ini
%{_mandir}/man1/%{bin_cgi}.1*

%files ioncube
%attr(755,root,root) %{php_libdir}/modules/ioncube_loader_lin_5.6.so

%files zend-guard-loader
%attr(755,root,root) %{php_libdir}/modules/ZendGuardLoader.so
%endif

%if %{with_fpm}
%files fpm
%doc %{fpm_config_name}.default
%doc fpm_LICENSE
%{_sbindir}/%{bin_fpm}
%attr(0770,root,nginx) %dir %{fpm_sharedstatedir}/session
%attr(0770,root,nginx) %dir %{fpm_sharedstatedir}/wsdlcache
%attr(0770,root,nginx) %dir %{fpm_sharedstatedir}/opcache
%config(noreplace) %{_sysconfdir}/nginx/conf.d/%{fpm_name}.conf
%config(noreplace) %{_sysconfdir}/nginx/default.d/%{main_name}.conf
%config(noreplace) %{fpm_config}
%config(noreplace) %{fpm_config_d}/www.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{fpm_logrotate}
%if 0%{?rhel} >= 7
%dir %{_sysconfdir}/systemd/system/%{fpm_service_d}
%{_prefix}/lib/tmpfiles.d/%{fpm_tmpfiles_d}
%{_unitdir}/%{fpm_unit}
%else
%{_sysconfdir}/init.d/%{fpm_service}
%endif
%dir %{fpm_config_d}
# log owned by apache for log
%attr(770,nginx,root) %dir %{fpm_logdir}
%dir %{fpm_rundir}
%{_mandir}/man8/%{bin_fpm}.8*
%dir %{fpm_datadir}
%{fpm_datadir}/status.html
%endif

%files devel
%defattr(-,root,root)
%{_bindir}/%{bin_php_config}
%{php_includedir}
%{php_libdir}/build
%{_mandir}/man1/%{bin_php_config}.1*
%if 0%{?rhel} >= 7
%config %{_rpmconfigdir}/macros.d/macros.%{php_main}
%else
%config %{_sysconfdir}/rpm/macros.%{php_main}
%endif

%files xml -f files.xml
%files pgsql -f files.pgsql
%files sqlite -f files.sqlite

%files opcache -f files.opcache
%config(noreplace) %{php_sysconfdir}/php.d/opcache-default.blacklist

%files odbc -f files.odbc
%files bcmath -f files.bcmath
%files ldap -f files.ldap
%if %{with_mysqlnd}
%files mysqlnd -f files.mysqlnd
%else
%files mysql -f files.mysql
%endif

%changelog
* Mon Feb 19 2018 Alexander Ursu <alexander.ursu@gmail.com> 5.6.33-1
- update to 5.6.33
- added fpm sapi
- added php-common
- added relocation support

* Sat Dec 16 2017 Alexander Ursu <alexander.ursu@gmail.com> 5.6.31-11
- fixed build

* Wed Oct 18 2017 Alexander Ursu <alexander.ursu@gmail.com> 5.6.31-10
- disabled user error handler for custom logging
- added ability to output logs regardless of log_errors and
  error_reporting settings

* Fri Sep 29 2017 Alexander Ursu <alexander.ursu@gmail.com> 5.6.31-8
- introduced scan directory for php-cgi
  http://php.net/manual/de/configuration.file.php#configuration.file.scan
 
* Thu Sep 21 2017 Alexander Ursu <alexander.ursu@gmail.com> 5.6.31-5
- disabe PHP functions logging output to browser

* Mon Sep 18 2017 Alexander Ursu <alexander.ursu@gmail.com> 5.6.31-4
- added logging for several PHP functions, inclding exec() and
  eval()

* Tue Sep 12 2017 Alexander Ursu <alexander.ursu@gmail.com> 5.6.31-3
- added support for Apache 2.4

* Fri Jul 28 2017 Alexander Ursu <alexander.ursu@gmail.com> 5.6.31-2
- make mysql package
- make php-mysqlnd package optional

* Wed Jul 19 2017 Alexander Ursu <alexander.ursu@gmail.com> 5.6.31-1
- upgrade to 5.6.31

* Mon Jun 12 2017 Alexander Ursu <alexander.ursu@gmail.com> 5.6.30-2
- upgrade to PHP 5.6.30
- added opcache and sqlite sub packages
- added levels to PHP ini additional files
  10 - zend extensions
  20 - extensions without dependencies
  30 - extensions depended on 20
