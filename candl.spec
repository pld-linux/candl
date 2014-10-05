Summary:	Candl - Data Dependence Analysis Tool in the Polyhedral Model
Summary(pl.UTF-8):	Candl - narzędzie do analizy zależności danych w modelu wielościennym
Name:		candl
Version:	0.6.2
%define	snap	20140806
Release:	1.%{snap}.1
License:	LGPL v3+
Group:		Libraries
Source0:	http://web.cse.ohio-state.edu/~pouchet/software/pocc/download/modules/%{name}-%{version}.tar.gz
# Source0-md5:	4e86392fa46a514b03532f93d9c83f8d
# git clone git://repo.or.cz/candl.git
# git diff 0.6.2
Patch0:		%{name}-git.patch
Patch1:		%{name}-isl.patch
Patch2:		%{name}-info.patch
Patch3:		%{name}-system-libs.patch
URL:		http://icps.u-strasbg.fr/people/bastoul/public_html/development/candl/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1:1.9
BuildRequires:	gmp-devel
# 0.12.x originally, 0.13 with isl patch
BuildRequires:	isl-devel >= 0.13
BuildRequires:	libtool
BuildRequires:	osl-devel
BuildRequires:	piplib-devel
BuildRequires:	texinfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Candl (Chunky ANalyzer for Dependences in Loops) is a free software
and a library devoted to data dependences computation.

%description -l pl.UTF-8
Candl (Chunky ANalyzer for Dependences in Loops - blokowy analizator
zależności w pętlach) to wolnodostępne oprogramowanie i biblioteka
służące do obliczeń zależności danych.

%package devel
Summary:	Header files for Candl library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Candl
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gmp-devel
Requires:	isl-devel >= 0.13
Requires:	osl-devel
Requires:	piplib-devel

%description devel
Header files for Candl library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Candl.

%package static
Summary:	Static Candl library
Summary(pl.UTF-8):	Statyczna biblioteka Candl
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Candl library.

%description static -l pl.UTF-8
Statyczna biblioteka Candl.

%prep
%setup -q
# clean after make dist to allow git patch
%{__rm} include/candl/candl.h
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# because of tests subdir stripped from git patch
> tests/Makefile.am

%{__rm} osl piplib
install -d osl piplib

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--enable-mp-version \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/candl
%attr(755,root,root) %{_libdir}/libcandl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcandl.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcandl.so
%{_libdir}/libcandl.la
%{_includedir}/candl
%{_infodir}/candl.info*

%files static
%defattr(644,root,root,755)
%{_libdir}/libcandl.a
