#!/bin/bash

# Variables
BUILDDIR="$HOME/rpmbuild"
RMBUILDDIR=0
products=( bamboo bitbucket crowd confluence jira-software all)

# Check if running as root
if [ "$EUID" -eq 0 ] ; then
    echo -e "###\n\nPlease run as an unpriviledged user to start building!\n\n###"
    exit 1
fi

# Function to print the usage information
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
 jira-software
 all

Options:
 -f    force removal of ~/rpmbuild without asking
 -h    print this message and exit
EOF
}

# Clean up environment
function cleanup_env_question {
echo -e "###\n\nIn order to have a clean build environment\nthis script will remove ~/rpmbuild.\nPlease make sure you have a backup if required.\n\n###\n"
read -p "Proceed to remove ~/rpmbuild directory? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
    rm -rf $BUILDDIR
else
    echo -e "###\n\nCan't proceed without removing ~/rpmbuild. Bye."
    exit 1
fi
}

# Verify that there are arguments
if [ -z "$1" ] ; then
    print_usage
    exit 1
fi

# Function to retrieve the repo
function get_repo {
    git clone https://github.com/rullmann/atlassian-rpm-specs.git $HOME/rpmbuild
}

# Function to that the given product is in our products array
valid_product () {
  local p
  for p in "${@:2}"; do [[ "$p" == "$1" ]] && return 0; done
}

# Get args and update variables
while getopts p:h,f opt ; do
    case "${opt}"
    in
    p) PRODUCT=${OPTARG};;
    h) print_usage ; exit 1 ;;
    f) RMBUILDDIR=1;;
    esac
done

# Remove rpmbuild-dir if it exists
if [ -d $BUILDDIR ] ; then
    if [ $RMBUILDDIR -eq 1 ] ; then
        rm -rf $BUILDDIR
    else
        cleanup_env_question
    fi
fi

# Verify that the given product is valid. Exit if not.
if valid_product "$PRODUCT" "${products[@]}" ; then
    echo -e "###\n\nReady to download and build the rpm files. Please wait.\n\n###\n"
else
    echo -e "###\n\nNo valid product chosen! Please read the usage information below!\n\n###\n"
    print_usage
    exit 1
fi
