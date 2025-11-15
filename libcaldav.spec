#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define tde_pkg libcaldav
%define tde_prefix /opt/trinity
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}

%if 0%{?mdkversion} || 0%{?mgaversion} || 0%{?pclinuxos}
%define libcaldav %{_lib}caldav
%else
%define libcaldav libcaldav
%endif

%if 0%{?mdkversion}
%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1
%endif

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.6.5
Release:	%{?tde_version}_%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:	A client library that adds support for the CalDAV protocol (rfc4791)
Group:		System/Libraries
URL:		http://www.trinitydesktop.org/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Source0:	https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/dependencies/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires:    cmake make

BuildRequires:	trinity-tde-cmake >= %{tde_version}
# BuildRequires:	make
BuildRequires:	libtool
BuildRequires:	fdupes

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

##########

%if 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########

%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

if ! rpm -E %%cmake|grep -e 'cd build\|cd ${CMAKE_BUILD_DIR:-build}'; then
  %__mkdir_p build
  cd build
fi

%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH=OFF \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=OFF \
  \
  -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
  -DLIB_INSTALL_DIR="%{_libdir}" \
  -DSHARE_INSTALL_PREFIX="%{_datadir}" \
  \
  -DWITH_ALL_OPTIONS=ON \
  -DWITH_GCC_VISIBILITY=ON \
  \
  -DBUILD_ALL=ON \
  -DBUILD_DOC=ON \
  -DBUILD_TRANSLATIONS=ON \
  \
  ..

%__make %{?_smp_mflags} || %__make


%install
%__make install DESTDIR=%{buildroot} -C build

# Fix duplicate files
%fdupes %{?buildroot}

# Fix doc directory
%if "%{_docdir}" != "%{_datadir}/doc"
%__mkdir_p "%{?buildroot}/%{_docdir}"
%__mv -f "%{?buildroot}/%{_datadir}/doc/libcaldav" "%{?buildroot}/%{_docdir}/libcaldav"
%endif

