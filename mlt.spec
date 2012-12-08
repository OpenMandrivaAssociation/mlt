%define major		5
%define libname		%mklibname %{name} %{major}
%define libplus_major	3
%define libplus		%mklibname mlt++ %{libplus_major}
%define libnamedev	%mklibname %{name} -d

%define use_mmx		0

%{?_with_mmx: %global use_mmx 1}
%{?_without_mmx: %global use_mmx 0}

Name:		mlt
Version:	0.8.2
Release:	1
Summary:	Media Lovin' Toolkit nonlinear video editing library
License:	LGPLv2+
Group:		Video
Url:		http://mlt.sourceforge.net
Source0:	http://downloads.sourceforge.net/project/mlt/mlt/%{name}-%{version}.tar.gz
Patch0:		mlt-0.7.6-fix-used-symbols.patch
# from upstream
Patch1:		mlt-0.8.2-ffmpeg1.0.patch
BuildRequires:	imagemagick
BuildRequires:	multiarch-utils >= 1.0.3
BuildRequires:	ffmpeg
BuildRequires:	ffmpeg-devel
BuildRequires:	ladspa-devel
BuildRequires:	qt4-devel
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libdv)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(libquicktime)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(sox)

# For python-bindings

BuildRequires:	swig
BuildRequires:	python-devel

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

%package -n %{libnamedev}
Summary:	Headers for developing programs that will use mlt
Group:		Development/C
Requires:	%{libname} = %{version}
Requires:	%{libplus} = %{version}
# mlt-config requires stuff from %{_datadir}/%{name}
Requires:	%{name} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n %{libnamedev}
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
%patch0 -p1
%patch1 -p1

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
%{_libdir}/libmlt++.so.%{libplus_major}*
%{_libdir}/libmlt++.so.%{version}

%files -n %{libnamedev}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files -n python-%{name}
%{py_platsitedir}/%{name}.p*
%{py_platsitedir}/_%{name}.so

%changelog
* Mon Jun 25 2012 Andrey Bondrov <andrey.bondrov@rosalab.ru> 0.8.0-3
- Drop useless Obsoletes
- Spec cleanup

* Fri Jun 08 2012 Bernhard Rosenkraenzer <bero@bero.eu> 0.8.0-2
+ Revision: 803454
- Rebuild to pick up libsox.so.2

* Fri Jun 08 2012 Bernhard Rosenkraenzer <bero@bero.eu> 0.8.0-1
+ Revision: 803405
- Update to 0.8.0
- Build for ffmpeg 0.11.x

* Mon Feb 27 2012 Alexander Khrukin <akhrukin@mandriva.org> 0.7.8-1
+ Revision: 780991
- version update 0.7.8

* Sat Nov 19 2011 Александр Казанцев <kazancas@mandriva.org> 0.7.6-1
+ Revision: 731800
- drop frei0r-plugins due adding to need videoeditor
- update to 0.7.6
- add BR frei0r-plugins needing by openshot

* Wed Apr 27 2011 Funda Wang <fwang@mandriva.org> 0.7.0-1
+ Revision: 659690
- new version 0.7.0

* Thu Nov 04 2010 Götz Waschk <waschk@mandriva.org> 0.5.10-2mdv2011.0
+ Revision: 593364
- rebuild for new python 2.7

* Wed Sep 15 2010 Funda Wang <fwang@mandriva.org> 0.5.10-1mdv2011.0
+ Revision: 578422
- new version 0.5.10

* Sat Aug 07 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.5.6-1mdv2011.0
+ Revision: 567229
- update to 0.5.6

* Tue Feb 16 2010 Frederik Himpe <fhimpe@mandriva.org> 0.5.0-1mdv2010.1
+ Revision: 506848
- update to new version 0.5.0

* Wed Jan 13 2010 Stéphane Téletchéa <steletch@mandriva.org> 0.4.10-3mdv2010.1
+ Revision: 490979
- Adjust python path in the files section
- Add python bindings
- Add missing ogg BR
- Add conditional build for MMX and SSE support
- Small indentation fixes
- Update configure parameters

* Thu Dec 10 2009 Frederik Himpe <fhimpe@mandriva.org> 0.4.10-1mdv2010.1
+ Revision: 476119
- update to new version 0.4.10

* Fri Oct 09 2009 Funda Wang <fwang@mandriva.org> 0.4.6-1mdv2010.0
+ Revision: 456244
- New version 0.4.6

* Sat Jul 04 2009 Frederik Himpe <fhimpe@mandriva.org> 0.4.4-1mdv2010.0
+ Revision: 392365
- update to new version 0.4.4

* Mon Jun 01 2009 Funda Wang <fwang@mandriva.org> 0.4.2-2mdv2010.0
+ Revision: 381769
- fix requires

* Mon Jun 01 2009 Funda Wang <fwang@mandriva.org> 0.4.2-1mdv2010.0
+ Revision: 381761
- New version 0.4.2

* Fri May 01 2009 Funda Wang <fwang@mandriva.org> 0.3.8-1mdv2010.0
+ Revision: 369393
- try to simplify underlink patch
- New version 0.3.8

* Tue Feb 03 2009 Funda Wang <fwang@mandriva.org> 0.3.6-1mdv2009.1
+ Revision: 336764
- New version 0.3.6

