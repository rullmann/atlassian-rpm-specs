%define __jar_repack %{nil}
%define confluence_group confluence
%define confluence_user confluence
%define confluence_home /opt/confluence
%define confluence_user_home /var/opt/confluence
%define systemd_dir /usr/lib/systemd/system
%define logrotate_dir /etc/logrotate.d
%define confluence_version 6.1.2
%define confluence_release 1

Summary:    Atlassian Confluence
Name:       atlassian-confluence
Version:    %{confluence_version}
BuildArch:  noarch
Release:    %{confluence_release}
License:    Apache Software License
URL:        https://www.atlassian.com/software/confluence
Source0:    atlassian-confluence-%{version}.tar.gz
Source1:    %{name}.service
Source2:    %{name}.logrotate
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Confluence is where you create, organize and discuss work with your team.

%prep
%setup -q -n atlassian-confluence-%{version}

%build

%install
install -d -m 755 %{buildroot}/%{confluence_home}/
install -d -m 755 %{buildroot}/%{confluence_user_home}/
cp -R * %{buildroot}/%{confluence_home}/

# Remove windows bat files
rm -f %{buildroot}/%{confluence_home}/bin/*.bat

# Remove the 'safeToDelete.tmp'
rm -f %{buildroot}/%{confluence_home}/temp/safeToDelete.tmp

# Remove useless doc files
rm -f %{buildroot}/%{confluence_home}/LICENSE
rm -f %{buildroot}/%{confluence_home}/NOTICE
rm -f %{buildroot}/%{confluence_home}/RELEASE-NOTES
rm -f %{buildroot}/%{confluence_home}/RUNNING.txt
rm -f %{buildroot}/%{confluence_home}/README.*

# systemd service
install -d -m 755 %{buildroot}/%{systemd_dir}
install    -m 644 %_sourcedir/%{name}.service %{buildroot}/%{systemd_dir}/%{name}.service

# logrotate script
install -d -m 755 %{buildroot}/%{logrotate_dir}/logrotate.d
install    -m 644 %_sourcedir/%{name}.logrotate %{buildroot}/%{logrotate_dir}/%{name}.conf

%clean
rm -rf %{buildroot}

%pre
getent group %{confluence_group} >/dev/null || groupadd -r %{confluence_group}
getent passwd %{confluence_user} >/dev/null || /usr/sbin/useradd --comment "Atlassian Confluence" --shell /sbin/nologin -M -r -g %{confluence_group} --home %{confluence_user_home} %{confluence_user}

%files
%defattr(-,%{confluence_user},%{confluence_group},0770)
%defattr(-,root,root)
%{confluence_user_home}
%{confluence_home}
%dir %attr(0775,%{confluence_user},%{confluence_group}) %{confluence_user_home}
%dir %attr(0775,%{confluence_user},%{confluence_group}) %{confluence_home}/conf
%dir %attr(0775,%{confluence_user},%{confluence_group}) %{confluence_home}/logs
%dir %attr(0775,%{confluence_user},%{confluence_group}) %{confluence_home}/work
%dir %attr(0775,%{confluence_user},%{confluence_group}) %{confluence_home}/temp
%{systemd_dir}/%{name}.service
%{logrotate_dir}/%{name}.conf
%defattr(-,root,%{confluence_group})

%post
/bin/systemctl daemon-reload

