%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%{!?pecl_phpdir: %{expand: %%global pecl_phpdir  %(%{__pecl} config-get php_dir  2> /dev/null || echo undefined)}}

%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}
%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)

%global php_base php54
%global pecl_name xhprof
%global real_name xhprof

%global commit c90e966

Summary: Function-level hierarchical profiler for PHP
Name: %{php_base}-pecl-xhprof

Version: 0.%{commit}
Release: 2.vortex%{?dist}
License: PHP
Group: Development/Languages
Vendor: Vortex RPM
URL: https://github.com/facebook/xhprof/tarball/master

Source0: facebook-%{pecl_name}-%{commit}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: %{php_base}-devel, %{php_base}-cli, %{php_base}-pear
Requires(post): %{__pecl}
Requires(postun): %{__pecl}

%if %{?php_zend_api}0
Requires: php(zend-abi) = %{php_zend_api}
Requires: php(api) = %{php_core_api}
%else
Requires: %{php_base}-api = %{php_apiver}
%endif

%description
XHProf is a function-level hierarchical profiler for PHP and has a simple
HTML based user interface. The raw data collection component is
implemented in C (as a PHP extension). The reporting/UI layer is all
in PHP. It is capable of reporting function-level call counts and
inclusive and exclusive wall time, CPU time and memory usage. Additionally,
it supports ability to compare two runs (hierarchical DIFF reports), or
aggregate results from multiple runs. Originally developed at Facebook,
XHProf was open sourced in Mar, 2009
%prep 
%setup -q -n facebook-%{pecl_name}-%{commit}


%build
cd extension
phpize
%configure
%{__make} %{?_smp_mflags}


%install
cd extension
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
xhprof.output_dir=/tmp/xhprof
EOF


%clean
%{__rm} -rf %{buildroot}



%postun
if [ $1 -eq 0 ]; then
%{__pecl} uninstall --nodeps --ignore-errors --register-only %{pecl_name} >/dev/null || :
fi


%files
%defattr(-, root, root, -)
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so


%changelog
* Mon Nov 02 2012 Ilya A. Otyutskiy <sharp@thesharp.ru> - 0.c90e966.2.vortex
- Initial packaging.

* Mon Nov 01 2012 Ilya A. Otyutskiy <sharp@thesharp.ru> - 0.c90e966.1.vortex
- Initial packaging.
