#!/bin/bash

PATH=/bin:/usr/bin:/usr/sbin

VERSION=$FANTASTICO_VERSION
WORKDIR=`pwd`

if [ -z $VERSION ]; then
	echo "You must provide a fantastico version to package."
	exit 1
fi

# Publish release code.
echo "Create release tag $VERSION"
git tag -a v$VERSION -m "Fantastico version $VERSION released."

if [ $? -gt 0 ]; then
	exit $?
fi

git push origin v$VERSION

# Publish release documentation.
echo "Create release doc tag $VERSION"
cd ../fantastico-doc
git tag -a v$VERSION-doc -m "Fantastico doc version $VERSION released."

if [ $? -gt 0 ]; then
	exit $?
fi

git push origin v$VERSION-doc

if [ $? -gt 0 ]; then
	exit $?
fi


# Publish Fantastico on PyPi.
cd $WORKDIR/doc

echo "Removing previous doc build."
rm -Rf build
mkdir build
cd build
ln -s ../../../fantastico-doc/doctrees doctrees
ln -s ../../../fantastico-doc/epub epub
ln -s ../../../fantastico-doc/html html
ln -s ../../../fantastico-doc/latex latex

cd $WORKDIR
cp -f doc/source/changes.rst CHANGES.txt

cat README.txt CHANGES.txt >> README_NEW.txt
rm -f README.txt
rm CHANGES.txt
mv README_NEW.txt README.txt

echo "Publishing Fantastico $VERSION on PyPi."
python3 setup.py clean sdist register upload

if [ $? -gt 0 ]; then
	exit $?
fi

echo "Fantastico $VERSION released successfully."