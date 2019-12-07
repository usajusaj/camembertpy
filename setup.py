import os
from distutils.core import setup
from distutils.extension import Extension

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
    # url='https://github.com/usajusaj/segmentation',
    # download_url='https://github.com/usajusaj/segmentation/archive/master.zip',
    # keywords=['mixture', 'model', 'segmentation'],
    # classifiers=[],
    cmdclass={"build_ext": build_ext},
    ext_modules=cythonize([
        Extension(
            name="camembert.bri",
            sources=[
                "src/bri.pyx",
                os.path.join(BRI, 'bri_index.c'),
                os.path.join(BRI, 'bri_get.c')
            ],
            include_dirs=[
                BRI,
            ],
            libraries=['hts'],
            extra_compile_args=[],
            extra_link_args=['-D_FILE_OFFSET_BITS=64']
        ),
    ]),
)
