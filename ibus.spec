%define	version 1.1.0.20090423
%define	release %mkrel 1

Name:      ibus
Summary:   A next generation input framework
Version:   %{version}
Release:   %{release}
Group:     System/Internationalization
License:   GPLv2+
URL:       http://code.google.com/p/ibus/
Source0:   http://ibus.googlecode.com/files/%{name}-%{version}.tar.gz
Patch1:    ibus-0.1.1-lower-qt-version-dep.patch
Patch3:		ibus-1.1.0-enalbe-qt4.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
%py_requires -d
BuildRequires:  gtk2-devel
BuildRequires:  qt4-devel
BuildRequires:  dbus-glib-devel
Buildrequires:	python-dbus >= 0.83.0
BuildRequires:  gettext-devel intltool gtk-doc
BuildRequires:	python-gobject-devel >= 2.15
BuildRequires:	libGConf2-devel
Requires:	python-gobject >= 2.15
Requires:	pygtk2.0
Requires:	python-dbus >= 0.83.0
Requires:	pyxdg
Requires:	gnome-python-gconf
Requires:	iso-codes
Suggests:	%{name}-gtk = %version

%description
IBus is a next generation input framework.

%package    devel
Summary:    Headers of %{name} for development
Group:      Development/C
Requires:   %{name} = %{version}-%{release}

%description devel
IBus development package: static libraries, header files, and the like.

%package    gtk
Summary:    IBus gtk module
Group:      System/Internationalization
Requires:   ibus = %{version}
Requires(post):	gtk+2.0
Requires(postun): gtk+2.0

%description gtk
IBus gtk module.

%package    qt4
Summary:    IBus qt4 module
Group:      System/Internationalization
Requires:   ibus = %{version}

%description qt4
IBus qt4 module.

%prep
%setup -q -n %{name}-%{version}
%patch3 -p0
%if %mdkversion < 200900
%patch1 -p0
%endif

%build
%if %mdkversion < 200900
export PKG_CONFIG_PATH=%_libdir/pkgconfig:%qt4lib/pkgconfig
%endif
./autogen.sh
%configure2_5x --enable-qt4-immodule \
	--disable-dbus-python-check --disable-iso-codes-check
%make

%install
rm -rf %buildroot
%makeinstall_std

# install .desktop files
echo "NoDisplay=true" >> %buildroot%{_datadir}/applications/ibus.desktop
echo "NoDisplay=true" >> %buildroot%{_datadir}/applications/ibus-setup.desktop

rm -f %buildroot%_libdir/*.la
rm -f %buildroot%_libdir/gtk-2.0/*/immodules/*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post gtk
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib

%postun gtk
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_sysconfdir}/gconf/schemas/ibus.schemas
%{_bindir}/*
%{_libdir}/libibus.so.0*
%{_libexecdir}/ibus-gconf
%{_libexecdir}/ibus-x11
%{_libexecdir}/ibus-ui-gtk
%{_datadir}/applications/*.desktop
%{_datadir}/ibus/*
%{_datadir}/pixmaps/*
%{python_sitelib}/*
%exclude %{_sysconfdir}/xdg/autostart/ibus.desktop

%files gtk
%defattr(-,root,root)
%{_libdir}/gtk-2.0/*/immodules/*.so

%files qt4
%defattr(-,root,root)
%{qt4plugins}/inputmethods/*.so

%files devel
%defattr(-,root,root)
%{_includedir}/ibus-1.0
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gtk-doc/html/ibus
