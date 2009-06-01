%define major		1
%define libname		%mklibname %name %major
%define libplus_major	2
%define libplus		%mklibname mlt++ %libplus_major
%define libnamedev	%mklibname %name -d

%define use_mmx	0
%{?_with_mmx: %global use_mmx 1}
%{?_without_mmx: %global use_mmx 0}

Name: mlt
Version: 0.4.2
Release: %mkrel 1
Summary: Mutton Lettuce Tomato Nonlinear Video Editor
Source0: http://ovh.dl.sourceforge.net/sourceforge/mlt/%name-%version.tar.gz
Patch0: mlt-0.3.8-fix-underlink.patch
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
BuildRequires: qt4-devel
BuildRequires:  quicktime-devel
BuildRequires:	SDL-devel
BuildRequires:	imagemagick
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

%description -n %{libname}
This package contains the libraries needed to run programs dynamically
linked with mlt.

%package -n	%{libplus}
Summary:	Main library for mlt++
Group:		System/Libraries

%description -n	%{libplus}
This package contains the libraries needed to run programs dynamically
linked with mlt++.

%package -n     %{libnamedev}
Summary:        Headers for developing programs that will use mlt
Group:          Development/C
Requires:       %{libname} = %{version}
# mlt-config requires stuff from %{_datadir}/%{name}
Requires:	%{name} = %{version}
Provides:       %{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname -d %name 0.3.0
Obsoletes:	%mklibname -d %name 0.2.2
Obsoletes:	%{_lib}mlt++-devel < 0.4.0

%description -n %{libnamedev}
This package contains the headers that programmers will need to develop
applications which will use mlt.


%prep
%setup -q -n %name-%version
%patch0 -p0 -b .underlink

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
	--qimage-libdir=%{qt4lib} \
	--qimage-includedir=%{qt4include} \

%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

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
%{_bindir}/melt
%{_datadir}/mlt
%{_libdir}/mlt

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libmlt.so.%{major}*
%{_libdir}/libmlt.so.%{version}

%files -n %{libplus}
%defattr(-,root,root)
%{_libdir}/libmlt++.so.%{libplus_major}*
%{_libdir}/libmlt++.so.%{version}

%files -n %{libnamedev}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
