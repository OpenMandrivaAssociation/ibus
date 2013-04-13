%define	version 1.5.1
%define	release 1

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
Patch1:	   ibus-1.5.1-strfmt.patch
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
BuildRequires:	pkgconfig(dconf)
BuildRequires:	dconf
BuildRequires:	vala
BuildRequires:	vala-tools
BuildRequires:	pkgconfig(vapigen)
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

%define major 5
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
%patch1 -p1

%build
%configure2_5x \
	--enable-gtk3 \
	--disable-dbus-python-check \
	--enable-python-library --enable-gconf --enable-vala=yes
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

%find_lang %{name}10

%preun
%preun_uninstall_gconf_schemas ibus

%files -f %{name}10.lang
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_sysconfdir}/bash_completion.d/ibus.bash
%{_sysconfdir}/gconf/schemas/ibus.schemas
%{_bindir}/*
%{_libexecdir}/ibus-gconf
%{_libexecdir}/ibus-x11
%{_libexecdir}/ibus-ui-gtk*
%{_libexecdir}/ibus-engine-simple
%{_datadir}/applications/*.desktop
%{_datadir}/ibus/*
%{_iconsdir}/*/*/*/*
%{python_sitelib}/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libibus*.so.*
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
%{_datadir}/vala/vapi/ibus-1.0.deps
%{_sysconfdir}/rpm/macros.d/%name.macros


%changelog
* Wed Oct  3 2012 Arkady L. Shane <ashejn@rosalab.ru> 1.4.99.20120917-1
- update to 1.4.99.20120917

* Fri May 06 2011 Funda Wang <fwang@mandriva.org> 1.3.9-6mdv2011.0
+ Revision: 669810
- fix escape char of macros

* Tue Apr 26 2011 Funda Wang <fwang@mandriva.org> 1.3.9-5
+ Revision: 659261
- register by installed locales, not by  system locale

* Tue Apr 26 2011 Funda Wang <fwang@mandriva.org> 1.3.9-4
+ Revision: 659256
- install rpm helper macro for engine register
- revised macro
- rename macro to macros
- add test rpm macro

* Mon Apr 25 2011 Funda Wang <fwang@mandriva.org> 1.3.9-3
+ Revision: 658388
- split out libs

* Thu Mar 24 2011 Funda Wang <fwang@mandriva.org> 1.3.9-2
+ Revision: 648262
- build gtk3 module

* Tue Nov 30 2010 Funda Wang <fwang@mandriva.org> 1.3.9-1mdv2011.0
+ Revision: 603343
- update to new version 1.3.9

* Tue Nov 02 2010 Michael Scherer <misc@mandriva.org> 1.3.8-4mdv2011.0
+ Revision: 592393
- rebuild for python 2.7

  + Funda Wang <fwang@mandriva.org>
    - rebuild for py2.7

* Mon Oct 25 2010 Funda Wang <fwang@mandriva.org> 1.3.8-2mdv2011.0
+ Revision: 589215
- update file list
- update to new version 1.3.8

* Mon Aug 09 2010 Funda Wang <fwang@mandriva.org> 1.3.7-1mdv2011.0
+ Revision: 568001
- update to new version 1.3.7

* Sun Aug 08 2010 Funda Wang <fwang@mandriva.org> 1.3.6-4mdv2011.0
+ Revision: 567667
- customize ibus:
  * add Ctrl_Shift as keybindings for switching input methods (compatible with windows)
  * default to show language bar if input methods is activated

* Thu Jul 29 2010 Funda Wang <fwang@mandriva.org> 1.3.6-2mdv2011.0
+ Revision: 563172
- rebuild for new gobject-introspection

* Sat Jul 10 2010 Funda Wang <fwang@mandriva.org> 1.3.6-1mdv2011.0
+ Revision: 549908
- New version 1.3.6

* Thu Jun 24 2010 Funda Wang <fwang@mandriva.org> 1.3.5-1mdv2010.1
+ Revision: 548989
- New version 1.3.5

* Thu May 06 2010 Funda Wang <fwang@mandriva.org> 1.3.3-1mdv2010.1
+ Revision: 542826
- New version 1.3.3
  (fix crash of ibus-x11 and ibus-daemon)

* Mon Apr 26 2010 Funda Wang <fwang@mandriva.org> 1.3.2-2mdv2010.1
+ Revision: 538983
- add requires

* Mon Apr 26 2010 Funda Wang <fwang@mandriva.org> 1.3.2-1mdv2010.1
+ Revision: 538823
- New version 1.3.2

* Sat Mar 27 2010 Funda Wang <fwang@mandriva.org> 1.2.1-2mdv2010.1
+ Revision: 528047
- bump rel
- update to new version 1.2.1

* Sat Jan 16 2010 Funda Wang <fwang@mandriva.org> 1.2.0.20100111-1mdv2010.1
+ Revision: 492370
- new version 1.2.0.20100111

* Fri Dec 25 2009 Funda Wang <fwang@mandriva.org> 1.2.0.20091225-1mdv2010.1
+ Revision: 482237
- new verison 1.2.0.20091225

* Thu Dec 17 2009 Funda Wang <fwang@mandriva.org> 1.2.0.20091215-1mdv2010.1
+ Revision: 479622
- new version 1.2.0.20091215

* Sat Dec 05 2009 Funda Wang <fwang@mandriva.org> 1.2.0.20091204-1mdv2010.1
+ Revision: 473929
- new version 1.2.0.20091204

* Wed Nov 25 2009 Funda Wang <fwang@mandriva.org> 1.2.0.20091124-1mdv2010.1
+ Revision: 469951
- new version 1.2.0.20091124

* Fri Nov 06 2009 Funda Wang <fwang@mandriva.org> 1.2.0.20091024-1mdv2010.1
+ Revision: 460557
- New version 1.2.0.20091024

* Sat Oct 17 2009 Funda Wang <fwang@mandriva.org> 1.2.0.20091014-1mdv2010.0
+ Revision: 457998
- add GConf2 requires
- New version 1.2.0.20091014
- fix problem when uninstalling (forget to call unregister gconf keys)

* Thu Oct 01 2009 Funda Wang <fwang@mandriva.org> 1.2.0.20090927-2mdv2010.0
+ Revision: 451924
- rebuild
- New version 1.2.0.20090927

* Wed Sep 16 2009 Funda Wang <fwang@mandriva.org> 1.2.0.20090915-1mdv2010.0
+ Revision: 443463
- New version 1.2.0.20090915

* Tue Sep 15 2009 Funda Wang <fwang@mandriva.org> 1.2.0.20090904-1mdv2010.0
+ Revision: 441963
- fix file list
- New version 1.2.0.20090904

* Thu Sep 03 2009 Funda Wang <fwang@mandriva.org> 1.2.0.20090828-1mdv2010.0
+ Revision: 426837
- New version 1.2.0.20090828

* Wed Aug 12 2009 Funda Wang <fwang@mandriva.org> 1.2.0.20090812-1mdv2010.0
+ Revision: 415454
- new version 1.2.0.20090812

* Tue Aug 11 2009 Funda Wang <fwang@mandriva.org> 1.2.0.20090810-1mdv2010.0
+ Revision: 414519
- new version 1.2.0.20090810

* Fri Aug 07 2009 Funda Wang <fwang@mandriva.org> 1.2.0.20090807-1mdv2010.0
+ Revision: 411063
- new version 1.2.0.20090807

* Thu Aug 06 2009 Funda Wang <fwang@mandriva.org> 1.2.0.20090806-1mdv2010.0
+ Revision: 410438
- new version 1.2.0.20090806

* Mon Aug 03 2009 Funda Wang <fwang@mandriva.org> 1.2.0.20090723-1mdv2010.0
+ Revision: 408349
- New version series 1.2.0

* Fri Jun 12 2009 Funda Wang <fwang@mandriva.org> 1.1.0.20090612-1mdv2010.0
+ Revision: 385510
- New version 1.1.0.20090612

* Thu Jun 11 2009 Funda Wang <fwang@mandriva.org> 1.1.0.20090609-1mdv2010.0
+ Revision: 385121
- New version 1.1.0.20090609

* Tue Jun 02 2009 Funda Wang <fwang@mandriva.org> 1.1.0.20090531-1mdv2010.0
+ Revision: 382249
- New version 1.1.0.20090531

* Mon May 11 2009 Funda Wang <fwang@mandriva.org> 1.1.0.20090508-1mdv2010.0
+ Revision: 374142
- New version  1.1.0.20090508

* Fri May 01 2009 Funda Wang <fwang@mandriva.org> 1.1.0.20090423-1mdv2010.0
+ Revision: 369418
- BR iso-codes
- BR dbus-python
- BR gtkdoc
- BR intltool
- New version 1.1.0.20090423

* Sat Mar 14 2009 Funda Wang <fwang@mandriva.org> 1.1.0.20090311-1mdv2009.1
+ Revision: 354799
- New version 1.1.0.20090311

* Sat Mar 07 2009 Funda Wang <fwang@mandriva.org> 1.1.0.20090306-1mdv2009.1
+ Revision: 351813
- New version 1.1.0.20090306

* Thu Feb 26 2009 Funda Wang <fwang@mandriva.org> 1.1.0.20090225-1mdv2009.1
+ Revision: 345039
- do not ship xdg auto start file
- New version 20090225

* Sat Feb 21 2009 Funda Wang <fwang@mandriva.org> 1.1.0.20090217-1mdv2009.1
+ Revision: 343569
- enable qt4
- New version 1.1.0.20090217

* Fri Feb 13 2009 Funda Wang <fwang@mandriva.org> 1.1.0.20090211-1mdv2009.1
+ Revision: 339993
- update to new version 1.1.0.20090211

* Thu Feb 05 2009 Funda Wang <fwang@mandriva.org> 1.1.0.20090205-3mdv2009.1
+ Revision: 337933
- la files are too confuse

* Thu Feb 05 2009 Funda Wang <fwang@mandriva.org> 1.1.0.20090205-2mdv2009.1
+ Revision: 337918
- devel should require main package

* Thu Feb 05 2009 Funda Wang <fwang@mandriva.org> 1.1.0.20090205-1mdv2009.1
+ Revision: 337899
- New version 1.1.0.20090205

* Thu Dec 25 2008 Funda Wang <fwang@mandriva.org> 0.1.1.20081023-3mdv2009.1
+ Revision: 318655
- rebuild for new python

* Thu Nov 13 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.1.20081023-2mdv2009.1
+ Revision: 302739
- rebuilt against new libxcb

  + Funda Wang <fwang@mandriva.org>
    - lower qt ver dependency, preparing backports for 2008.1

* Thu Oct 23 2008 Funda Wang <fwang@mandriva.org> 0.1.1.20081023-1mdv2009.1
+ Revision: 296653
- New version 0.1.1.20081023

* Fri Oct 17 2008 Funda Wang <fwang@mandriva.org> 0.1.1.20081016-2mdv2009.1
+ Revision: 294579
- the dependecy is solved within sub package

* Fri Oct 17 2008 Funda Wang <fwang@mandriva.org> 0.1.1.20081016-1mdv2009.1
+ Revision: 294562
- new version 0.1.1.20081016
- defaults to auto-hide panel
- adjust post requires
- fix requires

* Thu Oct 16 2008 Funda Wang <fwang@mandriva.org> 0.1.1.20081006-2mdv2009.1
+ Revision: 294130
- don't dispaly any desktop files

* Sat Oct 11 2008 Funda Wang <fwang@mandriva.org> 0.1.1.20081006-1mdv2009.1
+ Revision: 292370
- BR iso-codes
- New version 0.1.1.20081006

* Sun Sep 21 2008 Funda Wang <fwang@mandriva.org> 0.1.1.20080908-2mdv2009.0
+ Revision: 286324
- suggest gtk immodule

* Mon Sep 08 2008 Funda Wang <fwang@mandriva.org> 0.1.1.20080908-1mdv2009.0
+ Revision: 282552
- New version

* Fri Sep 05 2008 Funda Wang <fwang@mandriva.org> 0.1.1.20080901-1mdv2009.0
+ Revision: 281256
- New version 0.1.1.20080901
- add requires on python modules

* Sun Aug 31 2008 Funda Wang <fwang@mandriva.org> 0.1.1.20080830-1mdv2009.0
+ Revision: 277702
- update to new version 0.1.1.20080830

* Mon Aug 25 2008 Funda Wang <fwang@mandriva.org> 0.1.1.20080825-1mdv2009.0
+ Revision: 275713
- fix package layout
- import ibus


* Mon Aug 25 2008 UTUMI Hirosi <utuhiro78@yahoo.co.jp> 0.1.1-1.20080825.1mdv2009.0
- first package for Mandriva
