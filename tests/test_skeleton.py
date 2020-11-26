# -*- coding: utf-8 -*-

import pytest
from jci_iot.skeleton import fib

__author__ = "Vinay from MSI WSL"
__copyright__ = "Vinay from MSI WSL"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
