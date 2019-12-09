import os
import sys
from distutils.core import setup
from distutils.extension import Extension

import pysam
from Cython.Build import cythonize
from Cython.Distutils import build_ext

ROOT = os.path.dirname(__file__)
BRI = os.path.join(ROOT, 'src/bri/src')

setup(
    name="camembert",
    packages=["camembert"],
    version='0.0.1',
    description='Python interface to bri',
    author='Matej Usaj',
    author_email='m.usaj@utoronto.ca',
    url='https://github.com/usajusaj/camembertpy',
    download_url='https://github.com/usajusaj/camembertpy/archive/master.zip',
    keywords=['bri'],
    cmdclass={"build_ext": build_ext},
    install_requires=[
        'cython',
        'pysam'
    ],
    ext_modules=cythonize([
        Extension(
            name="camembert.bri",
            sources=[
                "src/bri.pyx",
                os.path.join(BRI, 'bri_index.c'),
                os.path.join(BRI, 'bri_get.c')
            ],
            include_dirs=pysam.get_include() + [
                BRI,
                os.path.join(sys.prefix, 'include')
            ],
            extra_link_args=pysam.get_libraries(),
            define_macros=pysam.get_defines(),
            extra_compile_args=['-O3'],
        ),
    ]),
)
