Summary: The PPP (Point-to-Point Protocol) daemon.
Name: ppp
Version: 2.4.2
Release: 2.2
License: distributable
Group: System Environment/Daemons
Source0: ftp://ftp.samba.org/pub/ppp/ppp-%{version}.tar.gz
Source1: ppp-2.3.5-pamd.conf
Source2: ppp.logrotate
Patch0: ppp-2.4.2-make.patch
Patch1: ppp-2.3.6-sample.patch
Patch2: ppp-2.4.2-libutil.patch
Patch3: ppp-2.4.1-varargs.patch
Patch4: ppp-2.4.2-lib64.patch
Patch5: ppp-2.4.2-bpf.patch
Patch6: ppp-2.4.2-dontwriteetc.patch
Patch7: ppp-2.4.2-pie.patch

BuildRoot: %{_tmppath}/%{name}-root
BuildPrereq: pam-devel, libpcap
Requires: glibc >= 2.0.6, /etc/pam.d/system-auth, logrotate

%description
The ppp package contains the PPP (Point-to-Point Protocol) daemon and
documentation for PPP support. The PPP protocol provides a method for
transmitting datagrams over serial point-to-point links. PPP is
usually used to dial in to an ISP (Internet Service Provider) or other
organization over a modem and phone line.

%prep
%setup  -q
%patch0 -p1 -b .make
%patch1 -p1 -b .sample
# patch 2 depends on the -lutil in patch 0
%patch2 -p1 -b .libutil
%patch3 -p1 -b .varargs
# patch 4 depends on the -lutil in patch 0
%patch4 -p1 -b .lib64
%patch5 -p1 -b .bpf
%patch6 -p1 -b .dontwriteetc
%patch7 -p1 -b .pie
find . -type f -name "*.sample" | xargs rm -f 

%build
./configure
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS -fPIC"

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT MANDIR=$RPM_BUILD_ROOT%{_mandir} BINDIR=$RPM_BUILD_ROOT%{_sbindir}

## it shouldn't be SUID root be default
#chmod 755 $RPM_BUILD_ROOT/usr/sbin/pppd

