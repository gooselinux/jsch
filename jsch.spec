# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define section   free

%define gcj_support 0

Name:           jsch
Version:        0.1.41
Release:        2.2%{?dist}
Epoch:          0
Summary:        Pure Java implementation of SSH2
Group:          Development/Libraries
License:        BSD
URL:            http://www.jcraft.com/jsch/
Source0:        http://download.sourceforge.net/sourceforge/jsch/jsch-%{version}.zip
# wget \
# http://download.eclipse.org/tools/orbit/downloads/drops/R20090825191606/bundles/com.jcraft.jsch_0.1.41.v200903070017.jar
# unzip com.jcraft.jsch_*.jar META-INF/MANIFEST.MF
# mv META-INF/MANIFEST.MF .
# sed -i "/^Name/d" MANIFEST.MF
# sed -i "/^SHA1/d" MANIFEST.MF
# dos2unix MANIFEST.MF
# sed -i "/^$/d" MANIFEST.MF
# unix2dos MANIFEST.MF
Source1:        MANIFEST.MF

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:  java-devel >= 1.4.2
BuildRequires:  jzlib >= 0:1.0.5
BuildRequires:  ant

%if ! %{gcj_support}
BuildArch:      noarch
%endif

%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel >= 1.0.31
Requires(post): java-gcj-compat >= 1.0.31
Requires(postun): java-gcj-compat >= 1.0.31
%endif
Requires:       jzlib >= 0:1.0.5

%description
JSch allows you to connect to an sshd server and use port forwarding, 
X11 forwarding, file transfer, etc., and you can integrate its 
functionality into your own Java programs.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Documentation

%description    javadoc
%{summary}.

%package        demo
Summary:        Examples for %{name}
Group:          Documentation

%description    demo
%{summary}.


%prep
%setup -q

%build
export CLASSPATH=$(build-classpath jzlib)
ant dist javadoc 

# inject the OSGi Manifest
mkdir META-INF
cp %{SOURCE1} META-INF
zip dist/lib/%{name}-*.jar META-INF/MANIFEST.MF

%install
# jars
rm -rf $RPM_BUILD_ROOT
install -Dpm 644 dist/lib/%{name}-*.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# examples
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
cp -pr examples/* $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_datadir}/%{name}

%if %{gcj_support}
# https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=234989
%ifnarch ia64
  aot-compile-rpm
%endif 
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{_bindir}/rebuild-gcj-db

%postun
%{_bindir}/rebuild-gcj-db
%endif

%files
%defattr(-,root,root,-)
%{_javadir}/*.jar
%doc LICENSE.txt
%if %{gcj_support}
%ifnarch ia64
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif
%endif

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}*

%files demo
%defattr(-,root,root,-)
%doc %{_datadir}/%{name}*


%changelog
* Mon Jan 11 2010 Andrew Overholt <overholt@redhat.com> 0:0.1.41-2.2
- Update URL in comment for MANIFEST.MF
- Fix Groups
- Remove ghost symlinking

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0:0.1.41-2.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.1.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 8 2009 Alexander Kurtakov <akurtako@redhat.com> 0:0.1.41-1
- Update to new version 0.1.41.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.1.39-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jul 11 2008 Andrew Overholt <overholt@redhat.com> 0:0.1.39-1.1
- 0.1.39

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:0.1.31-2.5
- drop repotag

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:0.1.31-2jpp.4
- fix license tag

* Mon Apr 07 2008 Deepak Bhole <dbhole@redhat.com> - 0:0.1.31-2jpp.3
- Fix bz# 441071: Add backward compatibility patch from mwringe at redhat

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:0.1.31-2jpp.2
- Autorebuild for GCC 4.3

* Thu Sep 20 2007 Deepak Bhole <dbhole@redhat.com> - 0:0.1.31-1jpp.2
- Added %%{?dist} as per new policy

* Tue Jun 5 2007 Ben Konrath <bkonrath@redhat.com> - 0:0.1.31-1jpp.1
- 0.1.31.

* Tue Apr 3 2007 Ben Konrath <bkonrath@redhat.com> - 0:0.1.28-1jpp.6
- Add OSGi Manifest to jar.
- Disable aot-compile-rpm on ia64. 

* Thu Aug 10 2006 Deepak Bhole <dbhole@redhat.com> - 0:0.1.28-1jpp.5
- Updated changelog entries in spec.

* Fri Aug 04 2006 Deepak Bhole <dbhole@redhat.com> - 0:0.1.28-1jpp.4
- Added conditional compiling support.
- Added missing requirements.
- Additionally, for synchronizaion between logs:
- From r.apel@r-apel.de:
  - 0.1.26
- From fnasser@redhat.com:
  - 0.1.20

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:0.1.28-1jpp_3fc
- Rebuilt

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0:0.1.28-1jpp_2fc
- rebuild

* Thu Jun  1 2006 Ben Konrath <bkonrath@redhat.com> - 0:0.1.28-1jpp_1fc
- 0.1.28
- Add BuildRequires ant.

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 0:0.1.18-1jpp_7fc
- stop scriptlet spew

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0:0.1.18-1jpp_6fc
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0:0.1.18-1jpp_5fc
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Dec 21 2005 Andrew Overholt <overholt@redhat.com> 0.1.18-1jpp_4fc
- Rebuild again

* Tue Dec 13 2005 Andrew Overholt <overholt@redhat.com> 0.1.18-1jpp_3fc
- Rebuild with gcc 4.1.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Jul 15 2005 Gary Benson <gbenson@redhat.com> 0.1.18-1jpp_2fc
- Build on ia64, ppc64, s390 and s390x.
- Switch to aot-compile-rpm.

* Fri Apr 22 2005 Andrew Overholt <overholt@redhat.com> 0.1.18-1jpp_1fc
- Build into Fedora.
- Natively-compile.

* Fri Apr 22 2005 Fernando Nasser <fnasser@redhat.com> 0:0.1.18-1jpp_1rh
- Merge with upstream for 0.1.18 upgrade

* Fri Apr 22 2005 Fernando Nasser <fnasser@redhat.com> 0:0.1.18-1jpp
- 0.1.18

* Fri Mar 18 2005 Andrew Overholt <overholt@redhat.com> 0.1.17-2jpp_1fc
- Build into Fedora.
- Remove Distribution and Vendor tags.
- Add BuildRequires:  java-devel for javadoc requirement.

* Tue Nov 02 2004 David Walluck <david@jpackage.org> 0:0.1.17-2jpp
- rebuild with jdk 1.4.2

* Tue Oct 19 2004 David Walluck <david@jpackage.org> 0:0.1.17-1jpp
- 0.1.17

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:0.1.13-2jpp
- Rebuild with ant-1.6.2

* Sat Feb 14 2004 David Walluck <david@anti-microsoft.org> 0:0.1.13-1jpp
- 0.1.13

* Wed Jan 14 2004 Ralph Apel <r.apel@r-apel.de> - 0:0.1.12-1jpp
- First JPackage build.
