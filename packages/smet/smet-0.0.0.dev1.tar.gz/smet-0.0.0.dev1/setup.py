#  -*- coding: utf-8 -*-
"""

Author: Rafael R. L. Benevides
Date: 1/26/23

"""

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext
from pathlib import Path

import numpy


smet_dirpath = Path('smet')

# ========== ========== ========== ========== ========== ========== sofa
sofa_src_files = [str(file) for file in (smet_dirpath / 'sofa' / 'src').glob('*.c') if file.stem != 't_sofa_c']

# ========== ========== ========== ========== ========== ==========
extensions = []

for path in smet_dirpath.glob('**/*.pyx'):

    name = str(path.with_suffix('').relative_to(smet_dirpath)).replace('/', '.')
    source = str(path.with_suffix('.c'))

    if path.stem == 'wrap':
        ext = Extension(name, [source] + sofa_src_files)
    else:
        ext = Extension(name, [source])

    extensions.append(ext)

# ========== ========== ========== ========== ========== ==========
setup(
    ext_modules=extensions,
    include_dirs=[numpy.get_include()],
    cmdclass={'build_ext': build_ext}
)
