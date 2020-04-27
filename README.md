# GtkSourceView for Inkscape 1.0 on Windows

Add gtksourceview libraries for Inkscape on Windows providing Syntax highlighting 
for LaTeX.

- The script `build_packages.py` basically downloads the msys2 mingw gtksourceview
packages, extracts them and bundels the required stuff needed by Inkscape extensions
that need syntax highlighting for LaTeX.

- The script `build_installer.nsi` builds installer files using Nullsoft Scriptable
 Install System.


