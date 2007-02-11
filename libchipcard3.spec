#
# Conditional build:
%bcond_without	sysfs	# don't use sysfs to scan for ttyUSB
#
Summary:	A library for easy access to smart cards (chipcards)
Summary(pl):	Biblioteka do �atwego dost�pu do kart procesorowych
Name:		libchipcard3
Version:	3.0.0
Release:	1
License:	GPL v2 with OpenSSL linking exception
Group:		Libraries
Source0:	http://dl.sourceforge.net/libchipcard/%{name}-%{version}.tar.gz
# Source0-md5:	b6d77da54f2d3fc1c79882e20b591941
URL:		http://www.libchipcard.de/
BuildRequires:	gwenhywfar-devel >= 2.3.0
BuildRequires:	libusb-devel
# disabled in sources
#BuildRequires:	opensc-devel >= 0.9.4
BuildRequires:	pcsc-lite-devel
BuildRequires:	pkgconfig
%{?with_sysfs:BuildRequires:	sysfsutils-devel >= 1.3.0-3}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libchipcard allows easy access to smart cards. It provides basic
access to memory and processor cards and has special support for
German medical cards, German "GeldKarte" and HBCI (homebanking) cards
(both type 0 and type 1). It accesses the readers via CTAPI or IFD
interfaces and has successfully been tested with Towitoko, Kobil, SCM,
Orga, Omnikey and Reiner-SCT readers. This package contains the
chipcard2 daemon needed to access card readers.

%description -l pl
libchipcard pozwala na �atwy dost�p do kart procesorowych. Daje
podstawowy dost�p do kart pami�ciowych i procesorowych, ma tak�e
specjaln� obs�ug� niemieckich kart medycznych, niemieckich kart
"GeldKarte" oraz kart HBCI (do homebankingu, zar�wno typu 0 jak i 1).
Z czytnikami komunikuje si� poprzez interfejs CTAPI lub IFD, by�a
testowana z czytnikami Towitoko, Kobil, SCM, Orga, Omnikey i
Reiner-SCT. Ten pakiet zawiera demona chipcard2 potrzebnego do dost�pu
do czytnik�w kart.

%package devel
Summary:	libchipcard server development kit
Summary(pl):	Pliki programistyczne serwera libchipcard
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gwenhywfar-devel >= 2.3.0
Requires:	libusb-devel
%{?with_sysfs:Requires:	sysfsutils-devel >= 1.3.0-3}

%description devel
This package contains chipcard2-server-config and header files for
writing drivers, services or even your own chipcard daemon for
libchipcard.

%description devel -l pl
Ten pakiet zawiera skrypt chipcard2-server-config oraz pliki
nag��wkowe do pisania sterownik�w, us�ug, a nawet w�asnych demon�w
kart dla libchipcard.

%prep
%setup -q

%build
%configure \
	%{!?with_sysfs:ac_cv_header_sysfs_libsysfs_h=no}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/gwenhywfar/plugins/*/crypttoken/*.la
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/chipcard3/client/chipcardc3.conf{.default,}
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/chipcard3/client/chipcardc3.conf.example
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/chipcard3/server/chipcardd3.conf{.default,}
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/chipcard3/server/chipcardd3.conf.example

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO doc/{CERTIFICATES,CONFIG,IPCCOMMANDS} etc/*.conf.*
%attr(755,root,root) %{_bindir}/cardcommander3
%attr(755,root,root) %{_bindir}/chipcard3-tool
%attr(755,root,root) %{_bindir}/geldkarte3
%attr(755,root,root) %{_bindir}/kvkcard3
%attr(755,root,root) %{_bindir}/memcard3
%attr(755,root,root) %{_sbindir}/chipcardd3
%attr(755,root,root) %{_libdir}/libchipcard3c.so.*.*.*
%attr(755,root,root) %{_libdir}/libchipcard3d.so.*.*.*
%attr(755,root,root) %{_libdir}/libchipcard3_ctapi.so.*.*.*
%dir %{_libdir}/chipcard3
%dir %{_libdir}/chipcard3/server
%dir %{_libdir}/chipcard3/server/drivers
%{_libdir}/chipcard3/server/drivers/*.xml
%attr(755,root,root) %{_libdir}/chipcard3/server/drivers/SKEL1
%attr(755,root,root) %{_libdir}/chipcard3/server/drivers/ctapi
%attr(755,root,root) %{_libdir}/chipcard3/server/drivers/ifd
%dir %{_libdir}/chipcard3/server/lowlevel
%dir %{_libdir}/chipcard3/server/services
%{_libdir}/chipcard3/server/services/*.xml
%attr(755,root,root) %{_libdir}/chipcard3/server/services/kvks
%attr(755,root,root) %{_libdir}/gwenhywfar/plugins/*/crypttoken/*.so*
%{_libdir}/gwenhywfar/plugins/*/crypttoken/*.xml
%dir %{_datadir}/chipcard3
%dir %{_datadir}/chipcard3/client
%{_datadir}/chipcard3/client/apps
%{_datadir}/chipcard3/client/cards
%dir %{_datadir}/chipcard3/server
%{_datadir}/chipcard3/server/drivers
%dir %{_sysconfdir}/chipcard3
%dir %{_sysconfdir}/chipcard3/client
%dir %{_sysconfdir}/chipcard3/client/certs
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/chipcard3/client/chipcardc3.conf
%dir %{_sysconfdir}/chipcard3/server
%dir %{_sysconfdir}/chipcard3/server/certs
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/chipcard3/server/chipcardd3.conf
# XXX: move to init.d?
%attr(754,root,root) %{_sysconfdir}/chipcard3/server/chipcardd3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/chipcard3-config
%attr(755,root,root) %{_libdir}/libchipcard3c.so
%attr(755,root,root) %{_libdir}/libchipcard3d.so
%attr(755,root,root) %{_libdir}/libchipcard3_ctapi.so
%{_libdir}/libchipcard3c.la
%{_libdir}/libchipcard3d.la
%{_libdir}/libchipcard3_ctapi.la
%{_includedir}/chipcard3
%{_aclocaldir}/chipcard3.m4
