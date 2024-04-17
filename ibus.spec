%define api	1.0
%define major	5
%define libname %mklibname %{name} %{api} %{major}
%define girname %mklibname %{name}-gir %{api}
%define devname %mklibname %{name} -d
%define _disable_rebuild_configure 1

Summary:	A next generation input framework
Name:		ibus
Version:	1.5.29
Release:	1
Group:		System/Internationalization
License:	GPLv2+
Url:		https://github.com/ibus/ibus/
Source0:	https://github.com/ibus/ibus/releases/download/%{version}/%{name}-%{version}.tar.gz
Source1:	ibus.macros
Patch0:		ibus-1.5.26-gtk4-linkage.patch

BuildRequires:	dconf
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	iso-codes
BuildRequires:	libx11-common
BuildRequires:	vala
BuildRequires:	vala-tools
BuildRequires:	gettext-devel
BuildRequires:	unicode-cldr-annotations
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(dbus-python)
BuildRequires:	pkgconfig(dbusmenu-glib-0.4)
BuildRequires:	pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:	pkgconfig(dconf)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gtk4)
BuildRequires:  pkgconfig(iso-codes)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(pygobject-3.0)
BuildRequires:	pkgconfig(vapigen)
BuildRequires:	unicode-cldr-annotations
BuildRequires:	pkgconfig(python)
BuildRequires:	python-gi 
BuildRequires:	systemd-rpm-macros
Requires:	iso-codes
Requires:	librsvg
Recommends:	python-notify
Requires:	pyxdg
Requires:	typelib(IBus)
Suggests:	%{name}-gtk = %{version}
Requires:	unicode-cldr-annotations

%description
IBus is a next generation input framework.

%package -n %{libname}
Summary:	Shared libraries for %{name}
Group:		System/Internationalization
Conflicts:	ibus < 1.3.9-3

%description -n %{libname}
IBus shared libraries.

%package -n python-ibus
Summary:	Python bindings to ibus
Group:		System/Libraries

%description -n python-ibus
Python bindings to ibus

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}ibus1.0_5 < 1.5.2-1

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n %{devname}
Summary:	Headers of %{name} for development
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}ibus1.0_5-devel < 1.5.2-1

%description -n	%{devname}
IBus development package: development libraries, header files, and the like.

%package    gtk2
Summary:	IBus gtk 2.x module
Group:		System/Internationalization
Requires:	ibus = %{version}
%rename %{name}-gtk

%description gtk2
IBus gtk 2.x module.

%package    gtk3
Summary:	IBus gtk 3.x module
Group:		System/Internationalization
Requires:	ibus = %{version}

%description gtk3
IBus gtk 3.x module.

%package    gtk4
Summary:	IBus gtk 4.x module
Group:		System/Internationalization
Requires:	ibus = %{version}

%description gtk4
IBus gtk 4.x module.

%prep
%autosetup -p1

%build
%configure \
	--enable-gtk3 \
	--disable-dbus-python-check \
	--enable-vala=yes \
	--disable-gconf \
	--enable-dconf \
	--enable-wayland \
	--enable-gtk4

%make_build

%install
%make_install
%find_lang %{name}10

# install .desktop files
echo "NoDisplay=true" >> %{buildroot}%{_datadir}/applications/org.freedesktop.IBus.Setup.desktop

# install rpm macro
mkdir -p %{buildroot}%{_sysconfdir}/rpm/macros.d/
install -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/rpm/macros.d/%{name}.macros

rm -rf %{buildroot}%{py3_platsitedir}/gi/overrides/__pycache__

# Create a Plasma (and LXQt and Cutefish and ...) friendly version
# of the systemd service...
sed -e 's,generic sessions,Qt based desktops,;s,ibus-daemon,ibus-daemon --xim --desktop=kde --panel=/usr/lib64/libexec/kimpanel-ibus-panel --emoji-extension=/usr/bin/ibus-ui-emojier-plasma,' %{buildroot}%{_userunitdir}/org.freedesktop.IBus.session.generic.service >%{buildroot}%{_userunitdir}/org.freedesktop.IBus.session.KDE.service


%preun
%preun_uninstall_gconf_schemas ibus

%files -f %{name}10.lang
%doc AUTHORS COPYING ChangeLog NEWS README
%{_sysconfdir}/dconf/profile/ibus
%{_sysconfdir}/dconf/db/ibus.d
%{_bindir}/*
%{_libexecdir}/ibus-dconf
%{_libexecdir}/ibus-x11
%{_libexecdir}/ibus-engine-simple
%{_libexecdir}/ibus-portal
%{_libexecdir}/ibus-ui-emojier
%{_libexecdir}/ibus-wayland
%{_datadir}/applications/*.desktop
%{_datadir}/bash-completion/completions/ibus.bash
%{_datadir}/GConf/gsettings/ibus.convert
%{_datadir}/glib-2.0/schemas/org.freedesktop.ibus.gschema.xml
%{_datadir}/dbus-1/services/org.freedesktop.IBus.service
%{_datadir}/dbus-1/services/org.freedesktop.portal.IBus.service
%{_datadir}/ibus/*
%{_iconsdir}/*/*/*/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_datadir}/gettext/its/ibus.*
%{_sysconfdir}/xdg/Xwayland-session.d/10-ibus-x11
%{_userunitdir}/org.freedesktop.IBus.session.generic.service
%{_userunitdir}/org.freedesktop.IBus.session.KDE.service

%files -n %{libname}
%{_libdir}/libibus-%{api}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/IBus-%{api}.typelib

%files gtk2
%{_libdir}/gtk-2.0/*/immodules/*.so

%files gtk3
%{_libdir}/gtk-3.0/*/immodules/*.so
%{_libexecdir}/ibus-ui-gtk*
%{_libexecdir}/ibus-extension-gtk3
%{_userunitdir}/gnome-session.target.wants/org.freedesktop.IBus.session.GNOME.service
%{_userunitdir}/org.freedesktop.IBus.session.GNOME.service

%files gtk4
%{_libdir}/gtk-4.0/*/immodules/libim-ibus.so

%files -n %{devname}
%{_includedir}/ibus-1.0
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gtk-doc/html/ibus
%{_datadir}/gir-1.0/*.gir
%{_datadir}/vala/vapi/*.vapi
%{_datadir}/vala/vapi/ibus-1.0.deps
%{_sysconfdir}/rpm/macros.d/%{name}.macros

%files -n python-ibus
%{py3_platsitedir}/gi/overrides/IBus.*
