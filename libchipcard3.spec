#
# Conditional build:
%bcond_without	sysfs	# don't use sysfs to scan for ttyUSB
#
%define		beta	beta
Summary:	A library for easy access to smart cards (chipcards)
Summary(pl.UTF-8):	Biblioteka do łatwego dostępu do kart procesorowych
Name:		libchipcard
Version:	3.9.6
Release:	0.%{beta}.1
License:	GPL v2 with OpenSSL linking exception
Group:		Libraries
Source0:	http://dl.sourceforge.net/libchipcard/%{name}-%{version}%{beta}.tar.gz
# Source0-md5:	4f032f988b846adcd6c960f74a6dae1c
URL:		http://www.libchipcard.de/
BuildRequires:	gwenhywfar-devel >= 2.9.8
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

%description -l pl.UTF-8
libchipcard pozwala na łatwy dostęp do kart procesorowych. Daje
podstawowy dostęp do kart pamięciowych i procesorowych, ma także
specjalną obsługę niemieckich kart medycznych, niemieckich kart
"GeldKarte" oraz kart HBCI (do homebankingu, zarówno typu 0 jak i 1).
Z czytnikami komunikuje się poprzez interfejs CTAPI lub IFD, była
testowana z czytnikami Towitoko, Kobil, SCM, Orga, Omnikey i
Reiner-SCT. Ten pakiet zawiera demona chipcard2 potrzebnego do dostępu
do czytników kart.

%package devel
Summary:	libchipcard server development kit
Summary(pl.UTF-8):	Pliki programistyczne serwera libchipcard
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gwenhywfar-devel >= 2.3.0
Requires:	libusb-devel
%{?with_sysfs:Requires:	sysfsutils-devel >= 1.3.0-3}

%description devel
This package contains chipcard2-server-config and header files for
writing drivers, services or even your own chipcard daemon for
libchipcard.

%description devel -l pl.UTF-8
Ten pakiet zawiera skrypt chipcard2-server-config oraz pliki
nagłówkowe do pisania sterowników, usług, a nawet własnych demonów
kart dla libchipcard.

%prep
%setup -q -n %{name}-%{version}%{beta}

%build
%configure \
	%{!?with_sysfs:ac_cv_header_sysfs_libsysfs_h=no}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/gwenhywfar/plugins/*/ct/*.la
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/chipcard/client/chipcardc.conf{.default,}
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/chipcard/client/chipcardc.conf.example
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/chipcard/server/chipcardd.conf{.default,}
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/chipcard/server/chipcardd.conf.example

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO doc/{CERTIFICATES,CONFIG,IPCCOMMANDS} etc/*.conf.*
%attr(755,root,root) %{_bindir}/cardcommander
%attr(755,root,root) %{_bindir}/chipcard-tool
%attr(755,root,root) %{_bindir}/geldkarte
%attr(755,root,root) %{_bindir}/kvkcard
%attr(755,root,root) %{_bindir}/memcard
%attr(755,root,root) %{_sbindir}/chipcardd4
%attr(755,root,root) %{_libdir}/libchipcardc.so.*.*.*
%attr(755,root,root) %{_libdir}/libchipcardd.so.*.*.*
%attr(755,root,root) %{_libdir}/libchipcard_ctapi.so.*.*.*
%dir %{_libdir}/chipcard
%dir %{_libdir}/chipcard/server
%dir %{_libdir}/chipcard/server/drivers
%{_libdir}/chipcard/server/drivers/*.xml
%attr(755,root,root) %{_libdir}/chipcard/server/drivers/SKEL1
%attr(755,root,root) %{_libdir}/chipcard/server/drivers/ctapi
%attr(755,root,root) %{_libdir}/chipcard/server/drivers/ifd
%dir %{_libdir}/chipcard/server/lowlevel
%dir %{_libdir}/chipcard/server/services
%{_libdir}/chipcard/server/services/*.xml
%attr(755,root,root) %{_libdir}/chipcard/server/services/kvks
%attr(755,root,root) %{_libdir}/gwenhywfar/plugins/*/ct/*.so*
%{_libdir}/gwenhywfar/plugins/*/ct/*.xml
%dir %{_datadir}/chipcard
%dir %{_datadir}/chipcard/client
%{_datadir}/chipcard/client/apps
%{_datadir}/chipcard/client/cards
%dir %{_datadir}/chipcard/server
%{_datadir}/chipcard/server/drivers
%dir %{_sysconfdir}/chipcard
%dir %{_sysconfdir}/chipcard/client
%dir %{_sysconfdir}/chipcard/client/certs
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/chipcard/client/chipcardc.conf
%dir %{_sysconfdir}/chipcard/server
%dir %{_sysconfdir}/chipcard/server/certs
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/chipcard/server/chipcardd.conf
# XXX: move to rc.d/init.d?
%attr(754,root,root) %{_sysconfdir}/init.d/chipcardd

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/chipcard-config
%attr(755,root,root) %{_libdir}/libchipcardc.so
%attr(755,root,root) %{_libdir}/libchipcardd.so
%attr(755,root,root) %{_libdir}/libchipcard_ctapi.so
%{_libdir}/libchipcardc.la
%{_libdir}/libchipcardd.la
%{_libdir}/libchipcard_ctapi.la
%{_includedir}/chipcard
%{_aclocaldir}/chipcard.m4
