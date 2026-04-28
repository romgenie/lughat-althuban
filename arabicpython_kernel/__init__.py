"""arabicpython_kernel
B-054: Jupyter kernel for the apython Arabic Python dialect.

Provides the ``ArabicPythonKernel`` class which extends IPython's
``IPythonKernel``, transparently translating .apy source to Python
before execution.

Installation::

    pip install arabicpython[kernel]
    python -m arabicpython_kernel install

Then select "لغة الثعبان (apython)" in the Jupyter kernel picker.
"""

from arabicpython_kernel.kernel import ArabicPythonKernel

__all__ = ["ArabicPythonKernel"]
__version__ = "0.1.0"
