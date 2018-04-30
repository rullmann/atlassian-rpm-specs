%define __jar_repack %{nil}
%define bitbucket_group bitbucket
%define bitbucket_user bitbucket
%define bitbucket_home /opt/bitbucket
%define bitbucket_user_home /var/opt/bitbucket
%define systemd_dir /usr/lib/systemd/system
%define bitbucket_version 5.10.0
%define bitbucket_release 1

Summary:    Atlassian Bitbucket
Name:       atlassian-bitbucket
Version:    %{bitbucket_version}
BuildArch:  noarch
Release:    %{bitbucket_release}
License:    Apache Software License
URL:        https://www.atlassian.com/software/bitbucket
Source0:    atlassian-bitbucket-%{version}.tar.gz
Source1:    %{name}.service
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Bitbucket is the Git solution for professional teams

%prep
%setup -q -n atlassian-bitbucket-%{version}

%build

%install
install -d -m 755 %{buildroot}/%{bitbucket_home}/
install -d -m 755 %{buildroot}/%{bitbucket_user_home}/
cp -R * %{buildroot}/%{bitbucket_home}/

# Remove useless executable files
rm -f %{buildroot}/%{bitbucket_home}/bin/*.bat
rm -f %{buildroot}/%{bitbucket_home}/bin/*.exe
rm -rf %{buildroot}/%{bitbucket_home}/lib/native

# Remove useless doc files
rm -rf %{buildroot}/%{bitbucket_home}/licenses
rm -f %{buildroot}/%{bitbucket_home}/README.txt
rm -f %{buildroot}/%{bitbucket_home}/elasticsearch/README.textile
rm -f %{buildroot}/%{bitbucket_home}/elasticsearch/LICENSE.txt
rm -f %{buildroot}/%{bitbucket_home}/elasticsearch/NOTICE.txt

# systemd service
install -d -m 755 %{buildroot}/%{systemd_dir}
install    -m 644 %_sourcedir/%{name}.service %{buildroot}/%{systemd_dir}/%{name}.service

%clean
rm -rf %{buildroot}

%pre
getent group %{bitbucket_group} >/dev/null || groupadd -r %{bitbucket_group}
getent passwd %{bitbucket_user} >/dev/null || /usr/sbin/useradd --comment "Atlassian bitbucket" --shell /sbin/nologin -M -r -g %{bitbucket_group} --home %{bitbucket_user_home} %{bitbucket_user}

%files
%defattr(-,%{bitbucket_user},%{bitbucket_group},0770)
%defattr(-,root,root)
%{bitbucket_user_home}
%{bitbucket_home}
%dir %attr(0775,%{bitbucket_user},%{bitbucket_group}) %{bitbucket_user_home}
%{systemd_dir}/%{name}.service
%defattr(-,root,%{bitbucket_group})

%post
/bin/systemctl daemon-reload
