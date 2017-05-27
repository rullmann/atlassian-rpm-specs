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

# Requirements and usage

* Red Hat-based Linux distribution
  * Fedora 25 is highly recommended, as an bug in older versions of rpmbuild prevent building most Java applications
* `rpmbuild`
* [Oracle Java](http://www.oracle.com/technetwork/java/javase/downloads/index-jsp-138363.html)

Simply clone the repo as some unpriviledged user:

<pre>
$ cd ~
$ git clone https://github.com/rullmann/atlassian-rpm-specs.git rpmbuild
</pre>

* Verify what version you want to build in the appropriate file in the `SPECS`-dir.
* Download the tar archive from Atlassian and move it to `~/rpmbuild/SOURCES`-dir:
  * [Confluence](https://www.atlassian.com/software/confluence/download)
  * [JIRA Software](https://www.atlassian.com/software/jira/download)
  * [Bamboo](https://www.atlassian.com/software/bamboo/download)
  * [Bitbucket](https://www.atlassian.com/software/bitbucket/download)
  * [Crowd](https://www.atlassian.com/software/crowd/download)

After that you can simply build with one of the spec files, e.g. Confluence:

<pre>
$ rpmbuild -bb rpmbuild/SPECS/atlassian-confluence.spec
</pre>