* Wed Dec 31 2008 Funda Wang <fwang@mandriva.org> 0.3.4-1mdv2009.1
+ Revision: 321589
- rediff noO3 patch
- New version 0.3.4
- drop sox patch (merged upstream)
- disable ppc patch (we do not support it officially)

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Mon Nov 17 2008 Funda Wang <fwang@mandriva.org> 0.3.2-2mdv2009.1
+ Revision: 303891
- add sox 14.2.0 patch from upstream

* Tue Nov 11 2008 Funda Wang <fwang@mandriva.org> 0.3.2-1mdv2009.1
+ Revision: 302079
- New version 0.3.2

* Tue Oct 14 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.1-0.svn1184.1mdv2009.1
+ Revision: 293781
- bump snapshot to fix build with latest ffmpeg
- rebuild for new ffmpeg major

* Wed Sep 10 2008 Stéphane Téletchéa <steletch@mandriva.org> 0.3.1-0.svn1180.3mdv2009.0
+ Revision: 283525
- re-enabling sox, it works correctly now

* Tue Sep 09 2008 Stéphane Téletchéa <steletch@mandriva.org> 0.3.1-0.svn1180.2mdv2009.0
+ Revision: 283342
- update Obsoletes to ease migration from previous release

* Tue Sep 09 2008 Stéphane Téletchéa <steletch@mandriva.org> 0.3.1-0.svn1180.1mdv2009.0
+ Revision: 283341
- update to latest svn revision
- fix the svn case for a smoother upgrade
- update to latest svn revision to build a working kdenlive

* Wed Sep 03 2008 Helio Chissini de Castro <helio@mandriva.com> 0.3.0-2mdv2009.0
+ Revision: 279971
- We have qt4 in main and kdenlive is qt4, so make library qt3 not helps in any way. This fix startup crashes on kdenlive
- Clean the redefinitions in spec
- Kill all hack to enable and patch and disable and buildconflicts where just a --disable-sox would work

* Wed Aug 06 2008 Funda Wang <fwang@mandriva.org> 0.3.0-1mdv2009.0
+ Revision: 264227
- add sox detection patch
- disable sox build as mlt 0.3 does not like sox 14.1
- more underlink patch
- update libmajor
- New version 0.3.0
- apply underlink patch
- fix under llink

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sat Feb 02 2008 Austin Acton <austin@mandriva.org> 0.2.5-0.20080123.2mdv2008.1
+ Revision: 161308
- rebuild for new libsox

* Wed Jan 23 2008 Giuseppe Ghibò <ghibo@mandriva.com> 0.2.5-0.20080123.1mdv2008.1
+ Revision: 156997
- Update to mlt svn 20080123 (for bug #36896).

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Nov 19 2007 Adam Williamson <awilliamson@mandriva.org> 0.2.4-3mdv2008.1
+ Revision: 110562
- buildrequires libjack-devel (#33601)

* Wed Sep 05 2007 Funda Wang <fwang@mandriva.org> 0.2.4-2mdv2008.0
+ Revision: 80185
- Obsoletes old devel package

* Sun Aug 12 2007 Funda Wang <fwang@mandriva.org> 0.2.4-1mdv2008.0
+ Revision: 62171
- drop patch5, not needed
- drop patch4, merged upstream
- Drop patch3, merged upstream
- New version 0.2.4


* Tue Mar 13 2007 Giuseppe Ghibò <ghibo@mandriva.com> 0.2.2-9mdv2007.1
+ Revision: 142397
- Rebuilt against latest ffmpeg.

* Mon Mar 12 2007 Giuseppe Ghibò <ghibo@mandriva.com> 0.2.2-8mdv2007.1
+ Revision: 141637
- Don't revert gb PPC patch.
- Better handling of avformat-swscale (for now disabled).

* Sun Mar 11 2007 Giuseppe Ghibò <ghibo@mandriva.com> 0.2.2-7mdv2007.1
+ Revision: 141361
- Unbzip2 patches.
- Added Patch3 from cvs (fix motion-est for x86_64).
- Added Patch4 to build with sox 13 (fix bug #29207).
- Added Patch5 (to enable --avformat-swscale).

  + Gwenole Beauchesne <gbeauchesne@mandriva.com>
    - lib{32,64} fixes

* Mon Dec 18 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.2.2-6mdv2007.1
+ Revision: 98492
- fix patch2: enable SSE optimizations for x86-64
- drop BuildRequires libavifile-devel (not used)
- patch2: fix build on ppc

* Mon Oct 30 2006 Anssi Hannula <anssi@mandriva.org> 0.2.2-5mdv2007.1
+ Revision: 73837
- buildrequires mad-devel
- buildrequires ImageMagick
- rebuild
- drop unused plf build switch
  fix invalid provides of libpackage
  fix requires of devel package

  + Andreas Hasenack <andreas@mandriva.com>
    - commit on behalf of Giuseppe Ghib?\195?\178 to get package in sync with svn:
      * Wed Sep 13 2006 Giuseppe Ghib?\195?\178 <ghibo@mandriva.com> 0.2.2-2mdv2007.0
      - Fix build for X86_64.
      - Fixed License.
      - Removed suffix in configure, so to let modules avformat built.

  + Jerome Martin <jmartin@mandriva.org>
    - import mlt-0.2.2-0.1.20060mdk

* Wed Jun 21 2006 Jerome Martin <jmartin@mandriva.org> 0.2.2-1
- Initial version

