%define __jar_repack %{nil}
%define crowd_group crowd
%define crowd_user crowd
%define crowd_home /opt/crowd
%define crowd_user_home /var/opt/crowd
%define systemd_dir /usr/lib/systemd/system
%define logrotate_dir /etc/logrotate.d
%define crowd_version 2.12.0
%define crowd_release 1

Summary:    Atlassian Crowd
Name:       atlassian-crowd
Version:    %{crowd_version}
BuildArch:  noarch
Release:    %{crowd_release}
License:    Apache Software License
URL:        https://www.atlassian.com/software/crowd
Source0:    atlassian-crowd-%{version}.tar.gz
Source1:    %{name}.service
Source2:    %{name}.logrotate
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Single sign-on and user identity that's easy to use

%prep
%setup -q -n atlassian-crowd-%{version}

%build

%install
install -d -m 755 %{buildroot}/%{crowd_home}/
install -d -m 755 %{buildroot}/%{crowd_user_home}/
cp -R * %{buildroot}/%{crowd_home}/

# Remove useless executable files
rm -f %{buildroot}/%{crowd_home}/*.bat
rm -f %{buildroot}/%{crowd_home}/apache-tomcat/bin/*.bat
rm -f %{buildroot}/%{crowd_home}/apache-tomcat/bin/*.exe
rm -f %{buildroot}/%{crowd-home}/apache-tomcat/bin/*.dll

# Remove the 'safeToDelete.tmp'
rm -f %{buildroot}/%{crowd_home}/apache-tomcat/temp/safeToDelete.tmp

# Remove useless doc files
rm -f %{buildroot}/%{crowd_home}/build.*
rm -f %{buildroot}/%{crowd_home}/README.*
rm -rf %{buildroot}/%{crowd_home}/licenses
rm -rf %{buildroot}/%{crowd_home}/apache-tomcat/tools
rm -rf %{buildroot}/%{crowd_home}/apache-tomcat/tomcat-docs

# systemd service
install -d -m 755 %{buildroot}/%{systemd_dir}
install    -m 644 %_sourcedir/%{name}.service %{buildroot}/%{systemd_dir}/%{name}.service

# logrotate script
install -d -m 755 %{buildroot}/%{logrotate_dir}/logrotate.d
install    -m 644 %_sourcedir/%{name}.logrotate %{buildroot}/%{logrotate_dir}/%{name}.conf

# set data directory
install    -m 644 %_sourcedir/crowd-init.properties %{buildroot}/%{crowd_home}/crowd-webapp/WEB-INF/classes/crowd-init.properties

%clean
rm -rf %{buildroot}

%pre
getent group %{crowd_group} >/dev/null || groupadd -r %{crowd_group}
getent passwd %{crowd_user} >/dev/null || /usr/sbin/useradd --comment "Atlassian Crowd" --shell /sbin/nologin -M -r -g %{crowd_group} --home %{crowd_user_home} %{crowd_user}

%files
%defattr(-,%{crowd_user},%{crowd_group},0770)
%defattr(-,root,root)
%{crowd_user_home}
%{crowd_home}
%dir %attr(0775,%{crowd_user},%{crowd_group}) %{crowd_user_home}
%dir %attr(0775,%{crowd_user},%{crowd_group}) %{crowd_home}/apache-tomcat/conf
%dir %attr(0775,%{crowd_user},%{crowd_group}) %{crowd_home}/apache-tomcat/logs
%dir %attr(0775,%{crowd_user},%{crowd_group}) %{crowd_home}/apache-tomcat/work
%dir %attr(0775,%{crowd_user},%{crowd_group}) %{crowd_home}/apache-tomcat/temp
%{systemd_dir}/%{name}.service
%{logrotate_dir}/%{name}.conf
%defattr(-,root,%{crowd_group})

%post
/bin/systemctl daemon-reload
