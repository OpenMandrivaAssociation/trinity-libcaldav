%bcond clang 1

# TDE variables
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif

%define tde_pkg libcaldav
%define tde_prefix /opt/trinity

%define libname %mklibname caldav
%define devname %mklibname caldav -d

%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Version:	0.6.5
Release:	%{?tde_version:%{tde_version}_}7
Summary:	A client library that adds support for the CalDAV protocol (rfc4791)
Group:		System/Libraries
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

Source0:	https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/dependencies/%{tarball_name}-%{tde_version}.tar.xz

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
libcaldav is a client library that adds support for the CalDAV protocol (rfc4791).
The object is to have a library which fully implements the protocol so that it is
easy to integrate CalDAV support into any PIM application.

##########

%package -n %{libname}0
Summary:	A client library that adds support for the CalDAV protocol (rfc4791)
Group:		System/Libraries

%description -n %{libname}0
%summary

%files -n %{libname}0
%defattr(-,root,root,-)
%{_libdir}/libcaldav.so.0
%{_libdir}/libcaldav.so.0.0.6
%{_docdir}/libcaldav/

##########

%package -n %{devname}
Summary:	A client library that adds support for the CalDAV protocol (Development Files)
Group:		Development/Libraries/Other
Requires:	%{libname}0 = %{EVRD}
%{?libcurl_devel:Requires: %{libcurl_devel}}
Requires:	pkgconfig(glib-2.0)

Obsoletes:	trinity-libcaldav-devel < %{EVRD}

%description -n %{devname}
%summary

%files -n %{devname}
%defattr(-,root,root,-)
%{_includedir}/libcaldav/
%{_libdir}/libcaldav.la
%{_libdir}/libcaldav.so
%{_libdir}/pkgconfig/libcaldav.pc


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

