%define	version 1.3.9
%define	release %mkrel 6

Name:      ibus
Summary:   A next generation input framework
Version:   %{version}
Release:   %{release}
Group:     System/Internationalization
License:   GPLv2+
URL:       http://code.google.com/p/ibus/
Source0:   http://ibus.googlecode.com/files/%{name}-%{version}.tar.gz
Source1:   ibus.macros
Patch0:    ibus-1.3.6-mdv-customize.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
%py_requires -d
BuildRequires:  gtk2-devel
BuildRequires:	gtk+3-devel
BuildRequires:  dbus-glib-devel
BuildRequires:	python-dbus >= 0.83.0
BuildRequires:	iso-codes
BuildRequires:  gettext-devel intltool gtk-doc
BuildRequires:	python-gobject-devel >= 2.15
BuildRequires:	libGConf2-devel >= 2.12
BuildRequires:	GConf2
BuildRequires:	gobject-introspection-devel
Requires:	python-gobject >= 2.15
Requires:	python-dbus >= 0.83.0
Requires:	pygtk2.0
Requires:	python-notify
Requires:	pyxdg
Requires:	iso-codes
Requires:	librsvg
Suggests:	%{name}-gtk = %version

%description
IBus is a next generation input framework.

%define major 2
%define libname %mklibname %name %major

%package -n %libname
Summary:    Shared libraries for %{name}
Group:      System/Internationalization
Conflicts:  ibus < 1.3.9-3

%description -n %libname
IBus shared libraries.

%package    devel
Summary:    Headers of %{name} for development
Group:      Development/C
Requires:   %{libname} = %{version}-%{release}

%description devel
IBus development package: static libraries, header files, and the like.

%package    gtk
Summary:    IBus gtk module
Group:      System/Internationalization
Requires:   ibus = %{version}

%description gtk
IBus gtk module.

%package    gtk3
Summary:    IBus gtk3 module
Group:      System/Internationalization
Requires:   ibus = %{version}

%description gtk3
IBus gtk module.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0

%build
%configure2_5x \
	--enable-gtk3 \
	--disable-dbus-python-check
%make

%install
rm -rf %buildroot
%makeinstall_std

# install .desktop files
echo "NoDisplay=true" >> %buildroot%{_datadir}/applications/ibus.desktop
echo "NoDisplay=true" >> %buildroot%{_datadir}/applications/ibus-setup.desktop

# install rpm macro
mkdir -p %buildroot%{_sysconfdir}/rpm/macros.d/
install -m0644 %{SOURCE1} %buildroot%{_sysconfdir}/rpm/macros.d/%name.macros

rm -f %buildroot%_libdir/*.la
rm -f %buildroot%_libdir/gtk-*/*/immodules/*.la
rm -f %buildroot%{_sysconfdir}/xdg/autostart/ibus.desktop

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%preun
%preun_uninstall_gconf_schemas ibus

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_sysconfdir}/gconf/schemas/ibus.schemas
%{_bindir}/*
%{_libexecdir}/ibus-gconf
%{_libexecdir}/ibus-x11
%{_libexecdir}/ibus-ui-gtk
%{_datadir}/applications/*.desktop
%{_datadir}/ibus/*
%{_iconsdir}/*/*/*/*
%{python_sitelib}/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libibus.so.%{major}
%{_libdir}/libibus.so.%{major}.*
%{_libdir}/girepository-1.0/*.typelib

%files gtk
%defattr(-,root,root)
%{_libdir}/gtk-2.0/*/immodules/*.so

%files gtk3
%defattr(-,root,root)
%{_libdir}/gtk-3.0/*/immodules/*.so

%files devel
%defattr(-,root,root)
%{_includedir}/ibus-1.0
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gtk-doc/html/ibus
%{_datadir}/gir-1.0/*.gir
%{_datadir}/vala/vapi/*.vapi
%{_sysconfdir}/rpm/macros.d/%name.macros
