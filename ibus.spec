%define api	1.0
%define major	5
%define libname %mklibname %{name} %{api} %{major}
%define girname %mklibname %{name}-gir %{api}
%define devname %mklibname %{name} -d

Summary:	A next generation input framework
Name:		ibus
Version:	1.5.9
Release:	7
Group:		System/Internationalization
License:	GPLv2+
Url:		https://github.com/ibus/ibus/
Source0:	https://github.com/ibus/ibus/releases/download/%{version}/%{name}-%{version}.tar.gz
Source1:	ibus.macros

BuildRequires:	dconf
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	iso-codes
BuildRequires:	vala
BuildRequires:	vala-tools
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(dbus-python)
BuildRequires:	pkgconfig(dconf)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(pygobject-3.0)
BuildRequires:	pkgconfig(vapigen)
BuildRequires:	python-gi 
Requires:	iso-codes
Requires:	librsvg
Requires:	python-gobject >= 2.15
Requires:	python-dbus >= 0.83.0
Requires:	pygtk2.0
Requires:	python-notify
Requires:	pyxdg
Requires:	typelib(IBus)
Suggests:	%{name}-gtk = %{version}

%description
IBus is a next generation input framework.

%package -n %{libname}
Summary:	Shared libraries for %{name}
Group:		System/Internationalization
Conflicts:	ibus < 1.3.9-3

%description -n %{libname}
IBus shared libraries.

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

%package    gtk
Summary:	IBus gtk module
Group:		System/Internationalization
Requires:	ibus = %{version}

%description gtk
IBus gtk module.

%package    gtk3
Summary:	IBus gtk3 module
Group:		System/Internationalization
Requires:	ibus = %{version}

%description gtk3
IBus gtk module.

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
	--enable-gtk3 \
	--disable-dbus-python-check \
	--enable-vala=yes \
	--disable-gconf \
	--enable-dconf 

%make

%install
%makeinstall_std
%find_lang %{name}10

# install .desktop files
echo "NoDisplay=true" >> %{buildroot}%{_datadir}/applications/ibus-setup.desktop

# install rpm macro
mkdir -p %{buildroot}%{_sysconfdir}/rpm/macros.d/
install -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/rpm/macros.d/%{name}.macros

rm -f %{buildroot}%{_sysconfdir}/xdg/autostart/ibus.desktop
rm -rf %{buildroot}%{py3_platsitedir}/gi/overrides/__pycache__

%preun
%preun_uninstall_gconf_schemas ibus

%files -f %{name}10.lang
%doc AUTHORS COPYING ChangeLog NEWS README
%{_sysconfdir}/dconf/profile/ibus
%{_sysconfdir}/dconf/db/ibus.d
%{_bindir}/*
%{_libexecdir}/ibus-dconf
%{_libexecdir}/ibus-x11
%{_libexecdir}/ibus-ui-gtk*
%{_libexecdir}/ibus-engine-simple
%{_datadir}/applications/*.desktop
%{_datadir}/bash-completion/completions/ibus.bash
%{_datadir}/GConf/gsettings/ibus.convert
%{_datadir}/glib-2.0/schemas/org.freedesktop.ibus.gschema.xml
%{_datadir}/ibus/*
%{_iconsdir}/*/*/*/*
%{_datadir}/man/man1/*
%{py3_platsitedir}/gi/overrides/IBus.*

%files -n %{libname}
%{_libdir}/libibus-%{api}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/IBus-%{api}.typelib

%files gtk
%{_libdir}/gtk-2.0/*/immodules/*.so

%files gtk3
%{_libdir}/gtk-3.0/*/immodules/*.so

%files -n %{devname}
%{_includedir}/ibus-1.0
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gtk-doc/html/ibus
%{_datadir}/gir-1.0/*.gir
%{_datadir}/vala/vapi/*.vapi
%{_datadir}/vala/vapi/ibus-1.0.deps
%{_sysconfdir}/rpm/macros.d/%{name}.macros

