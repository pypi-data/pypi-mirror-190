#  -*- coding: utf-8 -*-
"""

Author: Rafael R. L. Benevides
Date: 1/26/23

"""

# from setuptools import Extension, setup
# from setuptools.command.build_ext import build_ext as _build_ext
# from pathlib import Path
#
# import numpy
#
#
# smet_dirpath = Path('smet')
#
# # ========== ========== ========== ========== ========== ========== sofa
# sofa_src_files = [str(file.relative_to(smet_dirpath.parent)) for file in (smet_dirpath / 'sofa' / 'src').glob('*.c') if file.stem != 't_sofa_c']
#
# # ========== ========== ========== ========== ========== ==========
# extensions = []
#
# for path in smet_dirpath.glob('**/*.pyx'):
#
#     name = str(path.with_suffix('').relative_to(smet_dirpath.parent)).replace('/', '.')
#     source = str(path.relative_to(smet_dirpath.parent))
#     # source = str(path.with_suffix('.c').relative_to(smet_dirpath.parent))
#
#     print(name, '\t', source)
#
#     if path.stem == 'wrap':
#         ext = Extension(name, [source] + sofa_src_files)
#     else:
#         ext = Extension(name, [source])
#
#     extensions.append(ext)
#
#
# # ========== ========== ========== ========== ========== ==========
# class build_ext(_build_ext):
#     def finalize_options(self):
#         _build_ext.finalize_options(self)
#         # Prevent numpy from thinking it is still in its setup process:
#         if hasattr(__builtins__, '__NUMPY_SETUP__'):
#             __builtins__.__NUMPY_SETUP__ = False
#         import numpy
#         self.include_dirs.append(numpy.get_include())
#
# # ========== ========== ========== ========== ========== ==========
# setup(
#     ext_modules=extensions,
#     # include_dirs=[numpy.get_include()],
#     cmdclass={'build_ext': build_ext},
#     # zip_safe=False,
# )

# from setuptools import Extension, setup  # must be on top
#
# import numpy
# from Cython.Build import cythonize
# from pathlib import Path
#
#
# cython_compiler_directives = {
#     'language_level': '3',
#     'embedsignature': True,
#     'cdivision': True,
#     'boundscheck': False,
#     'wraparound': False,
#     'binding': True
# }
# """Refer to
# https://cython.readthedocs.io/en/stable/src/userguide/source_files_and_compilation.html#compiler-directives
# """
#
#
# # ========== ========== ========== ========== ========== ========== sofa
# # sofa_src_dirpath = Path('smet/sofa/src')
# # sofa_src_files = [str(file) for file in sofa_src_dirpath.iterdir()
# #                   if file.suffix == '.c' and file.stem != 't_sofa_c']
#
# # ========== ========== ========== ========== ========== ==========
# # extensions = [
# #     Extension('smet/**/*', ['smet/**/*.pyx']),
# #     # Extension('smet.sofa.wrap', ['smet/sofa/wrap.pyx'] + sofa_src_files),
# # ]
#
# dir_path = Path(__file__).parent / "smet"
#
# for path in dir_path.glob("**/*.pyx"):
#     print(str(path.relative_to(dir_path.parent)))
#
# # ========== ========== ========== ========== ========== ==========
# setup(ext_modules=cythonize('./smet/**/*.pyx',
#                             annotate=True,
#                             compiler_directives=cython_compiler_directives,
#                             include_path=[numpy.get_include()]
#                             ))


from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext as _build_ext
from pathlib import Path

from Cython.Build import cythonize
use_cython = True
ext = '.pyx'

# try:
#     from Cython.Build import cythonize
# except ImportError:
#     use_cython = False
#     ext = '.c'
# else:
#     use_cython = True
#     ext = '.pyx'

# ========== ========== ========== ========== ========== ==========
smet = Path(__file__).parent / 'smet'
extensions = []

for pyxfile in smet.glob('**/*.pyx'):
    name = str(pyxfile.relative_to(smet.parent).with_suffix('')).replace('/', '.')
    source = str(pyxfile.relative_to(smet.parent).with_suffix(ext))

    print(name, '\t\t\t', source)

    extension = Extension(name, [source])
    extensions.append(extension)

if use_cython:
    compiler_directives = {
        'language_level': '3',
        'embedsignature': True,
        'cdivision': True,
        'boundscheck': False,
        'wraparound': False,
        'binding': True
    }

    extensions = cythonize(extensions, compiler_directives=compiler_directives)

setup(
    ext_modules=extensions,
)



