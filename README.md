# GtkSourceView 3 for Inkscape 1.x on Windows

A package providing GtkSourceView 3 libraries for Inkscape 1.x on Windows.
GtkSourceView enables Inkscape extensions using the GTK3 python bindings to use
syntax highlighting. Currently only LaTeX is supported in this version for Inkscape
but it can easily be extended to other languages upon request.

## Installation

Download the Installer from the
[release section](https://github.com/textext/gtksourceview-for-inkscape-windows/releases) of this repository and execute it. It will add (not overwrite) some files
to your Inkscape installation so that GtkSourceView is available. If you do not
trust the installer you can use the corresponding zip file also offered in the
release section. Extract its content into `C:\Program Files\Inkscape`.

## Package building

The following information are intended for users who want to build this package.

### File overview

- The script `build_packages.py` basically downloads the msys2 mingw gtksourceview
packages, extracts them and bundels the required stuff needed by Inkscape extensions
in the directory `files`. Additionally it builds two zip packages containing the
required files for the 64 and 32 bit architecture.

- The script `build_installer.nsi` builds installers from the `files` directory
using Nullsoft Scriptable Install System.


### Usage

1. Check the latest available GtkSourceView 3 version on
   http://repo.msys2.org/mingw/i686 (32bit) and http://repo.msys2.org/mingw/x86_64
   (64bit)

2. In `build_packages.py` set the variable `GTKSOURCEVIEW_PACKAGENAME` to the
   corresponding package name, e.g. `gtksourceview3-3.24.11-1`.

3. Run `python build_packages.py`. It will download the necessary files and extract
   what is needed by the Inkscape extensions. This is only a small subset of the
   original mingw GtkSourceView package. Furthermore, it will create the installer
   and uninstaller file lists required by the NSIS installer in step 6.

4. You will find the architecture depending zip packages in the `build` directory.
   The files packaged are in the directory `files` and the content of the
   originally downloaded mingw packages in the `package_content` directory.

5. In `build_installer.nsi` set the variable `ARCHITECTURE` to either 32 or 64
   depending on the architecture you want to build an installer for.

6. Build the installer using Nullsoft Scriptable Install System. You will find the
   installers in the `build` directory.

7. Finally, you can safely delete the `files` and `packages` directories.

