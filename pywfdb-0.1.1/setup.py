from distutils.core import setup
from distutils.extension import Extension
from Pyrex.Distutils import build_ext
import glob, os.path

version = open("version.txt", 'r').read().strip()

################################################################################
## see http://www.physionet.org/physiotools/wfdb.shtml#downloading
## for wfdb source files and help on installing this library on your platform
## or directly http://www.physionet.org/physiotools/wfdb-no-docs.tar.gz


wfdb_header_dir = "./wfdb-10.4.4/lib"       ## modify this first
wfdb_source_dir = "./wfdb-10.4.4/lib"       ## modify this first

source_files = ["annot.c", "signal.c", "wfdbio.c"]
source_files = [os.path.join(wfdb_source_dir, f) for f in source_files]

long_description = \
"""Pywfdb is a Python module which provides interface to WFDB library.
It allows to access PhysioBank databases of physiologic signals
from within Python in a simple and convenient manner."""

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: Healthcare Industry',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: OS Independent',
    'Programming Language :: C',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules'
]


if os.path.exists('MANIFEST'): os.remove('MANIFEST')

try:
    from Pyrex.Distutils import build_ext
    has_pyrex = True
except ImportError:
    has_pyrex = False

if has_pyrex:
    pyx_sources = ['pywfdb/_pywfdb.pyx']
    cmdclass    = {'build_ext': build_ext}
else:
    pyx_sources = ['pywfdb/_pywfdb.c']
    cmdclass    = {}


ext_modules=[
    Extension("pywfdb._pywfdb",
        sources = pyx_sources + source_files,
        include_dirs = [wfdb_header_dir],
        library_dirs = [],
        runtime_library_dirs = [],
        libraries = [],
        extra_compile_args=['-Wno-uninitialized', '-Wno-unused'],
        extra_link_args = [],
        export_symbols = [],
        language = "pyrex",
    ),
]

setup(
    name = 'pywfdb',
    version = version,
    description = "Python interface to WFDB library.",
    long_description=long_description,
    author = 'Filip Wasilewski',
    author_email = 'filipwasilewski@gmail.com',
    url = 'http://www.pybytes.com/pywfdb/',
    download_url = 'http://cheeseshop.python.org/pypi/pywfdb/',
    license = 'GPL',
    ext_modules=ext_modules,
    platforms = ['any'],
    packages = ['pywfdb', 'pywfdb.example'],
    package_dir = {'pywfdb':'pywfdb', 'pywfdb.example':'example'},
    #script_args = ["build_ext"],
    cmdclass = {'build_ext': build_ext},
    classifiers = classifiers, 
)

