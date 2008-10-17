%define	version 0.1.1.20081016
%define	release %mkrel 1

Name:      ibus
Summary:   A next generation input framework
Version:   %{version}
Release:   %{release}
Group:     System/Internationalization
License:   GPLv2+
URL:       http://code.google.com/p/ibus/
Source0:   http://ibus.googlecode.com/files/%{name}-%{version}.tar.gz
Patch0:    ibus-0.1.1-defaults-to-auto-hide.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
%py_requires -d
BuildRequires:   iso-codes
BuildRequires:   gtk2-devel
BuildRequires:   qt4-devel
BuildRequires:   dbus-glib-devel
BuildRequires:   gettext-devel
Requires:	pygtk2.0
Requires:	python-dbus >= 0.83.0
Requires:	pyxdg
Requires:	gnome-python-gconf
Suggests:	%{name}-gtk = %version

%description
IBus is a next generation input framework.

%package    devel
Summary:    Headers of %{name} for development
Group:      Development/C

%description devel
IBus development package: static libraries, header files, and the like.

%package    gtk
Summary:    IBus gtk module
Group:      System/Internationalization
Requires:   ibus = %{version}
Requires(post):	gtk+2.0, ibus = %{version}
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
%patch0 -p0

%build
%configure2_5x
%make

%install
rm -rf %buildroot
%makeinstall_std

# install .desktop files
echo "NoDisplay=true" >> %buildroot%{_datadir}/applications/ibus.desktop
echo "NoDisplay=true" >> %buildroot%{_datadir}/applications/ibus-setup.desktop

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
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/ibus/*
%{_datadir}/pixmaps/*
%{python_sitelib}/*

%files gtk
%defattr(-,root,root)
%{_libdir}/libibus-gtk.so.0*
%{_libdir}/gtk-2.0/*/immodules/*.so

%files qt4
%defattr(-,root,root)
%{qt4plugins}/inputmethods/*.so

%files devel
%defattr(-,root,root)
%{_libdir}/libibus-gtk.la
%{_libdir}/libibus-gtk.so
%{_libdir}/gtk-2.0/*/immodules/*.la
