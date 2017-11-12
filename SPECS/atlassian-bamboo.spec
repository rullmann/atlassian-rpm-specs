%define __jar_repack %{nil}
%define bamboo_group bamboo
%define bamboo_user bamboo
%define bamboo_home /opt/bamboo
%define bamboo_user_home /var/opt/bamboo
%define systemd_dir /usr/lib/systemd/system
%define logrotate_dir /etc/logrotate.d
%define bamboo_version 6.2.2
%define bamboo_release 1

Summary:    Atlassian Bamboo
Name:       atlassian-bamboo
Version:    %{bamboo_version}
BuildArch:  noarch
Release:    %{bamboo_release}
License:    Apache Software License
URL:        https://www.atlassian.com/software/bamboo
Source0:    atlassian-bamboo-%{version}.tar.gz
Source1:    %{name}.service
Source2:    %{name}.logrotate
Source3:    bamboo-init.properties
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Bamboo Server is the choice of professional teams for continuous integration, deployment, and delivery

%prep
%setup -q -n atlassian-bamboo-%{version}

%build

%install
install -d -m 755 %{buildroot}/%{bamboo_home}/
install -d -m 755 %{buildroot}/%{bamboo_user_home}/
cp -R * %{buildroot}/%{bamboo_home}/

# Remove deprecated bamboo.sh file
rm -f %{buildroot}/%{bamboo_home}/bamboo.sh

# Remove the 'safeToDelete.tmp'
rm -f %{buildroot}/%{bamboo_home}/temp/safeToDelete.tmp

# Remove useless doc files
rm -f %{buildroot}/%{bamboo_home}/NOTICE
rm -f %{buildroot}/%{bamboo_home}/README.*
rm -rf %{buildroot}/%{bamboo_home}/tomcat-docs
rm -rf %{buildroot}/%{bamboo_home}/licenses

# Remove Apache maven as it's not required
rm -rf %{buildroot}/%{bamboo_home}/tools/apache-maven-3.5.0

# systemd service
install -d -m 755 %{buildroot}/%{systemd_dir}
install    -m 644 %_sourcedir/%{name}.service %{buildroot}/%{systemd_dir}/%{name}.service

# logrotate script
install -d -m 755 %{buildroot}/%{logrotate_dir}/logrotate.d
install    -m 644 %_sourcedir/%{name}.logrotate %{buildroot}/%{logrotate_dir}/%{name}.conf

# set data directory
install    -m 644 %_sourcedir/bamboo-init.properties %{buildroot}/%{bamboo_home}/atlassian-bamboo/WEB-INF/classes/bamboo-init.properties

%clean
rm -rf %{buildroot}

%pre
getent group %{bamboo_group} >/dev/null || groupadd -r %{bamboo_group}
getent passwd %{bamboo_user} >/dev/null || /usr/sbin/useradd --comment "Atlassian Bamboo" --shell /sbin/nologin -M -r -g %{bamboo_group} --home %{bamboo_user_home} %{bamboo_user}

%files
%defattr(-,%{bamboo_user},%{bamboo_group},0770)
%defattr(-,root,root)
%{bamboo_user_home}
%{bamboo_home}
%dir %attr(0775,%{bamboo_user},%{bamboo_group}) %{bamboo_user_home}
%dir %attr(0775,%{bamboo_user},%{bamboo_group}) %{bamboo_home}/conf
%dir %attr(0775,%{bamboo_user},%{bamboo_group}) %{bamboo_home}/logs
%dir %attr(0775,%{bamboo_user},%{bamboo_group}) %{bamboo_home}/work
%dir %attr(0775,%{bamboo_user},%{bamboo_group}) %{bamboo_home}/temp
%{systemd_dir}/%{name}.service
%{logrotate_dir}/%{name}.conf
%defattr(-,root,%{bamboo_group})

%post
/bin/systemctl daemon-reload
