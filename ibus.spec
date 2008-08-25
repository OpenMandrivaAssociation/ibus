%define	version 0.1.1
%define	date    20080825
%define	release %mkrel 1.%{date}.1

%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %name

Name:      ibus
Summary:   A next generation input framework
Version:   %{version}
Release:   %{release}
Group:     System/Internationalization
License:   GPLv2+
URL:       http://code.google.com/p/ibus/
Source0:   http://ibus.googlecode.com/files/%{name}-%{version}.%{date}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}.%{date}-%{release}-buildroot
Requires:        %{libname} = %{version}
BuildRequires:   python-devel gtk2-devel
BuildRequires:   qt4-devel dbus-devel
BuildRequires:   gettext-devel

%description
IBus is a next generation input framework.


%package -n %{libname}
Summary:    IBus library
Group:      System/Internationalization

%description -n %{libname}
IBus library.

%package -n %{develname}
Summary:    Headers of %{name} for development
Group:      Development/C
Requires:   %{libname} = %{version}
Provides:   %{name}-devel = %{version}-%{release}

%description -n %{develname}
IBus development package: static libraries, header files, and the like.

%package    gtk
Summary:    IBus gtk module
Group:      System/Internationalization
Requires:   ibus = %{version}
Requires:   gtk+2.0

%description gtk
IBus gtk module.

%package    qt4
Summary:    IBus qt4 module
Group:      System/Internationalization
Requires:   ibus = %{version}
Requires:   qt4-common

%description qt4
IBus qt4 module.


%prep
%setup -q -n %{name}-%{version}.%{date}

%build
%configure2_5x

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

# fix for x86_64
if [ "%{_lib}" == "lib64" ] ; then
mv %buildroot/usr/lib/python2.5 %buildroot/%{_libdir}
fi

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

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/python2.5/*

%files gtk
%defattr(-,root,root)
%{_libdir}/libibus-gtk.so.0.0.0
%{_libdir}/gtk-2.0/immodules/*.so

%files qt4
%defattr(-,root,root)
%{_libdir}/qt4/*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/libibus-gtk.la
%{_libdir}/libibus-gtk.so
%{_libdir}/libibus-gtk.so.0
%{_libdir}/gtk-2.0/immodules/*.la


