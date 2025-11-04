%define major 7
%define plusmaj %{major}
%define libname %mklibname %{name}-%{major} %{major}
%define libplus %mklibname mlt++-%{major} %{plusmaj}
%define devname %mklibname %{name} -d
%define _disable_lto 1
%global optflags %{optflags} -O3
%global build_ldflags %{build_ldflags} -Wl,--undefined-version

Summary:	Media Lovin' Toolkit nonlinear video editing library
Name:		mlt
Version:	7.34.0
Release:	1
License:	LGPLv2+
Group:		Video
Url:		https://mltframework.org/
Source0:	https://github.com/mltframework/mlt/releases/download/v%{version}/mlt-%{version}.tar.gz

BuildRequires:	clang-tools
BuildRequires:	imagemagick
BuildRequires:	ffmpeg
BuildRequires:	ffmpeg-devel
BuildRequires:	ladspa-devel
BuildRequires:	qmake5
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Network)
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
BuildRequires:	cmake(Qt6Network)
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
BuildRequires:	pkgconfig(libebur128)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(movit)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(sox)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(opencv4)
BuildRequires:	pkgconfig(xkbcommon-x11)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(libarchive)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(rubberband)
BuildRequires:	pkgconfig(vidstab)
BuildRequires:	pkgconfig(lua)
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
%dir %{_datadir}/mlt-%{major}
%{_datadir}/mlt-%{major}/avformat
%{_datadir}/mlt-%{major}/chain_normalizers.ini
%{_datadir}/mlt-%{major}/core
%{_datadir}/mlt-%{major}/decklink
%{_datadir}/mlt-%{major}/frei0r
%{_datadir}/mlt-%{major}/jackrack
%{_datadir}/mlt-%{major}/metaschema.yaml
%{_datadir}/mlt-%{major}/movit
%{_datadir}/mlt-%{major}/normalize
%{_datadir}/mlt-%{major}/oldfilm
%{_datadir}/mlt-%{major}/plus
%{_datadir}/mlt-%{major}/plusgpl
%{_datadir}/mlt-%{major}/presets
%{_datadir}/mlt-%{major}/profiles
%{_datadir}/mlt-%{major}/resample
%{_datadir}/mlt-%{major}/rtaudio
%{_datadir}/mlt-%{major}/rubberband
%{_datadir}/mlt-%{major}/vid.stab
%{_datadir}/mlt-%{major}/vorbis
%{_datadir}/mlt-%{major}/xml
%dir %{_libdir}/mlt-%{major}
%{_libdir}/mlt-%{major}/libmltladspa.so
%{_libdir}/mlt-%{major}/libmltavformat.so
%{_libdir}/mlt-%{major}/libmltcore.so
%{_libdir}/mlt-%{major}/libmltdecklink.so
%{_libdir}/mlt-%{major}/libmltfrei0r.so
%{_libdir}/mlt-%{major}/libmltjackrack.so
%{_libdir}/mlt-%{major}/libmltmovit.so
%{_libdir}/mlt-%{major}/libmltnormalize.so
%{_libdir}/mlt-%{major}/libmltoldfilm.so
%{_libdir}/mlt-%{major}/libmltplus.so
%{_libdir}/mlt-%{major}/libmltplusgpl.so
%{_libdir}/mlt-%{major}/libmltresample.so
%{_libdir}/mlt-%{major}/libmltrtaudio.so
%{_libdir}/mlt-%{major}/libmltrubberband.so
%{_libdir}/mlt-%{major}/libmltvidstab.so
%{_libdir}/mlt-%{major}/libmltvorbis.so
%{_libdir}/mlt-%{major}/libmltxml.so
%{_mandir}/man1/melt-%{major}.1*

#----------------------------------------------------------------------------
%package gdk
Summary: GDK integration plugin for MLT
Requires: %{name} = %{EVRD}
Group: System/Libraries

%description gdk
GDK integration plugin for MLT

