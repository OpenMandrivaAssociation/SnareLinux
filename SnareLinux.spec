%define name SnareLinux
%define version 1.5.1
%define release %mkrel 1

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Snare for Linux - audit subsystem control and distribution
License:	GPL
Group:		System Environment/Daemons
URL:		https://www.intersectalliance.com/
Source: 	http://www.intersectalliance.com/projects/SnareLinux/Download/%{name}-%{version}.tar.gz
Requires:	audit >= 1.0.16, libaudit1 >= 1.0.16, policycoreutils
BuildRequires:	libaudit-devel >= 1.0.16
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
The System iNtrusion Analysis and Reporting Environment (SNARE) agent for
Linux provides a event collection, filtering, control and remote distribution
cabability for the Linux operating system. Snare supports organisations
that need to meet national security policy guidelines such as NISPOM,
DCID/DIAM, SOX/Sarbanes Oxley, GLBA, CISP and BS7799.

%prep
rm -rf $RPM_BUILD_ROOT

%setup -q

%build
perl -pi -e 's|^\s*\$\(bindir\)/SnareTranslationTable||' Makefile
perl -pi -e 's|^\s*./Installer.sh -i \$\(confdir\) \$\(bindir\) \$\(sharedir\)||' Makefile
%make clean
%make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_sbindir}  %{buildroot}%{_sysconfdir} %{buildroot}%{_datadir}/%{name}-%{version}
%make prefix=%{buildroot} install
cp Installer.sh %{buildroot}/%{_sbindir}/SnareInstaller.sh
cp snare.pp %{buildroot}%{_datadir}/%{name}-%{version}/

%post
if [ -f /usr/sbin/semodule ]; then /usr/sbin/semodule -i /usr/share/%{name}-%{version}/snare.pp; fi
%{_sbindir}/SnareInstaller.sh -i %{_sysconfdir} %{_sbindir} %{_datadir}/%{name}-%{version}
echo "Please modify /etc/snare.conf to turn on the web control interface"
%{_sbindir}/SnareTranslationTable

%clean
rm -rf $RPM_BUILD_ROOT

%preun
# only if this is not an upgrade
if [ $1 -eq 0 ]; then
	/usr/sbin/SnareInstaller.sh -u %{_sysconfdir} %{_sbindir} %{_datadir}/%{name}-%{version}
fi

%postun
# only if this is not an upgrade
if [ $1 -eq 0 ]; then
	if [ -f /usr/sbin/semodule ]; then
		/usr/sbin/semodule -l | egrep "^snare" > /dev/null
		if [ "$?" -eq 0 ]; then
			/usr/sbin/semodule -r snare;
		fi
	fi
fi

%files
%defattr(-,root,root)
%attr(750,root,root) %{_sbindir}/SnareDispatcher
%attr(750,root,root) %{_sbindir}/SnareDispatchHelper
%attr(750,root,root) %{_sbindir}/SnareTranslationTable
%attr(750,root,root) %{_sbindir}/SnareWebServer.pl
%attr(750,root,root) %{_sbindir}/SnareInstaller.sh
%attr(640,root,root) %{_sysconfdir}/snare.conf
%attr(644,root,root) %{_datadir}/%{name}-%{version}/snare.pp
%config(noreplace) %{_sysconfdir}/snare.conf
#%attr(644,root,root) %{_sysconfdir}/snare-xlate.conf

%changelog
