%define	version 1.3.6
%define	release %mkrel 2

Name:      ibus
Summary:   A next generation input framework
Version:   %{version}
Release:   %{release}
Group:     System/Internationalization
License:   GPLv2+
URL:       http://code.google.com/p/ibus/
Source0:   http://ibus.googlecode.com/files/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
%py_requires -d
BuildRequires:  gtk2-devel
BuildRequires:  dbus-glib-devel
BuildRequires:	python-dbus >= 0.83.0
BuildRequires:	iso-codes
BuildRequires:  gettext-devel intltool gtk-doc
BuildRequires:	python-gobject-devel >= 2.15
BuildRequires:	libGConf2-devel
BuildRequires:	gobject-introspection-devel
Requires:	python-gobject >= 2.15
Requires:	python-dbus >= 0.83.0
Requires:	pygtk2.0
Requires:	python-notify
Requires:	pyxdg
Requires(post):	GConf2
Requires(preun): GConf2
Requires:	iso-codes
Requires:	librsvg
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

%prep
%setup -q -n %{name}-%{version}

%build
%configure2_5x \
	--disable-dbus-python-check
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

%preun
%preun_uninstall_gconf_schemas ibus

%post gtk
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib

%postun gtk
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_sysconfdir}/gconf/schemas/ibus.schemas
%{_bindir}/*
%{_libdir}/libibus.so.2*
%{_libdir}/girepository-1.0/*.typelib
%{_libexecdir}/ibus-gconf
%{_libexecdir}/ibus-x11
%{_libexecdir}/ibus-ui-gtk
%{_datadir}/applications/*.desktop
%{_datadir}/ibus/*
%{_iconsdir}/*/*/*/*
%{python_sitelib}/*
%exclude %{_sysconfdir}/xdg/autostart/ibus.desktop

%files gtk
%defattr(-,root,root)
%{_libdir}/gtk-2.0/*/immodules/*.so

%files devel
%defattr(-,root,root)
%{_includedir}/ibus-1.0
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gtk-doc/html/ibus
%{_datadir}/gir-1.0/*.gir
%{_datadir}/vala/vapi/*.vapi
