#!/bin/bash

# Check if root
if [ "$EUID" -eq 0 ] ; then
    echo -e "###\n\nPlease run as an unpriviledged user to start building!\n\n###"
    exit 1
fi

function print_usage {
cat <<-EOF
atlassian-rpm-build.sh
Build your own rpm packages of Atlassian products

Usage: ./atlassian-rpm-build.sh [product] [options]

Product:
 bamboo
 bitbucket
 crowd
 confluence
 jira
 all

Options:
 -f    force removal of ~/rpmbuild without asking
 -h    print this message and exit
EOF
}

# Clean up environment
function cleanup_env {
if [ -d ~/rpmbuild ] ; then
    echo -e "###\n\nIn order to have a clean build environment\nthis script will remove ~/rpmbuild.\nPlease make sure you have a backup if required.\n\n###\n"
    read -p "Proceed to remove ~/rpmbuild directory? " -n 1 -r
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        rm -rf ~/rpmbuild
    else
        echo -e "###\n\nCan't proceed without removing ~/rpmbuild. Bye."
        exit 1
    fi
fi
}

if [ -z "$1" ] ; then
    print_usage
    exit 1
fi

while getopts p:h,f opt ; do
    case "${opt}"
    in
    p) PRODUCT=${OPTARG};;
    h) print_usage ; exit 1 ;;
    f) RMBUILDDIR=1;;
    esac
done

