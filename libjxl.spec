#
# Conditional build:
%bcond_with	tests	# build tests
%bcond_without	java	# JNI interface

%{?use_default_jdk}

Summary:	JPEG XL reference implementation
Summary(pl.UTF-8):	Referencyjna implementacja JPEG XL
Name:		libjxl
Version:	0.8.1
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/libjxl/libjxl/releases
Source0:	https://github.com/libjxl/libjxl/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	04a73be60211224e039d791a902a46de
Patch0:		%{name}-system-libs.patch
URL:		https://github.com/libjxl/libjxl
BuildRequires:	OpenEXR-devel
BuildRequires:	asciidoc
BuildRequires:	cmake >= 3.10
BuildRequires:	doxygen
BuildRequires:	gdk-pixbuf2-devel >= 2.38
BuildRequires:	giflib-devel >= 5
BuildRequires:	gimp-devel >= 1:2.10
%if %{with tests}
BuildRequires:	gmock-devel
BuildRequires:	google-benchmark-devel
BuildRequires:	gtest-devel
%endif
BuildRequires:	highway-devel >= 0.15.0
%{?with_java:%buildrequires_jdk}
%{?with_java:%{?use_jdk:BuildRequires:  %{use_jdk}-jre-base-X11}}
BuildRequires:	lcms2-devel >= 2.10
BuildRequires:	libavif-devel
BuildRequires:	libbrotli-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libwebp-devel
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	lodepng-devel
BuildRequires:	pkgconfig
BuildRequires:	python3-devel >= 1:3
BuildRequires:	rpmbuild(macros) >= 2.021
# for gdk-pixbuf loader only (the rest uses lcms2 by default)
BuildRequires:	skcms-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if "%{_lib}" != "lib"
%define		libext		%(lib="%{_lib}"; echo ${lib#lib})
%define		pqext		-%{libext}
%else
%define		pqext		%{nil}
%endif

%description
JPEG XL reference implementation.

%description -l pl.UTF-8
Referencyjna implementacja JPEG XL.

%package tools
Summary:	Tools to encode and decode JPEG XL files
Summary(pl.UTF-8):	Narzędzia do kodowania i dekodowania plików JPEG XL
Group:		Applications/Graphics
Requires:	%{name} = %{version}-%{release}

%description tools
Tools to encode and decode JPEG XL files.

%description tools -l pl.UTF-8
Narzędzia do kodowania i dekodowania plików JPEG XL.

%package devel
Summary:	Header files for JXL libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek JXL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	highway-devel >= 0.15.0
Requires:	lcms2-devel >= 2.10
Requires:	libbrotli-devel
Requires:	libstdc++-devel >= 6:7

%description devel
Header files for JXL libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek JXL.

%package static
Summary:	Static JXL libraries
Summary(pl.UTF-8):	Statyczne biblioteki JXL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static JXL libraries.

%description static -l pl.UTF-8
Statyczne biblioteki JXL.

%package -n java-libjxl
Summary:	JNI interface for JXL library
Summary(pl.UTF-8):	Interfejs JNI do biblioteki JXL
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}

%description -n java-libjxl
JNI interface for JXL library.

%description -n java-libjxl -l pl.UTF-8
Interfejs JNI do biblioteki JXL.

%package -n gdk-pixbuf2-loader-jxl
Summary:	JPEG XL loader module for gdk-pixbuf2 library
Summary(pl.UTF-8):	Moduł biblioteki gdk-pixbuf2 wczytujący pliki JPEG XL
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gdk-pixbuf2 >= 2.38
Requires:	shared-mime-info

%description -n gdk-pixbuf2-loader-jxl
JPEG XL loader module for gdk-pixbuf2 library.

%description -n gdk-pixbuf2-loader-jxl -l pl.UTF-8
Moduł biblioteki gdk-pixbuf2 wczytujący pliki JPEG XL.

%package -n gimp-plugin-jxl
Summary:	JPEG XL load/save plugin for GIMP
Summary(pl.UTF-8):	Wtyczka wczytująca/zapisująca pliki JPEG XL dla GIMP-a
Group:		Applications/Graphics
Requires:	%{name} = %{version}-%{release}
Requires:	gimp >= 1:2.10

%description -n gimp-plugin-jxl
JPEG XL load/save plugin for GIMP.

%description -n gimp-plugin-jxl -l pl.UTF-8
Wtyczka wczytująca/zapisująca pliki JPEG XL dla GIMP-a.

%prep
%setup -q
%patch0 -p1

%build
export JAVA_HOME="%{java_home}"
install -d build
cd build
%cmake .. \
	%{cmake_on_off tests BUILD_TESTING} \
	%{!?with_java:-DJPEGXL_ENABLE_JNI=OFF} \
	-DJPEGXL_ENABLE_PLUGINS=ON \
	-DJPEGXL_ENABLE_SJPEG=OFF \
	-DJPEGXL_ENABLE_SKCMS=OFF \
	-DJPEGXL_ENABLE_TCMALLOC=OFF \
	-DJPEGXL_FORCE_SYSTEM_BROTLI=ON \
	-DJPEGXL_FORCE_SYSTEM_GTEST=ON \
	-DJPEGXL_FORCE_SYSTEM_HWY=ON \
	-DJPEGXL_INSTALL_JARDIR=%{_javadir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n gdk-pixbuf2-loader-jxl
umask 022
%{_bindir}/gdk-pixbuf-query-loaders%{pqext} --update-cache || :
%update_mime_database

%postun	-n gdk-pixbuf2-loader-jxl
%update_mime_database
if [ "$1" != "0" ]; then
	umask 022
	[ ! -x %{_bindir}/gdk-pixbuf-query-loaders%{pqext} ] || \
	%{_bindir}/gdk-pixbuf-query-loaders%{pqext} --update-cache || :
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG.md CONTRIBUTORS LICENSE PATENTS README.md SECURITY.md doc/xl_overview.md
%attr(755,root,root) %{_libdir}/libjxl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjxl.so.0.8
%attr(755,root,root) %{_libdir}/libjxl_threads.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjxl_threads.so.0.8

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/benchmark_xl
%attr(755,root,root) %{_bindir}/cjxl
%attr(755,root,root) %{_bindir}/cjpeg_hdr
%attr(755,root,root) %{_bindir}/djxl
%attr(755,root,root) %{_bindir}/jxlinfo
%{_mandir}/man1/cjxl.1*
%{_mandir}/man1/djxl.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjxl.so
%attr(755,root,root) %{_libdir}/libjxl_threads.so
%{_libdir}/libjxl_dec.a
%{_includedir}/jxl
%{_pkgconfigdir}/libjxl.pc
%{_pkgconfigdir}/libjxl_threads.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libjxl.a
%{_libdir}/libjxl_threads.a

%if %{with java}
%files -n java-libjxl
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjxl_jni.so
%{_javadir}/org.jpeg.jpegxl.jar
%endif

%files -n gdk-pixbuf2-loader-jxl
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-jxl.so
%{_datadir}/mime/packages/image-jxl.xml
%{_datadir}/thumbnailers/jxl.thumbnailer

%files -n gimp-plugin-jxl
%defattr(644,root,root,755)
%dir %{_libdir}/gimp/2.0/plug-ins/file-jxl
%attr(755,root,root) %{_libdir}/gimp/2.0/plug-ins/file-jxl/file-jxl
