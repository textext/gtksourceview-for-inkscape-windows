#! python3
# Script downloading mingw gtksourceview packages and building a package
# which integrates gtksourceview with LaTeX syntax highlighting into
# Inkscape for Windows. Additionally, installer and uninstaller file
# lists are created for NSIS install system.
#
# Download addresses for the gtksourceviewpackages:
# 32bit:
# http://repo.msys2.org/mingw/i686/mingw-w64-i686-gtksourceview3-3.24.11-1-any.pkg.tar.xz
# 64bit:
# http://repo.msys2.org/mingw/i686/mingw-w64-x86_64-gtksourceview3-3.24.11-1-any.pkg.tar.xz

import urllib.request as ur
import urllib.error as ue
import shutil as sh
import tarfile as tf
import zipfile as zf
from contextlib import contextmanager
import os
import sys

GTKSOURCEVIEW_PACKAGENAME = "gtksourceview3-3.24.11-1"
PACKAGE_BASE_NAME = "GTKSourceView-Inkscape-1.0"
HTTP_ADDRESS = "http://repo.msys2.org/mingw"
MINGW_BASE_NAME = "mingw-w64"
MINGW_SUFFIX = "any.pkg.tar.xz"
ARCH32Bit = "32bit"
ARCH64Bit = "64bit"
ARCHSUFFIXES = {ARCH32Bit: "i686", ARCH64Bit: "x86_64"}
PACKAGE_BASE_DIR_NAME = 'package_content'
FILE_BASE_DIR_NAME = 'files'
BUILD_DIR_NAME = 'build'

# The minimum set of files we need for gtksourceview to work for LaTeX code
REQUIRED_FILES = ['bin/libgtksourceview-3.0-1.dll',
                  'lib/girepository-1.0/GtkSource-3.0.typelib',
                  'share/gtksourceview-3.0/language-specs/def.lang',
                  'share/gtksourceview-3.0/language-specs/language.dtd',
                  'share/gtksourceview-3.0/language-specs/language.rng',
                  'share/gtksourceview-3.0/language-specs/language2.rng',
                  'share/gtksourceview-3.0/language-specs/latex.lang',
                  'share/gtksourceview-3.0/language-specs/R.lang',
                  'share/gtksourceview-3.0/styles/classic.xml',
                  'share/gtksourceview-3.0/styles/styles.rng']

# Set this to False for debugging purposes if you have already downlaoded the gtksourceview-package
DoDownload = False

@contextmanager
def working_dir(dirname):
    old_dir = os.getcwd()
    os.chdir(dirname)
    try:
        yield
    finally:
        os.chdir(old_dir)


def create_fresh_directory(dirname):
    print('Creating fresh directory {0}'.format(dirname))
    # Recursively delete directory if it exists
    if os.path.exists(dirname):
        print('   Directory {0} exists. Trying to delete it...'.format(dirname))
        try:
            sh.rmtree(dirname)
            print('      Successfully deleted existing directory!')
        except OSError as excpt:
            print('      Failed to delete directory {0}!'.format(dirname))
            print('      Detailed error message')
            print('      {0}'.format(excpt))
            sys.exit()

    # Create the directory
    try:
        os.makedirs(dirname)
        print('   Successfully created directory!')
    except OSError as excpt:
        print('   Failed to create directory {0}!'.format(dirname))
        print('   Detailed error message')
        print('   {0}'.format(excpt))
        sys.exit()


create_fresh_directory(BUILD_DIR_NAME)
for arch in [ARCH32Bit, ARCH64Bit]:
    print('==========================================')
    print('Building for architecture {0}'.format(ARCHSUFFIXES[arch]))
    print('==========================================')
    package_name = '{0}-{1}-{2}-{3}'.format(MINGW_BASE_NAME, ARCHSUFFIXES[arch], GTKSOURCEVIEW_PACKAGENAME, MINGW_SUFFIX)

    # Download mingw package
    if DoDownload:
        url = '{0}/{1}/{2}'.format(HTTP_ADDRESS, ARCHSUFFIXES[arch], package_name)
        try:
            print('Trying to download {0} from {1} ...'.format(package_name, url))
            ur.urlretrieve(url, package_name)
            print('   Success!')
        except ue.URLError as excpt:
            print('   Failed to download {0} from {1}!'.format(package_name, url))
            print('   Detailed error message:')
            print('   {0}'.format(excpt))

    # Extract mingw package
    package_dir_name = os.path.join(PACKAGE_BASE_DIR_NAME, arch)
    file_dir_name = os.path.join(FILE_BASE_DIR_NAME, arch)
    create_fresh_directory(package_dir_name)
    create_fresh_directory(file_dir_name)
    print ('Extracting package {0}'.format(package_name))
    with tf.open(package_name) as f:
        f.extractall(package_dir_name)
    print('   Success!')

    # Collect the files we need in Inkscape
    print('Collection required files from {0}...'.format(package_name))
    for filename in REQUIRED_FILES:
        src = os.path.join(package_dir_name, 'mingw32' if arch == ARCH32Bit else 'mingw64', filename)
        dst = os.path.join(file_dir_name, filename)
        dstfolder = os.path.dirname(dst)
        if not os.path.exists(dstfolder):
            os.makedirs(dstfolder)
        print('   {0} -> {1}'.format(src, dst))
        sh.copy(src, dst)

    # Create the installer file list for NSIS installer system
    installer_list_file_name = 'inst_file_list_{0}.txt'.format(arch)
    print('Create installer file list for {0} in {1}'.format(arch, installer_list_file_name))
    with open(installer_list_file_name, 'w') as fh:
        with working_dir(file_dir_name):
            for subdir, _, filenames in os.walk('.', topdown=False):
                if len(filenames) > 0:
                    subdir = subdir[2:] # Remove ./
                    fh.write("   SetOutPath \"$INSTDIR\\" + subdir + "\"\n")
                    for fn in filenames:
                        fh.write("   File \"${FILES_SOURCE_PATH}\\" + subdir + "\\" + fn + "\"\n")
                    fh.write("\n")
    print('   Success!')

    # Create the uninstaller file list for NSIS installer system
    # (From bottom to top so NSIS can delete empty folders!)
    uninstaller_list_file_name = 'uninst_file_list_{0}.txt'.format(arch)
    print('Create uninstaller file list for {0} in {1}'.format(arch, uninstaller_list_file_name))
    with open(uninstaller_list_file_name, 'w') as fh:
        with working_dir(file_dir_name):
            for subdir, _, filenames in os.walk('.', topdown=False):
                subdir = subdir[2:]  # Remove ./
                if len(filenames) > 0:
                    for fn in filenames:
                        fh.write("   Delete \"${FILES_SOURCE_PATH}\\" + subdir + "\\" + fn + "\"\n")
                fh.write("   RMDir \"$INSTDIR\\" + subdir + "\"\n")
                fh.write("\n")
    print('   Success!')

    # Create ZIP-Packages
    zip_file_name = os.path.join(BUILD_DIR_NAME, '{0}-{1}.zip'.format(PACKAGE_BASE_NAME, arch))
    print('Create zip package {0}'.format(zip_file_name))
    with zf.ZipFile(zip_file_name, 'w') as fh:
        with working_dir(file_dir_name):
            for subdir, _, filenames in os.walk('.'):
                for filename in filenames:
                    fh.write(os.path.join(subdir, filename))
    print('   Success!')
