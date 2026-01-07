%bcond clang 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%define pkg_rel 3

%endif
%define tde_pkg libcaldav
%define tde_prefix /opt/trinity


%define libcaldav %{_lib}caldav

%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.6.5
Release:	%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:	A client library that adds support for the CalDAV protocol (rfc4791)
Group:		System/Libraries
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

Source0:	https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/dependencies/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildSystem:    cmake
BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DWITH_ALL_OPTIONS=ON
BuildOption:    -DBUILD_ALL=ON -DBUILD_DOC=ON -DBUILD_TRANSLATIONS=ON 
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires:	trinity-tde-cmake >= %{tde_version}
BuildRequires:	libtool
BuildRequires:	fdupes

%{!?with_clang:BuildRequires:    gcc-c++}

# GTK2 support
BuildRequires:  pkgconfig(gtk+-2.0)

# CURL support
BuildRequires:  pkgconfig(libcurl)

%description
libcaldev is a client library that adds support for the CalDAV protocol (rfc4791).
The object is to have a library which fully implements the protocol so that it is
easy to integrate CalDAV support into any PIM application.

##########

%package -n %{libcaldav}0
Summary:	A client library that adds support for the CalDAV protocol (rfc4791)
Group:		System/Libraries

Obsoletes:	trinity-libcaldav < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	trinity-libcaldav = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	libcaldav = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{libcaldav}0
libcaldev is a client library that adds support for the CalDAV protocol (rfc4791).
The object is to have a library which fully implements the protocol so that it is
easy to integrate CalDAV support into any PIM application.

%files -n %{libcaldav}0
%defattr(-,root,root,-)
%{_libdir}/libcaldav.so.0
%{_libdir}/libcaldav.so.0.0.6
%{_docdir}/libcaldav/

%post -n %{libcaldav}0
/sbin/ldconfig

%postun -n %{libcaldav}0
/sbin/ldconfig

##########

%package -n %{libcaldav}-devel
Summary:	A client library that adds support for the CalDAV protocol (Development Files)
Group:		Development/Libraries/Other
Requires:	%{libcaldav}0 = %{?epoch:%{epoch}:}%{version}-%{release}
%{?libcurl_devel:Requires: %{libcurl_devel}}
Requires:	pkgconfig(glib-2.0)

Obsoletes:	trinity-libcaldav-devel < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	trinity-libcaldav-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	libcaldav-devel = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{libcaldav}-devel
libcaldev is a client library that adds support for the CalDAV protocol (rfc4791).
The object is to have a library which fully implements the protocol so that it is
easy to integrate CalDAV support into any PIM application. 

This package includes the development files.

%files -n %{libcaldav}-devel
%defattr(-,root,root,-)
%{_includedir}/libcaldav/
%{_libdir}/libcaldav.la
%{_libdir}/libcaldav.so
%{_libdir}/pkgconfig/libcaldav.pc

%post -n %{libcaldav}-devel
/sbin/ldconfig

%postun -n %{libcaldav}-devel
/sbin/ldconfig


%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"

%install -a
# Fix duplicate files
%fdupes %{?buildroot}

# Fix doc directory
%if "%{_docdir}" != "%{_datadir}/doc"
%__mkdir_p "%{?buildroot}/%{_docdir}"
%__mv -f "%{?buildroot}/%{_datadir}/doc/libcaldav" "%{?buildroot}/%{_docdir}/libcaldav"
%endif

