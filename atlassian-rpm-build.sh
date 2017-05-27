#!/bin/bash

set -e

# Variables
BUILDDIR="$HOME/rpmbuild"
RMBUILDDIR=0
BUILDALL=0
products=(bamboo bitbucket crowd confluence jira)

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
 jira

Options:
 -a    build all the products
 -f    force removal of ~/rpmbuild without asking
 -h    print this message and exit
EOF
}

# Function to clean up environment
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

# Function to retrieve the repo
function get_repo {
    git clone https://github.com/rullmann/atlassian-rpm-specs.git $BUILDDIR
}

# Function to that the given product is in our products array
valid_product () {
    local p
    for p in "${@:2}"; do [[ "$p" == "$1" ]] && return 0; done
}

# Get teh currently defined version in the spec file for a given product
get_version () {
    grep "%define ${PRODUCT}_version" $BUILDDIR/SPECS/atlassian-$PRODUCT.spec | awk '{print $3}'
}

# Build the download url for a product
downloadlink_product () {
    echo "https://www.atlassian.com/software/$PRODUCT/downloads/binary/atlassian-$PRODUCT-$VERSION.tar.gz"
}

# Build a given product
build_product () {
    rpmbuild -bb --quiet $BUILDDIR/SPECS/atlassian-$PRODUCT.spec
}

# The actual process of downloading and building a given product and version
function dl_and_build {
    echo -e "\n###\n\nReady to download and build the rpm file for $PRODUCT. Please wait.\n\n###\n"
    # JIRA is a special snowflake when it comes to the download link
    if [ $PRODUCT = "jira" ]; then
        wget --quiet https://www.atlassian.com/software/jira/downloads/binary/atlassian-jira-software-$VERSION.tar.gz -P $BUILDDIR/SOURCES/
    # Bitbucket is an unicorn
    elif [ $PRODUCT = "bitbucket" ]; then
        wget --quiet https://www.atlassian.com/software/stash/downloads/binary/atlassian-$PRODUCT-$VERSION.tar.gz -P $BUILDDIR/SOURCES/
    else
        wget --quiet $(downloadlink_product $PRODUCT) -P $BUILDDIR/SOURCES/
    fi
    # Finally start the build process
    build_product
}

# Print the filenames of a build
function print_rpm_filename {
    # Print the filename of the build
    if [ $PRODUCT = "jira" ]; then
        echo -e "\nYour rpm file for $PRODUCT can be found here: $BUILDDIR/RPMS/noarch/atlassian-$PRODUCT-software-$VERSION-1.noarch.rpm"
    else
        echo -e "\n###\n\nYour rpm for $PRODUCT can be found here: $BUILDDIR/RPMS/noarch/atlassian-$PRODUCT-$VERSION-1.noarch.rpm"
    fi
}

# Verify that there are arguments
if [ -z "$1" ] ; then
    print_usage
    exit 1
fi

# Get args and update variables
while getopts p:h,f,a opt ; do
    case "${opt}"
    in
    p) PRODUCT=${OPTARG};;
    h) print_usage ; exit 1 ;;
    f) RMBUILDDIR=1 ;;
    a) BUILDALL=1 ;;
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

# Grab the latest spec files with git
echo -e "\n###\n\nCloning the repository\n\n###\n"
get_repo

# Check if the -a argument has been used
if [ $BUILDALL -eq 1 ] ; then
    for PRODUCT in "${products[@]}" ; do
        VERSION=$(get_version $PRODUCT)
        dl_and_build
    done
    for PRODUCT in "${products[@]}" ; do
        VERSION=$(get_version $PRODUCT)
        print_rpm_filename
    done
# if not proceed with a single product
else
    # Verify that the given product is valid. Exit if not.
    if valid_product "$PRODUCT" "${products[@]}" ; then
        VERSION=$(get_version $PRODUCT)
        dl_and_build
        print_rpm_filename
    else
        echo -e "###\n\nNo valid product chosen! Please read the usage information below!\n\n###\n"
        print_usage
        exit 1
    fi
fi
