%define __jar_repack %{nil}
%define jira_group jira
%define jira_user jira
%define jira_home /opt/jira
%define jira_user_home /var/opt/jira
%define systemd_dir /usr/lib/systemd/system
%define logrotate_dir /etc/logrotate.d
%define jira_version 7.7.1
%define jira_release 1

Summary:    Atlassian JIRA Software
Name:       atlassian-jira-software
Version:    %{jira_version}
BuildArch:  noarch
Release:    %{jira_release}
License:    Apache Software License
URL:        https://www.atlassian.com/software/jira
Source0:    atlassian-jira-software-%{version}.tar.gz
Source1:    %{name}.service
Source2:    %{name}.logrotate
Source3:    jira-application.properties
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The #1 software development tool used by agile teams

%prep
%setup -q -n atlassian-jira-software-%{version}-standalone

%build

%install
install -d -m 755 %{buildroot}/%{jira_home}/
install -d -m 755 %{buildroot}/%{jira_user_home}/
cp -R * %{buildroot}/%{jira_home}/

# Remove useless executable files
rm -f %{buildroot}/%{jira_home}/bin/*.bat
rm -f %{buildroot}/%{jira_home}/bin/*.exe
rm -f %{buildroot}/%{jira_home}/bin/*.exe.x64
rm -rf %{buildroot}/%{jira_home}/bin/apr

# Remove the 'safeToDelete.tmp'
rm -f %{buildroot}/%{jira_home}/temp/safeToDelete.tmp

# Remove useless doc files
rm -f %{buildroot}/%{jira_home}/NOTICE
rm -f %{buildroot}/%{jira_home}/README.*
rm -rf %{buildroot}/%{jira_home}/tomcat-docs
rm -rf %{buildroot}/%{jira_home}/licenses
rm -rf %{buildroot}/%{jira_home}/external-source

# systemd service
install -d -m 755 %{buildroot}/%{systemd_dir}
install    -m 644 %_sourcedir/%{name}.service %{buildroot}/%{systemd_dir}/%{name}.service

# logrotate script
install -d -m 755 %{buildroot}/%{logrotate_dir}/logrotate.d
install    -m 644 %_sourcedir/%{name}.logrotate %{buildroot}/%{logrotate_dir}/%{name}.conf

# set data directory
install    -m 644 %_sourcedir/jira-application.properties %{buildroot}/%{jira_home}/atlassian-jira/WEB-INF/classes/jira-application.properties

%clean
rm -rf %{buildroot}

%pre
getent group %{jira_group} >/dev/null || groupadd -r %{jira_group}
getent passwd %{jira_user} >/dev/null || /usr/sbin/useradd --comment "Atlassian jira" --shell /sbin/nologin -M -r -g %{jira_group} --home %{jira_user_home} %{jira_user}

%files
%defattr(-,%{jira_user},%{jira_group},0770)
%defattr(-,root,root)
%{jira_user_home}
%{jira_home}
%dir %attr(0775,%{jira_user},%{jira_group}) %{jira_user_home}
%dir %attr(0775,%{jira_user},%{jira_group}) %{jira_home}/conf
%dir %attr(0775,%{jira_user},%{jira_group}) %{jira_home}/logs
%dir %attr(0775,%{jira_user},%{jira_group}) %{jira_home}/work
%dir %attr(0775,%{jira_user},%{jira_group}) %{jira_home}/temp
%{systemd_dir}/%{name}.service
%{logrotate_dir}/%{name}.conf
%defattr(-,root,%{jira_group})

%post
/bin/systemctl daemon-reload