%files gdk
%{_libdir}/mlt-%{major}/libmltgdk.so
%{_datadir}/mlt-%{major}/gdk

#----------------------------------------------------------------------------
%package opencv
Summary: OpenCV integration plugin for MLT
Requires: %{name} = %{EVRD}
Group: System/Libraries

%description opencv
OpenCV integration plugin for MLT

%files opencv
%{_libdir}/mlt-%{major}/libmltopencv.so
%{_datadir}/mlt-%{major}/opencv

#----------------------------------------------------------------------------
%package sdl1
Summary: SDL 1.x integration plugin for MLT
Requires: %{name} = %{EVRD}
Group: System/Libraries

%description sdl1
SDL 1.x integration plugin for MLT

%files sdl1
%{_libdir}/mlt-%{major}/libmltsdl.so
%{_datadir}/mlt-%{major}/sdl

#----------------------------------------------------------------------------
%package sdl2
Summary: SDL 2.x integration plugin for MLT
Requires: %{name} = %{EVRD}
Group: System/Libraries

%description sdl2
SDL 2.x integration plugin for MLT

%files sdl2
%{_libdir}/mlt-%{major}/libmltsdl2.so
%{_datadir}/mlt-%{major}/sdl2

#----------------------------------------------------------------------------
%package qt5
Summary: Qt 5.x integration plugin for MLT
Requires: %{name} = %{EVRD}
Group: System/Libraries

%description qt5
Qt 5.x integration plugin for MLT

%files qt5
%{_libdir}/mlt-%{major}/libmltqt.so
%{_libdir}/mlt-%{major}/libmltglaxnimate.so
%{_libdir}/mlt-%{major}/libmltkdenlive.so
%{_datadir}/mlt-%{major}/glaxnimate
%{_datadir}/mlt-%{major}/kdenlive
%{_datadir}/mlt-%{major}/qt

#----------------------------------------------------------------------------
%package qt6
Summary: Qt 6.x integration plugin for MLT
Requires: %{name} = %{EVRD}
Group: System/Libraries

%description qt6
Qt 6.x integration plugin for MLT

%files qt6
%{_libdir}/mlt-%{major}/libmltqt6.so
%{_libdir}/mlt-%{major}/libmltglaxnimate-qt6.so
%{_datadir}/mlt-%{major}/glaxnimate-qt6
%{_datadir}/mlt-%{major}/qt6

#----------------------------------------------------------------------------
%package sox
Summary: Sox integration plugin for MLT
Requires: %{name} = %{EVRD}
Group: System/Libraries

%description sox
Sox integration plugin for MLT

%files sox
%{_libdir}/mlt-%{major}/libmltsox.so
%{_datadir}/mlt-%{major}/sox

#----------------------------------------------------------------------------
%package xine
Summary: Xine integration plugin for MLT
Requires: %{name} = %{EVRD}
Group: System/Libraries

%description xine
Xine integration plugin for MLT

%files xine
%{_libdir}/mlt-%{major}/libmltxine.so
%{_datadir}/mlt-%{major}/xine

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
	-DSWIG_LUA:BOOL=ON \
	-DSWIG_PYTHON:BOOL=ON \
	-DSWIG_RUBY:BOOL=ON \
	-DMOD_GLAXNIMATE:BOOL=ON \
	-DMOD_GLAXNIMATE_QT6:BOOL=ON \
 	-DMOD_SDL1=ON \
	-DMOD_QT:BOOL=OFF \
	-DMOD_QT6:BOOL=ON \
	-DCMAKE_CXX_STANDARD=17 -DCMAKE_CXX_FLAGS="%{optflags}" \
	-G Ninja

%build
export CXXFLAGS="%{optflags} -fpermissive"
%ninja_build -C build

%install
%ninja_install -C build
#install -d %{buildroot}%{py_platsitedir}
#install -pm 0644 src/swig/python/%{name}.py* %{buildroot}%{py_platsitedir}/
#install -pm 0755 src/swig/python/_%{name}.so %{buildroot}%{py_platsitedir}/
