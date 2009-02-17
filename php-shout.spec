%define modname shout
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A57_%{modname}.ini

Summary:	PHP module for communicating with Icecast servers
Name:		php-%{modname}
Version:	0.9.2
Release:	%mkrel 14
Group:		Development/PHP
License:	LGPL
URL:		http://phpshout.sourceforge.net/
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
