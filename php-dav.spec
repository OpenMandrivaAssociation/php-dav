%define modname dav
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A59_%{modname}.ini

Summary:	A PHP WebDAV for PHP
Name:		php-%{modname}
Version:	1.2
Release:	%mkrel 6
Group:		Development/PHP
License:	BSD-like
URL:		http://php-webdav.pureftpd.org/project/php-webdav
Source0:	http://download.pureftpd.org/php-webdav/php-webdav-%{version}.tar.gz
BuildRequires:	php-devel >= 3:5.2.1
BuildRequires:	neon-devel
BuildRequires:	file
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The PHP WebDAV extension allows easy access to remote resources with PHP
through the DAV protocol.

%prep

%setup -q -n dav

# fix permissions
find . -type f | xargs chmod 644

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
%serverbuild

phpize --clean
phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make

mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS LICENSE README tests
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 1.2-6mdv2012.0
+ Revision: 795412
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1.2-5
+ Revision: 761305
- fix deps
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.2-4
+ Revision: 696404
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.2-3
+ Revision: 695377
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.2-2
+ Revision: 646622
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1.2-1mdv2011.0
+ Revision: 630316
- 1.2

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1.1-21mdv2011.0
+ Revision: 629775
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.1-20mdv2011.0
+ Revision: 628089
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1-19mdv2011.0
+ Revision: 600471
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1-18mdv2011.0
+ Revision: 588754
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1-17mdv2010.1
+ Revision: 514528
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1-16mdv2010.1
+ Revision: 485349
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1.1-15mdv2010.1
+ Revision: 468155
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1.1-14mdv2010.0
+ Revision: 451261
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 1.1-13mdv2010.0
+ Revision: 397350
- Rebuild

* Wed Jul 08 2009 Oden Eriksson <oeriksson@mandriva.com> 1.1-12mdv2010.0
+ Revision: 393462
- rebuild (#2)
- rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 1.1-10mdv2010.0
+ Revision: 376980
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.1-9mdv2009.1
+ Revision: 346411
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1.1-8mdv2009.1
+ Revision: 341717
- rebuilt against php-5.2.9RC2

* Sun Jan 04 2009 Oden Eriksson <oeriksson@mandriva.com> 1.1-7mdv2009.1
+ Revision: 324290
- rebuild

* Fri Dec 12 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1-6mdv2009.1
+ Revision: 313605
- fix #46320 (Php-dav incorrectly useless empty directory /etc/php.d/dav)

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1-5mdv2009.1
+ Revision: 310258
- rebuilt against php-5.2.7

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1-4mdv2009.0
+ Revision: 238384
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1-3mdv2009.0
+ Revision: 200192
- rebuilt for php-5.2.6

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1-2mdv2008.1
+ Revision: 162216
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 1.1-1mdv2008.1
+ Revision: 107597
- 1.1
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0-5mdv2008.0
+ Revision: 77534
- rebuilt against php-5.2.4

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0-4mdv2008.0
+ Revision: 39488
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0-3mdv2008.0
+ Revision: 33803
- rebuilt against new upstream version (5.2.3)
- rebuilt against new upstream version (5.2.2)


* Tue Mar 06 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0-1mdv2007.0
+ Revision: 133867
- Import php-dav

* Tue Mar 06 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0-1mdv2007.1
- initial Mandriva package

