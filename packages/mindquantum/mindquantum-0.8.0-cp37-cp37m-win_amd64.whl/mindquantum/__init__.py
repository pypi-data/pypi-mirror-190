# Copyright 2021 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
""".. MindQuantum package."""


# start delvewheel patch
def _delvewheel_init_patch_1_1_2():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'mindquantum.libs'))
    is_pyinstaller = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
    if sys.version_info[:2] >= (3, 8) and not os.path.exists(os.path.join(sys.base_prefix, 'conda-meta')) or sys.version_info[:2] >= (3, 10):
        if not is_pyinstaller or os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        from ctypes import WinDLL
        load_order_filepath = os.path.join(libs_dir, '.load-order-mindquantum-0.8.0')
        if not is_pyinstaller or os.path.isfile(load_order_filepath):
            with open(os.path.join(libs_dir, '.load-order-mindquantum-0.8.0')) as file:
                load_order = file.read().split()
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if not is_pyinstaller or os.path.isfile(lib_path):
                    WinDLL(lib_path)


_delvewheel_init_patch_1_1_2()
del _delvewheel_init_patch_1_1_2
# end delvewheel patch



import os
import sys
import warnings

from .mqbackend import logging

# isort: split

from . import algorithm, config, core, engine, framework, io, simulator, utils
from .algorithm import *
from .config import *
from .core import *
from .core import gates, operators
from .framework import *
from .io import *
from .simulator import *
from .utils import *

if sys.version_info < (3, 8):  # pragma: no cover
    from importlib_metadata import PackageNotFoundError, version
else:  # pragma: no cover
    from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("mindquantum")
    __version_info__ = tuple(__version__.split('.'))
    __all__ = ['__version__', '__version_info__']
except PackageNotFoundError:
    __all__ = []

__all__.extend(core.__all__)
__all__.extend(algorithm.__all__)
__all__.extend(utils.__all__)
__all__.extend(simulator.__all__)
__all__.extend(framework.__all__)
__all__.extend(io.__all__)
__all__.extend(config.__all__)
__all__.sort()


try:
    import mindquantum.experimental

    _orig_enable_logging = logging.enable
    _orig_disable_logging = logging.disable

    def _enable_logging(level):
        _orig_enable_logging(level)
        if hasattr(mindquantum.experimental, 'logging'):
            mindquantum.experimental.logging.enable(level)

    def _disable_logging():
        _orig_disable_logging()
        if hasattr(mindquantum.experimental, 'logging'):
            mindquantum.experimental.logging.disable()

    logging.enable = _enable_logging
    logging.disable = _disable_logging
except ImportError:
    pass