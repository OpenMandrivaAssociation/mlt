%define major 6
%define plusmaj 3
%define libname %mklibname %{name} %{major}
%define libplus %mklibname mlt++ %{plusmaj}
%define devname %mklibname %{name} -d
%define _disable_lto 1
%global optflags %{optflags} -O3

Summary:	Media Lovin' Toolkit nonlinear video editing library
Name:		mlt
Version:	6.20.0
Release:	2
License:	LGPLv2+
Group:		Video
Url:		http://mlt.sourceforge.net
Source0:	http://downloads.sourceforge.net/project/mlt/mlt/%{name}-%{version}.tar.gz
#Patch0:		mlt-6.14.0-fix-python3-detect.patch
#Patch2:		mlt-inline-asm-lto.patch
Patch0:		mlt-6.20.0-qt-5.15.patch
BuildRequires:	imagemagick
BuildRequires:	ffmpeg
BuildRequires:	ffmpeg-devel
BuildRequires:	ladspa-devel
BuildRequires:	qmake5
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5OpenGL)
BuildRequires:	pkgconfig(Qt5Svg)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5Xml)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(libexif)
BuildRequires:	pkgconfig(eigen3)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(epoxy)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(frei0r)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libdv)
BuildRequires:	pkgconfig(libquicktime)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(movit)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(sox)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(opencv)
# For python-bindings
BuildRequires:	swig
BuildRequires:	pkgconfig(python2)
BuildRequires:	pkgconfig(python3)

%description
MLT is an open source multimedia framework, designed and developed for
television broadcasting.

It provides a toolkit for broadcasters, video editors, media players,
transcoders, web streamers and many more types of applications. The
functionality of the system is provided via an assortment of ready to
use tools, xml authoring components, and an extendible plug-in based
API.

%files
%doc docs COPYING README
%{_bindir}/melt
%{_datadir}/mlt
%{_libdir}/mlt

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Main library for mlt
Group:		System/Libraries

%description -n %{libname}
This package contains the libraries needed to run programs dynamically
linked with mlt.

%files -n %{libname}
%{_libdir}/libmlt.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libplus}
Summary:	Main library for mlt++
Group:		System/Libraries

%description -n %{libplus}
This package contains the libraries needed to run programs dynamically
linked with mlt++.

%files -n %{libplus}
%{_libdir}/libmlt++.so.%{plusmaj}*
%{_libdir}/libmlt++.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Headers for developing programs that will use mlt
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{libplus} = %{EVRD}
# mlt-config requires stuff from %{_datadir}/%{name}
Requires:	%{name} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
This package contains the headers that programmers will need to develop
applications which will use mlt.

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

#----------------------------------------------------------------------------

%package -n python-%{name}
Summary:	Python bindings for MLT
Group:		Development/Python
Requires:	python
Requires:	%{name} = %{EVRD}

%description -n python-%{name}
This module allows to work with MLT using python.

%files -n python-%{name}
%{py_platsitedir}/%{name}.p*
%{py_platsitedir}/_%{name}.so
%{py_platsitedir}/__pycache__/*

#----------------------------------------------------------------------------

%package -n python2-%{name}
Summary:	Python 2.x bindings for MLT
Group:		Development/Python
Requires:	python2
Requires:	%{name} = %{EVRD}

%description -n python2-%{name}
This module allows to work with MLT using python2.

%files -n python2-%{name}
%{py2_platsitedir}/%{name}.p*
%{py2_platsitedir}/_%{name}.so

#----------------------------------------------------------------------------

%prep
%autosetup -p1

%build
# Don't overoptimize (breaks debugging)
sed -i -e '/fomit-frame-pointer/d' configure
sed -i -e '/ffast-math/d' configure
sed -i -e 's|qmake|qmake-qt5|' src/modules/qt/configure

%ifarch %{ix86}
# Workaround for compile failure with clang 7.0.0-0.333395.1
export CC=gcc
export CXX=g++
%endif
CXXFLAGS="%{optflags} -std=gnu++14" %configure \
	--disable-debug \
	--enable-gpl \
	--enable-gpl3 \
	--enable-opengl \
	--enable-opencv \
%ifarch %{x86_64}
	--enable-mmx \
	--enable-sse \
	--enable-sse2 \
%else
	--disable-mmx \
	--disable-sse \
	--disable-sse2 \
%endif
	--luma-compress \
	--enable-avformat \
	--avformat-shared=%{_prefix} \
	--avformat-swscale \
	--enable-motion-est \
	--qt-libdir=%{_qt5_libdir} \
	--qt-includedir=%{_qt5_includedir} \
	--swig-languages='python'

%make_build

%install
%make_install
install -d %{buildroot}%{py_platsitedir}
install -pm 0644 src/swig/python/%{name}.py* %{buildroot}%{py_platsitedir}/
install -pm 0755 src/swig/python/_%{name}.so %{buildroot}%{py_platsitedir}/

# Build python2 version as well... Too much legacy cruft out there
cd src/swig/python
sed -i -e 's,python -c,python2 -c,g;s,python-config,python2-config,g;s,dm,d,g' build
./build CXX=%{__cxx} CXXFLAGS="%{optflags}"
cd ../../..

install -d %{buildroot}%{py2_platsitedir}
install -pm 0644 src/swig/python/%{name}.py* %{buildroot}%{py2_platsitedir}/
install -pm 0755 src/swig/python/_%{name}.so %{buildroot}%{py2_platsitedir}/
