# SPDX-FileCopyrightText: Copyright (c) 2022 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
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
"""This module provides a Python API for the core C++ API classes.

The `Application` class is the primary class that should be derived from to
create a custom application.

.. autosummary::

    holoscan.core.Application
    holoscan.core.Arg
    holoscan.core.ArgContainerType
    holoscan.core.ArgElementType
    holoscan.core.ArgList
    holoscan.core.ArgType
    holoscan.core.Component
    holoscan.core.ComponentSpec
    holoscan.core.ConditionType
    holoscan.core.Condition
    holoscan.core.Config
    holoscan.core.DLDevice
    holoscan.core.DLDeviceType
    holoscan.core.ExecutionContext
    holoscan.core.Executor
    holoscan.core.Fragment
    holoscan.core.Graph
    holoscan.core.InputContext
    holoscan.core.IOSpec
    holoscan.core.Message
    holoscan.core.Operator
    holoscan.core.OperatorSpec
    holoscan.core.OutputContext
    holoscan.core.Resource
    holoscan.core.Tensor
    holoscan.core.arg_to_py_object
    holoscan.core.arglist_to_kwargs
    holoscan.core.kwargs_to_arglist
    holoscan.core.py_object_to_arg
"""

import os

from ..config import holoscan_lib_path, holoscan_gxf_extensions_path
from ..graphs._graphs import Graph
from ._core import Application as _Application
from ._core import (
    Arg,
    ArgContainerType,
    ArgElementType,
    ArgList,
    ArgType,
    Component,
    ComponentSpec,
    Condition,
    ConditionType,
    Config,
    DLDevice,
    DLDeviceType,
    ExecutionContext,
    Executor,
    PyTensor as Tensor,
)
from ._core import Fragment as _Fragment
from ._core import InputContext, IOSpec, Message
from ._core import Operator as _Operator
from ._core import (
    OperatorSpec,
    OutputContext,
    PyOperatorSpec,
    Resource,
    arg_to_py_object,
    arglist_to_kwargs,
    kwargs_to_arglist,
    py_object_to_arg,
)

__all__ = [
    "Application",
    "Arg",
    "ArgContainerType",
    "ArgElementType",
    "ArgList",
    "ArgType",
    "Component",
    "ComponentSpec",
    "ConditionType",
    "Condition",
    "Config",
    "DLDevice",
    "DLDeviceType",
    "ExecutionContext",
    "Executor",
    "Fragment",
    "Graph",
    "InputContext",
    "IOSpec",
    "Message",
    "Operator",
    "OperatorSpec",
    "OutputContext",
    "Resource",
    "Tensor",
    "arg_to_py_object",
    "arglist_to_kwargs",
    "kwargs_to_arglist",
    "py_object_to_arg",
]


def _load_gxf_extensions(cls):
    import logging

    from ..gxf import load_extensions

    if not hasattr(cls, "_context"):
        raise ValueError("_context must be initialized prior to calling " "_load_gxf_extensions")
    gxf_extension_libs = [
        "libgxf_std.so",
        "libgxf_cuda.so",
        "libgxf_multimedia.so",
        "libgxf_serialization.so",
    ]
    holoscan_gxf_extension_libs = [
        "libaja_source.so",
        "libbayer_demosaic.so",
        "libcustom_lstm_inference.so",
        "libformat_converter.so",
        "libholoviz.so",
        "libmultiai_inference.so",
        "libmultiai_postprocessor.so",
        "libsegmentation_postprocessor.so",
        "libstream_playback.so",
        "libtensor_rt.so",
        "libtool_tracking_postprocessor.so",
        "libvisualizer_icardio.so",
        "libvisualizer_tool_tracking.so",
    ]

    try:
        from ..operators import EmergentSourceOp  # noqa
        holoscan_gxf_extension_libs += ['libemergent_source.so']
    except ImportError:
        pass

    extensions = [os.path.join(holoscan_lib_path, lib) for lib in gxf_extension_libs]
    extensions += [
        os.path.join(holoscan_gxf_extensions_path, lib) for lib in holoscan_gxf_extension_libs
    ]
    # Note: can only add a given extension once, otherwise will get:
    #       ValueError: GXF_FACTORY_DUPLICATE_TID
    # Note: loading them one at a time to print adequate warning
    for ext in extensions:
        try:
            load_extensions(cls._context, [ext], [], "")
        except ValueError as e:
            e_string = f"{type(e).__name__}: {e}"
            if not os.path.exists(ext):
                logging.warning(f"Could not find the GXF extension: {ext}. {e_string}")
            else:
                logging.warning(f"Could not load the GXF extension: {ext}. {e_string}")

class Application(_Application):
    def __init__(self, *args, **kwargs):
        # It is recommended to not use super()
        # (https://pybind11.readthedocs.io/en/stable/advanced/classes.html#overriding-virtual-functions-in-python)
        _Application.__init__(self, *args, **kwargs)
        # create an Executor and retrieve its context

        self._context = self.executor.context_uint64
        _load_gxf_extensions(self)

    # If we created a context via `gxf.context_create` then we would need to
    # call `gxf.context_destroy` in a destructor. However, in the __init__
    # here, the C++ API creates the GXFExecutor and its context and the
    # C++ object will also take care of the context deletion.

    # def __del__(self):
    #    context_destroy(self._context)


# copy docstrings defined in core_pydoc.hpp
Application.__doc__ = _Application.__doc__
Application.__init__.__doc__ = _Application.__init__.__doc__


class Fragment(_Fragment):
    def __init__(self, *args, **kwargs):
        # It is recommended to not use super()
        # (https://pybind11.readthedocs.io/en/stable/advanced/classes.html#overriding-virtual-functions-in-python)
        _Fragment.__init__(self, *args, **kwargs)
        # create an Executor and retrieve its context

        self._context = self.executor.context_uint64
        _load_gxf_extensions(self)


# copy docstrings defined in core_pydoc.hpp
Fragment.__doc__ = _Fragment.__doc__
Fragment.__init__.__doc__ = _Fragment.__init__.__doc__


class Operator(_Operator):
    def __init__(self, *args, **kwargs):
        # It is recommended to not use super()
        # (https://pybind11.readthedocs.io/en/stable/advanced/classes.html#overriding-virtual-functions-in-python)
        _Operator.__init__(self, self, *args, **kwargs)
        # Create a PyOperatorSpec object and pass it to the C++ API
        spec = PyOperatorSpec(fragment=self.fragment, op=self)
        self.spec = spec
        # Call setup and initialize methods in PyOperator class
        self.setup(spec)
        self.initialize()

    def setup(self, spec: OperatorSpec):
        """Default implementation of setup method."""
        pass


# copy docstrings defined in core_pydoc.hpp
Operator.__doc__ = _Operator.__doc__
Operator.__init__.__doc__ = _Operator.__init__.__doc__
# TODO: remove from core_pydoc.hpp and just define docstrings in this file?
