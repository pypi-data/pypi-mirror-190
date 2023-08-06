"""This module tests the command_line module."""

from snlcopyright import command_line as cl


def test_commands():
    """This is simple test just to make sure the function code is run."""
    assert cl.commands()


def test_scinfo():
    """This is simple test just to make sure the function code is run."""
    assert cl.copyright_info()


def test_version():
    """Verifies the version specified in pyproject.toml is installed."""
    known = "0.0.12"  # pyproject.toml defines the version
    found = cl.copyright_version()

    assert found == known


"""
Copyright 2023 Sandia National Laboratories

Notice: This computer software was prepared by National Technology and Engineering Solutions of
Sandia, LLC, hereinafter the Contractor, under Contract DE-NA0003525 with the Department of Energy
(DOE). All rights in the computer software are reserved by DOE on behalf of the United States
Government and the Contractor as provided in the Contract. You are authorized to use this computer
software for Governmental purposes but it is not to be released or distributed to the public.
NEITHER THE U.S. GOVERNMENT NOR THE CONTRACTOR MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR ASSUMES
ANY LIABILITY FOR THE USE OF THIS SOFTWARE. This notice including this sentence must appear on any
copies of this computer software. Export of this data may require a license from the United States
Government.
"""
