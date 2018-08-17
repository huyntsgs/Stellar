#!/bin/bash

# Dependencies
echo "Install dependencies ? [y/n]"
read ins
if [ $ins = "y" ] || [ $ins = "" ]; then
	su -c "apt -qq update && apt -qq upgrade"
	su -c "apt -qq install -y pkg-config bison flex libpq-dev pandoc perl libtool libstdc++6 autoconf automake git build-essential"
	mkdir tmp && cd tmp
	wget http://security.debian.org/debian-security/pool/updates/main/p/postgresql-9.6/libpq5_9.6.10-0+deb9u1_amd64.deb -qq
	su -c "dpkg -i *"
	cd .. && rm -rf tmp
	su -c "apt -qq --fix-broken install"
	su -c "echo \"deb http://ftp.fr.debian.org/debian unstable main contrib non-free\" >> /etc/apt/sources.list"
	su -c "apt -qq update"
	su -c "apt -qq install -y gcc-5/unstable"
	su -c "apt -qq install -y g++-5/unstable"
	su -c "cat /etc/apt/sources.list |grep -v \"$(tail -n 1 /etc/apt/sources.list)\" > /etc/apt/sources.list"
	su -c "apt -qq update"
fi


# Regex from https://github.com/semver/semver/issues/232
reg='^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(-(0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(\.(0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*)?(\+[0-9a-zA-Z-]+(\.[0-9a-zA-Z-]+)*)?$'

echo "Fetching the sources.."
git clone https://github.com/stellar/stellar-core -q &>/dev/null
cd stellar-core/
echo "Which version do you want to build ? (default : 9.2.0)"
read version
if ! [[ $version =~ $reg ]] ; then
	version='9.2.0'
fi
echo "Fetching v$version"
git checkout v$version &>/dev/null
git submodule init &>/dev/null
git submodule update &>/dev/null


echo "Configuring.."
./autogen.sh &>/dev/null
./configure CC=gcc-5 CXX=g++-5 &>/dev/null


echo "Building.."
make &>makeOut
if ! cat makeOut|grep -Fq "error"; then 
        echo "Succesfully compiled"
	echo "Running the tests.."
	make check &>testsOut
	if cat testsOut |grep -Fq "All tests passed"; then
		echo "All tests passed"
		su -c "make install"
	else
		echo "One test did not pass"
		cat testsout
	fi
	rm -rf testsOut
else
	echo "An error occured while compiling, here is the error message :"
	tail -n 20 makeOut
fi
rm -rf makeOut
