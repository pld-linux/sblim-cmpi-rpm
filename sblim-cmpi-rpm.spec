Summary:	SBLIM CMPI RPM provider
Summary(pl.UTF-8):	Dostawca danych RPM dla SBLIM CMPI
Name:		sblim-cmpi-rpm
Version:	1.0.1
Release:	1
License:	CPL v1.0
Group:		Libraries
Source0:	http://downloads.sourceforge.net/sblim/%{name}-%{version}.tar.bz2
# Source0-md5:	5a6ebb04abe884b51416054e97777d64
Patch0:		%{name}-link.patch
URL:		http://sblim.sourceforge.net/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	rpm-devel >= 4
BuildRequires:	sblim-cmpi-base-devel
BuildRequires:	sblim-cmpi-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	sblim-cmpi-base
Requires:	sblim-sfcb
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SBLIM CMPI RPM providers for system-related CIM classes.

%description -l pl.UTF-8
Dostawcy informacji RPM dla klas systemowych CIM dla SBLIM CMPI.

%package libs
Summary:	SBLIM RPM instrumentation library
Summary(pl.UTF-8):	Biblioteka pomiarowa SBLIM RPM
Group:		Libraries

%description libs
SBLIM RPM instrumentation library.

%description libs -l pl.UTF-8
Biblioteka pomiarowa SBLIM RPM.

%package devel
Summary:	Header files for SBLIM RPM instrumentation library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki pomiarowej SBLIM RPM
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	rpm-devel >= 4

%description devel
Header files for SBLIM RPM instrumentation library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki pomiarowej SBLIM RPM.

%package static
Summary:	Static SBLIM RPM instrumentation library
Summary(pl.UTF-8):	Statyczna biblioteka pomiarowa SBLIM RPM
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static SBLIM RPM instrumentation library.

%description static -l pl.UTF-8
Statyczna biblioteka pomiarowa SBLIM RPM.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	CIMSERVER=sfcb \
	PROVIDERDIR=%{_libdir}/cmpi

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

# modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/cmpi/lib*.{la,a}
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_datadir}/%{name}/provider-register.sh \
	-r %{_datadir}/%{name}/Linux_RpmPackage.registration \
	-m %{_datadir}/%{name}/Linux_RpmPackage.mof >/dev/null

%preun
if [ "$1" = "0" ]; then
	%{_datadir}/%{name}/provider-register.sh -d \
		-r %{_datadir}/%{name}/Linux_RpmPackage.registration \
		-m %{_datadir}/%{name}/Linux_RpmPackage.mof >/dev/null
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/cmpi/libcmpiOSBase_RpmAssociatedFileProvider.so*
%attr(755,root,root) %{_libdir}/cmpi/libcmpiOSBase_RpmFileCheckProvider.so*
%attr(755,root,root) %{_libdir}/cmpi/libcmpiOSBase_RpmPackageProvider.so*
%dir %{_datadir}/sblim-cmpi-rpm
%{_datadir}/sblim-cmpi-rpm/Linux_RpmPackage.mof
%{_datadir}/sblim-cmpi-rpm/Linux_RpmPackage.registration
%attr(755,root,root) %{_datadir}/sblim-cmpi-rpm/provider-register.sh

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcimrpm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcimrpm.so.0
%attr(755,root,root) %{_libdir}/libcimrpmv4.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcimrpmv4.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcimrpm.so
%attr(755,root,root) %{_libdir}/libcimrpmv4.so
%{_libdir}/libcimrpm.la
%{_libdir}/libcimrpmv4.la
# XXX: shared dir
%dir %{_includedir}/sblim
%{_includedir}/sblim/cimrpm.h
%{_includedir}/sblim/cimrpmfp.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libcimrpm.a
%{_libdir}/libcimrpmv4.a
