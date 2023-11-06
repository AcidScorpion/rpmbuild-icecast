%global global_ver 2.4.4
%global global_rel 1
%global debug_package %{nil}

Name:		icecast
Version:	%{global_ver}
Release:	%{global_rel}%{?dist}
Summary:	Icecast is a streaming media server

License:	GPLv2+
URL:		https://icecast.org
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}.logrotate
Source2:	%{name}.service

%description
Icecast is a streaming media (audio/video) server
which currently supports Ogg (Vorbis and Theora),
Opus, WebM and MP3 streams.
It can be used to create an Internet radio station
or a privately running jukebox and many things in between.
It is very versatile in that new formats can be added relatively easily
and supports open standards for communication and interaction.

%prep
%autosetup

%build
%configure
%make_build

%install
%{__rm} -rf %{buildroot}

%make_install

%{__mkdir_p} %{buildroot}%{_localstatedir}/log/%{name}
%{__install} -Dpm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%{__install} -Dpm 0644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service

%pre
%{_bindir}/getent passwd %{name} >/dev/null || \
  %{_sbindir}/useradd -M -r -d %{_datadir}%{name} -s /sbin/nologin \
  -c "%{name} streaming server" %{name} > /dev/null 2>&1 || :

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%config(noreplace) %attr(-,root,%{name}) %{_sysconfdir}/%{name}.xml
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_docdir}/%{name}
%dir %attr(-,%{name},%{name}) %{_localstatedir}/log/%{name}
%{_sysconfdir}/logrotate.d/%{name}
%{_unitdir}/%{name}.service

%changelog
* Mon Nov 06 2023 Acid_Scorpion <dmitry@petrich.me>
- Initial build
