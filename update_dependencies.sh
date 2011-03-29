#!/bin/sh
DEPS_DIR=`pwd`/third_party

# Remove existing directory.
rm -fr $DEPS_DIR
mkdir -p $DEPS_DIR

# ===== Django SVN =====
cd $DEPS_DIR
svn co http://code.djangoproject.com/svn/django/tags/releases/1.3/django django

# ===== Typogrify SVN =====
cd $DEPS_DIR
svn co http://typogrify.googlecode.com/svn/trunk/typogrify typogrify

# ===== django-contact-form =====
cd $DEPS_DIR
hg clone http://bitbucket.org/ubernostrum/django-contact-form/
mv django-contact-form/contact_form .
rm -fr django-contact-form

# ===== Smartypants =====
cd $DEPS_DIR
curl -o smartypants.py http://web.chad.org/projects/smartypants.py/smartypants.py-1.5_1.6

# ===== akismet.py =====
cd $DEPS_DIR
curl -O http://www.voidspace.org.uk/downloads/akismet.py
