%define major 1
%define libname		%mklibname %name %major
%define libnamedev	%mklibname %name -d
%define libname_orig	lib%{name}

%define use_mmx	0
%{?_with_mmx: %global use_mmx 1}
%{?_without_mmx: %global use_mmx 0}

%define useqt3 0
%{?_with_qt3: %global useqt3 1}

%define version 0.3.2
%define snapshot 0
%define rel 1

%if %snapshot
%define release %mkrel 0.svn%snapshot.%rel
%else
%define release %mkrel %rel
%endif

Name: mlt
Version: %version
Release: %release
Summary: Mutton Lettuce Tomato Nonlinear Video Editor
%if %snapshot
# http://mlt.svn.sourceforge.net/viewvc/mlt/trunk/mlt/
Source: %{name}-r%{snapshot}.tar.bz2
%else
Source0: http://ovh.dl.sourceforge.net/sourceforge/mlt/%name-%version.tar.gz
%endif

Patch0: mlt-0.3.0-fix-underlink.patch
Patch1: %{name}-0.3.2-noO3.patch
Patch2: mlt-0.2.2-linuxppc.patch
License: LGPLv2+
Group: Video
Url: http://mlt.sourceforge.net
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: pkgconfig
BuildRequires: ffmpeg
BuildRequires: ffmpeg-devel >= 0.4.9-3.pre1
BuildRequires: glib2-devel
BuildRequires: gtk2-devel
BuildRequires: ladspa-devel
BuildRequires: libdv-devel
BuildRequires: libsamplerate-devel
BuildRequires: libvorbis-devel
BuildRequires: libxml2-devel
BuildRequires: multiarch-utils >= 1.0.3
BuildRequires: pango-devel
%if %useqt3
BuildRequires:	qt3-devel
%else
BuildRequires:  qt4-devel
BuildConflicts:	qt3-devel
%endif
BuildRequires:  quicktime-devel
BuildRequires:	SDL-devel
BuildRequires:	ImageMagick
BuildRequires:	mad-devel
BuildRequires:	libjack-devel
BuildRequires:	sox-devel

%description
MLT is an open source multimedia framework, designed and developed for
television broadcasting.

It provides a toolkit for broadcasters, video editors, media players,
transcoders, web streamers and many more types of applications. The
functionality of the system is provided via an assortment of ready to
use tools, xml authoring components, and an extendible plug-in based
API.

%package -n     %{libname}
Summary:        Main library for mlt 
Group:          System/Libraries
Provides:       %{libname_orig} = %{version}-%{release}

%description -n %{libname}
This package contains the libraries needed to run programs dynamically
linked with mlt.


%package -n     %{libnamedev}
Summary:        Headers for developing programs that will use mlt
Group:          Development/C
Requires:       %{libname} = %{version}
# mlt-config requires stuff from %{_datadir}/%{name}
Requires:	%{name} = %{version}
Provides:       %{name}-devel = %{version}-%{release}
Provides:	%{libname_orig}-devel = %{version}-%{release}
Obsoletes:	%mklibname -d %name 0.3.0
Obsoletes:	%mklibname -d %name 0.2.2

%description -n %{libnamedev}
This package contains the headers that programmers will need to develop
applications which will use mlt.


%prep
%setup -q -n %name-%version
%patch0 -p0 -b .underlink
%patch1 -p1 -b .noO3
%patch2 -p1 -b .ppc

%build
%configure2_5x \
	--disable-debug \
	--enable-gpl \
%if %use_mmx
	--enable-mmx \
%else
	--disable-mmx \
%endif
	--luma-compress \
	--enable-avformat \
	--avformat-shared=%{_prefix} \
	--enable-motion-est \
%if %useqt3
	--force-qt3 \
	--qimage-libdir=%{qt3lib} \
	--qimage-includedir=%{qt3include} \
%else
	--qimage-libdir=%{qt4lib} \
	--qimage-includedir=%{qt4include} \
%endif

%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
%multiarch_binaries %{buildroot}%{_bindir}/mlt-config

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%doc docs COPYING README
%{_bindir}/albino
%{_bindir}/humperdink
%{_bindir}/inigo
%{_bindir}/miracle
%{_datadir}/*
%{_libdir}/mlt

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.%{major}*
%{_libdir}/lib*.so.%{version}

%files -n %{libnamedev}
%defattr(-,root,root)
%multiarch %{multiarch_bindir}/mlt-config
%{_bindir}/mlt-config
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
