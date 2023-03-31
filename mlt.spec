%define major 7
%define plusmaj %{major}
%define libname %mklibname %{name}-%{major} %{major}
%define libplus %mklibname mlt++-%{major} %{plusmaj}
%define devname %mklibname %{name} -d
%define _disable_lto 1
%global optflags %{optflags} -O3

Summary:	Media Lovin' Toolkit nonlinear video editing library
Name:		mlt
Version:	7.12.0
Release:	2
License:	LGPLv2+
Group:		Video
Url:		http://mltframework.org/
Source0:	https://github.com/mltframework/mlt/releases/download/v%{version}/mlt-%{version}.tar.gz
#Patch0:		mlt-6.24.0-opencv-4.5.patch

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
BuildRequires:	pkgconfig(rtaudio)
BuildRequires:	cmake(Qt6)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Core5Compat)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6OpenGL)
BuildRequires:	cmake(Qt6Svg)
BuildRequires:	cmake(Qt6SvgWidgets)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(Qt6Xml)
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
BuildRequires:	pkgconfig(opencv4)
BuildRequires:	pkgconfig(xkbcommon-x11)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(libarchive)
BuildRequires:	cmake ninja
# For python-bindings
BuildRequires:	swig
BuildRequires:	pkgconfig(python3)
# For ruby bindings
BuildRequires:	pkgconfig(ruby)

%description
MLT is an open source multimedia framework, designed and developed for
television broadcasting.

It provides a toolkit for broadcasters, video editors, media players,
transcoders, web streamers and many more types of applications. The
functionality of the system is provided via an assortment of ready to
use tools, xml authoring components, and an extendible plug-in based
API.

%files
%doc docs COPYING
%{_bindir}/melt
%{_bindir}/melt-%{major}
%{_datadir}/mlt-%{major}
%{_libdir}/mlt-%{major}
%{_mandir}/man1/melt-%{major}.1*

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Main library for mlt
Group:		System/Libraries

%description -n %{libname}
This package contains the libraries needed to run programs dynamically
linked with mlt.

%files -n %{libname}
%{_libdir}/libmlt-%{major}.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libplus}
Summary:	Main library for mlt++
Group:		System/Libraries

%description -n %{libplus}
This package contains the libraries needed to run programs dynamically
linked with mlt++.

%files -n %{libplus}
%{_libdir}/libmlt++-%{major}.so.%{plusmaj}*
%if "%{plusmaj}" != "%{major}"
%{_libdir}/libmlt++-%{major}.so.%{major}*
%endif

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
%{_libdir}/cmake/Mlt%{major}

#----------------------------------------------------------------------------

%package -n python-%{name}
Summary:	Python bindings for MLT
Group:		Development/Python
Requires:	python
Requires:	%{name} = %{EVRD}

%description -n python-%{name}
This module allows to work with MLT using python.

%files -n python-%{name}
%{py_platsitedir}/%{name}%{major}.p*
%{py_platsitedir}/_%{name}%{major}.so

#----------------------------------------------------------------------------

%package -n ruby-%{name}
Summary:	Ruby bindings for MLT
Group:		Development/Ruby
Requires:	ruby
Requires:	%{name} = %{EVRD}

%description -n ruby-%{name}
This module allows to work with MLT using ruby.

%files -n ruby-%{name}
%{_libdir}/ruby/vendor_ruby/mlt.so

#----------------------------------------------------------------------------

%prep
%autosetup -p1
%ifarch %{ix86}
# Workaround for compile failure with clang 7.0.0-0.333395.1
export CC=gcc
export CXX=g++
%endif
%cmake \
	-DGPL:BOOL=ON \
	-DGPL3:BOOL=ON \
	-DMOD_OPENCV:BOOL=ON \
	-DSWIG_PYTHON:BOOL=ON \
	-DSWIG_RUBY:BOOL=ON \
	-DMOD_GLAXNIMATE:BOOL=ON \
	-DMOD_QT6:BOOL=ON \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build
#install -d %{buildroot}%{py_platsitedir}
#install -pm 0644 src/swig/python/%{name}.py* %{buildroot}%{py_platsitedir}/
#install -pm 0755 src/swig/python/_%{name}.so %{buildroot}%{py_platsitedir}/
