%define modname shout
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A57_%{modname}.ini

Summary:	PHP module for communicating with Icecast servers
Name:		php-%{modname}
Version:	0.9.2
Release:	31
Group:		Development/PHP
License:	LGPL
URL:		https://phpshout.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/phpshout/phpShout-%{version}.tar.bz2
Patch0:		phpShout-nuke_hardcoded_cflags.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	libshout-devel >= 2.2
BuildRequires:	file
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
phpShout is a PHP5 Extension that wraps around the libshout library available
at icecast.org. LibShout is used in conjunction with an Icecast server to
create a streaming Internet radio station from your own music files. With
phpShout, PHP developers can create web-based streaming jukebox applications,
without worrying about the details of streaming the audio data. LibShout
handles all the metadata updates, data timing, and ensuring that no bad data
gets to the Icecast server.

%prep

%setup -q -n phpShout-%{version}
%patch0 -p0

# fix permissions
find . -type f | xargs chmod 644

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
%serverbuild

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

shout.allow_persistent = 1
shout.max_persistent   = -1
shout.max_links        = -1

shout.default_host     = localhost
shout.default_port     = 8000
shout.default_mount    = /phpShout
shout.default_user     = source
shout.default_password = hackme

shout.default_format   = SHOUT_FORMAT_OGG
shout.default_protocol = SHOUT_PROTOCOL_HTTP
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
[ "../package.xml" != "/" ] && rm -f ../package.xml

%files 
%defattr(-,root,root)
%doc examples tests LICENSE README TODO
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-30mdv2012.0
+ Revision: 795497
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-29
+ Revision: 761290
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-28
+ Revision: 696466
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-27
+ Revision: 695461
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-26
+ Revision: 646681
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-25mdv2011.0
+ Revision: 629867
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-24mdv2011.0
+ Revision: 628181
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-23mdv2011.0
+ Revision: 600527
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-22mdv2011.0
+ Revision: 588865
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-21mdv2010.1
+ Revision: 514650
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-20mdv2010.1
+ Revision: 485476
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-19mdv2010.1
+ Revision: 468249
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-18mdv2010.0
+ Revision: 451355
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 0.9.2-17mdv2010.0
+ Revision: 397596
- Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-16mdv2010.0
+ Revision: 377025
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-15mdv2009.1
+ Revision: 346606
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-14mdv2009.1
+ Revision: 341795
- rebuilt against php-5.2.9RC2

* Thu Jan 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-13mdv2009.1
+ Revision: 323064
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-12mdv2009.1
+ Revision: 310304
- rebuilt against php-5.2.7

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-11mdv2009.0
+ Revision: 238428
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-10mdv2009.0
+ Revision: 200266
- rebuilt for php-5.2.6

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-9mdv2008.1
+ Revision: 162152
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-8mdv2008.1
+ Revision: 107716
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-7mdv2008.0
+ Revision: 77574
- rebuilt against php-5.2.4

* Tue Jul 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-6mdv2008.0
+ Revision: 51010
- use clean cflags (P0)
- use the %%serverbuild macro

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-5mdv2008.0
+ Revision: 39522
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-4mdv2008.0
+ Revision: 33875
- rebuilt against new upstream version (5.2.3)

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-3mdv2008.0
+ Revision: 21355
- rebuilt against new upstream version (5.2.2)


* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-2mdv2007.0
+ Revision: 117630
- rebuilt against new upstream version (5.2.1)

* Sat Jan 27 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-1mdv2007.1
+ Revision: 114367
- Import php-shout

* Sat Jan 27 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-1mdv2007.1
- initial Mandriva package