chmod go+r scripts/*
chmod ugo-x scripts/autopppd
chmod 0755 $RPM_BUILD_ROOT/%{_libdir}/pppd/%{version}/*.so
mkdir -p $RPM_BUILD_ROOT/etc/pam.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/ppp

# Provide pointers for people who expect stuff in old places
ln -s ../../var/log/ppp/connect-errors $RPM_BUILD_ROOT/etc/ppp/connect-errors
ln -s ../../var/run/ppp/resolv.conf $RPM_BUILD_ROOT/etc/ppp/resolv.conf

# Logrotate script
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/ppp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_sbindir}/chat
%{_sbindir}/pppd
%{_sbindir}/pppdump
%{_sbindir}/pppstats
%{_mandir}/man8/chat.8*
%{_mandir}/man8/pppd.8*
%{_mandir}/man8/pppdump.8*
%{_mandir}/man8/pppstats.8*
%{_includedir}/pppd
%{_libdir}/pppd
%dir /etc/ppp
%dir /var/run/ppp
%attr(700, root, root) %dir /var/log/ppp
%config /etc/ppp/chap-secrets
%config /etc/ppp/options
%config /etc/ppp/pap-secrets
%config /etc/pam.d/ppp
%config /etc/logrotate.d/ppp
%doc FAQ PLUGINS README README.cbcp README.linux README.MPPE README.MSCHAP80 README.MSCHAP81 README.pwfd README.pppoe scripts sample

%changelog
* Fri May 14 2004 Thomas Woerner <twoerner@redhat.com> 2.4.2-2.2
- compiled pppd and chat PIE

* Thu May 13 2004 Thomas Woerner <twoerner@redhat.com> 2.4.2-2.1
- added 'missingok' to ppp.logrotate (#122911)

* Fri May 07 2004 Nils Philippsen <nphilipp@redhat.com> 2.4.2-2
- don't write to /etc (#118837)

* Wed Mar 10 2004 Nalin Dahyabhai <nalin@redhat.com> 2.4.2-1
- update to 2.4.2

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Sep  5 2003 Nalin Dahyabhai <nalin@redhat.com> 2.4.1-15
- rebuild

* Fri Sep  5 2003 Nalin Dahyabhai <nalin@redhat.com> 2.4.1-14
- apply the patch from -11

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Nalin Dahyabhai <nalin@redhat.com> 2.4.1-12
- rebuild

* Tue Jun  3 2003 Nalin Dahyabhai <nalin@redhat.com> 2.4.1-11
- check for libcrypt in the right directory at compile-time

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 12 2002 Elliot Lee <sopwith@redhat.com> 2.4.1-9
- Fix build failure by rebuilding

* Tue Nov 19 2002 Nalin Dahyabhai <nalin@redhat.com> 2.4.1-8
- rebuild
- set x86_64 to use varargs the way s390 does

* Mon Jul 22 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add patch:
	* Thu Jun 06 2002 Phil Knirsch <pknirsch@redhat.com>
	- Fixed varargs problem for s390/s390x.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri May 17 2002 Nalin Dahyabhai <nalin@redhat.com> 2.4.1-4
- rebuild in new environment

* Wed Feb 27 2002 Nalin Dahyabhai <nalin@redhat.com> 2.4.1-3
- revert cbcp patch, it's wrong (#55367)

* Thu Aug  9 2001 Nalin Dahyabhai <nalin@redhat.com> 2.4.1-2
- add buildprereq on pam-devel (#49559)
- add patch to respond to CBCP LCP requests (#15738)
- enable cbcp support at build-time
- change the Copyright: tag to a License: tag

* Wed May 23 2001 Nalin Dahyabhai <nalin@redhat.com> 2.4.1-1
- update to 2.4.1

* Fri Dec  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Thu Nov  9 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.4.0

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- move man pages to %{_mandir}

* Thu Jun  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- change perms using defattr
- modify PAM setup to use system-auth

* Sun Mar 26 2000 Florian La Roche <Florian.La Roche@redhat.com>
- change to root:root perms

* Mon Mar 06 2000 Nalin Dahyabhai <nalin@redhat.com>
- reaper bugs verified as fixed
- check pam_open_session result code (bug #9966)

* Mon Feb 07 2000 Nalin Dahyabhai <nalin@redhat.com>
- take a shot at the wrong reaper bugs (#8153, #5290)

* Thu Feb 03 2000 Nalin Dahyabhai <nalin@redhat.com>
- free ride through the build system (release 2)

* Tue Jan 18 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to 2.3.11

* Sat Nov 06 1999 Michael K. Johnson <johnsonm@redhat.com>
- Better fix for both problems

* Fri Nov 05 1999 Michael K. Johnson <johnsonm@redhat.com>
- fix for double-dial problem
- fix for requiring a controlling terminal problem

* Sun Sep 19 1999 Preston Brown <pbrown@redhat.com>
- 2.3.10 bugfix release

* Fri Aug 13 1999 Michael K. Johnson <johnsonm@redhat.com>
- New version 2.3.9 required for kernel 2.3.13 and will be required
  for new initscripts.  auth patch removed; 2.3.9 does the same thing
  more readably than the previous patch.

* Thu Jun 24 1999 Cristian Gafton <gafton@redhat.com>
- add pppdump

* Fri Apr 09 1999 Cristian Gafton <gafton@redhat.com>
- force pppd use the glibc's logwtmp instead of implementing its own

* Wed Apr 01 1999 Preston Brown <pbrown@redhat.com>
- version 2.3.7 bugfix release

* Tue Mar 23 1999 Cristian Gafton <gafton@redhat.com>
- version 2.3.6

* Mon Mar 22 1999 Michael Johnson <johnsonm@redhat.com>
- auth patch

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Thu Jan 07 1999 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Fri Jun  5 1998 Jeff Johnson <jbj@redhat.com>
- updated to 2.3.5.

* Tue May 19 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Fri May  8 1998 Jakub Jelinek <jj@ultra.linux.cz>
- make it run with kernels 2.1.100 and above.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Mar 18 1998 Cristian Gafton <gafton@redhat.com>
- requires glibc 2.0.6 or later

* Wed Mar 18 1998 Michael K. Johnson <johnsonm@redhat.com>
- updated PAM patch to not turn off wtmp/utmp/syslog logging.

* Wed Jan  7 1998 Cristian Gafton <gafton@redhat.com>
- added the /etc/pam.d config file
- updated PAM patch to include session support

* Tue Jan  6 1998 Cristian Gafton <gafton@redhat.com>
- updated to ppp-2.3.3, build against glibc-2.0.6 - previous patches not
  required any more.
- added buildroot
- fixed the PAM support, which was really, completely broken and against any
  standards (session support is still not here... :-( )
- we build against running kernel and pray that it will work
- added a samples patch; updated glibc patch

* Thu Dec 18 1997 Erik Troan <ewt@redhat.com>
- added a patch to use our own route.h, rather then glibc's (which has 
  alignment problems on Alpha's) -- I only applied this patch on the Alpha,
  though it should be safe everywhere

* Fri Oct 10 1997 Erik Troan <ewt@redhat.com>
- turned off the execute bit for scripts in /usr/doc

* Fri Jul 18 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Tue Mar 25 1997 Erik Troan <ewt@redhat.com>
- Integrated new patch from David Mosberger
- Improved description

