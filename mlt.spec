%define major	6
%define libname	%mklibname %{name} %{major}
%define plusmaj	3
%define libplus	%mklibname mlt++ %{plusmaj}
%define devname	%mklibname %{name} -d

%define use_mmx		0

%{?_with_mmx: %global use_mmx 1}
%{?_without_mmx: %global use_mmx 0}

Summary:	Media Lovin' Toolkit nonlinear video editing library
Name:		mlt
Version:	0.9.0
Release:	4
License:	LGPLv2+
Group:		Video
Url:		http://mlt.sourceforge.net
Source0:	http://downloads.sourceforge.net/project/mlt/mlt/%{name}-%{version}.tar.gz
Patch0:		mlt-0.7.6-fix-used-symbols.patch
BuildRequires:	imagemagick
BuildRequires:	multiarch-utils >= 1.0.3
BuildRequires:	ffmpeg
BuildRequires:	ffmpeg-devel
BuildRequires:	ladspa-devel
BuildRequires:	qt4-devel
BuildRequires:	pkgconfig(frei0r)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libdv)
BuildRequires:	pkgconfig(libquicktime)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(sox)
BuildRequires:	pkgconfig(vorbis)
# For python-bindings
BuildRequires:	swig
BuildRequires:	pkgconfig(python)

%description
MLT is an open source multimedia framework, designed and developed for
television broadcasting.

It provides a toolkit for broadcasters, video editors, media players,
transcoders, web streamers and many more types of applications. The
functionality of the system is provided via an assortment of ready to
use tools, xml authoring components, and an extendible plug-in based
API.

%package -n %{libname}
Summary:	Main library for mlt
Group:		System/Libraries

%description -n %{libname}
This package contains the libraries needed to run programs dynamically
linked with mlt.

%package -n %{libplus}
Summary:	Main library for mlt++
Group:		System/Libraries

%description -n %{libplus}
This package contains the libraries needed to run programs dynamically
linked with mlt++.

%package -n %{devname}
Summary:	Headers for developing programs that will use mlt
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libplus} = %{version}-%{release}
# mlt-config requires stuff from %{_datadir}/%{name}
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains the headers that programmers will need to develop
applications which will use mlt.

%package -n python-%{name}
Summary:	Python bindings for MLT
Group:		Development/Python
Requires:	python
Requires:	%{name} = %{version}-%{release}

%description -n python-%{name}
This module allows to work with MLT using python.

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
	--disable-debug \
	--enable-gpl \
%if %{use_mmx}
	--enable-mmx \
%else
	%ifarch x86_64
	--enable-mmx \
	--enable-sse \
	%else
	--disable-mmx \
	%endif
%endif
	--luma-compress \
	--enable-avformat \
	--avformat-shared=%{_prefix} \
	--avformat-swscale \
	--enable-motion-est \
	--qimage-libdir=%{qt4lib} \
	--qimage-includedir=%{qt4include} \
	--swig-languages='python'
%make

%install
%makeinstall_std
install -d %{buildroot}%{py_platsitedir}
install -pm 0644 src/swig/python/%{name}.py* %{buildroot}%{py_platsitedir}/
install -pm 0755 src/swig/python/_%{name}.so %{buildroot}%{py_platsitedir}/

%files
%doc docs COPYING README
%{_bindir}/melt
%{_datadir}/mlt
%{_libdir}/mlt

%files -n %{libname}
%{_libdir}/libmlt.so.%{major}*
%{_libdir}/libmlt.so.%{version}

%files -n %{libplus}
%{_libdir}/libmlt++.so.%{plusmaj}*
%{_libdir}/libmlt++.so.%{version}

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files -n python-%{name}
%{py_platsitedir}/%{name}.p*
%{py_platsitedir}/_%{name}.so

