Summary:	Media player based on BMP
Name:		audacious
Version:	3.6.1
Release:	1
License:	GPL
Group:		X11/Applications/Sound
Source0:	http://distfiles.audacious-media-player.org/%{name}-%{version}.tar.bz2
# Source0-md5:	8bfec6d11a05f4be6cf9eab4e18be307
URL:		http://audacious-media-player.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gtk+3-devel
#BuildRequires:	libguess-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	pkg-config
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	hicolor-icon-theme
Requires:	%{name}-libs = %{version}-%{release}
Requires:	audacious-plugins
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Audacious is a media player based on BMP. Since the development of the
former project had been terminated, this fork was created.

%package libs
Summary:	Audacious media player library
Group:		X11/Applications/Sound

%description libs
Audacious media player library.

%package devel
Summary:	Header files for Audacious media player
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files required for compiling Audacious media player plugins.

%prep
%setup -qn %{name}-%{version}

%{__sed} -i -e 's/gthread-2.0/gthread-2.0 gmodule-2.0/' configure.ac

%build
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%configure
%{__make} V=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/audacious/{Container,Effect,General,Input,Output,Transport,Visualization}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_localedir}/fa{_IR,}
mv $RPM_BUILD_ROOT%{_localedir}/id{_ID,}
mv $RPM_BUILD_ROOT%{_localedir}/ml{_IN,}
mv $RPM_BUILD_ROOT%{_localedir}/pt{_PT,}
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{cmn,sr_RS}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor

%postun
%update_desktop_database
%update_icon_cache hicolor

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/audacious
%attr(755,root,root) %{_bindir}/audtool

%dir %{_datadir}/audacious
%dir %{_datadir}/audacious/images
%dir %{_libdir}/audacious/Container
%dir %{_libdir}/audacious/Effect
%dir %{_libdir}/audacious/General
%dir %{_libdir}/audacious/Input
%dir %{_libdir}/audacious/Output
%dir %{_libdir}/audacious/Transport
%dir %{_libdir}/audacious/Visualization

%{_datadir}/audacious/images/*

%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.*

%{_mandir}/man*/*

%files libs
%defattr(644,root,root,755)
%dir %{_libdir}/audacious
%attr(755,root,root) %ghost %{_libdir}/libaudcore.so.?
%attr(755,root,root) %ghost %{_libdir}/libaudgui.so.?
%attr(755,root,root) %ghost %{_libdir}/libaudtag.so.?
%attr(755,root,root) %{_libdir}/libaudcore.so.*.*.*
%attr(755,root,root) %{_libdir}/libaudtag.so.*.*.*
%attr(755,root,root) %{_libdir}/libaudgui.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaudcore.so
%attr(755,root,root) %{_libdir}/libaudgui.so
%attr(755,root,root) %{_libdir}/libaudtag.so
%{_includedir}/audacious
%{_includedir}/libaudcore
%{_includedir}/libaudgui
%{_pkgconfigdir}/audacious.pc

