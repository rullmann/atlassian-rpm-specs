# atlassian-rpm-specs - Build your own rpm packages of Atlassian products

[Atlassian](https://www.atlassian.com/) is offering some great tools for team collaboration and developers.
The installation can be done from an installer or an archive.

...

Wait, what? From an archive or an installer?
Where can I find packages for Debian or RHEL?

For years there have been issues [asking for rpm support](https://jira.atlassian.com/browse/CONFSERVER-36902).
As they won't provide such builds others have to. 🤓

# Disclaimer

Atlassian does not allow public distribution of the software, e.g. as rpm files.
Therefore it is advised to use this repo and the scripts, which do not contain the software itself, only for internal use.
You should not make your builds public!

The scripts and spec files provided are not fully tested and may break your existing installation.
Please keep in mind to test the files before installing on a production anvironment.

# Requirements and usage

* Red Hat-based Linux distribution
  * Fedora 25 is highly recommended, as an bug in older versions of rpmbuild prevent building most Java applications
* `rpmbuild`

To download and view the help:

<pre>
    curl -fsSL https://github.com/rullmann/atlassian-rpm-specs/raw/master/atlassian-rpm-build.sh | sh -h
</pre>

If you want to download and build the rpm files for all produts directly simple use the `-a` option:

<pre>
    curl -fsSL https://github.com/rullmann/atlassian-rpm-specs/raw/master/atlassian-rpm-build.sh | sh -a
</pre>

## Build time

On a machine with 12 Cores, 32 GB RAM and 1 Gbit/s connection it takes approx. 12 minutes to download and build all the packages.

# Installation

The packages can be installed with `dnf` as well as `rpm`.
You should make sure that Oracle Java is installed and `JRE_HOME` is set.
