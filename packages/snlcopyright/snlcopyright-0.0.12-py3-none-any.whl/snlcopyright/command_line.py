import pkg_resources  # part of setup tools

# from typing import Final

# Reference:
# https://setuptools.pypa.io/en/latest/userguide


# module_name: Final[str] = "snlcopyright"  # postpone Final until 3.9 is required
module_name: str = "snlcopyright"  # be D.R.Y.


def commands() -> bool:  # This is a an entry point in pyproject.toml
    """Echos to the available command line entry points."""
    print("------------")
    print(f"{module_name}")
    print("------------")
    print(
        f"This is the command line interface help for Sandia National Laboratories {module_name} Python module."
    )
    print("Available commands:")
    print("commands           (this command)")
    print(
        "copyright          Appends contents of `copyright.txt` to .py files in the cwd, recursively."
    )
    print(
        "copyright-delete   Deletes contents of `copyright.txt` from .py files in cwd, recursively."
    )
    print("copyright-info     Describes the installation details.")
    print("copyright-show     Echos the `copyright.txt` contents to the terminal.")
    print(
        "copyright-status   Shows whether or not the copyright block was found in a .py file in the cwd, recursively."
    )
    print("copyright-version  Prints the semantic verison of the current installation.")

    return True


def copyright_info() -> bool:  # This is a an entry point in pyproject.toml
    """Echos the installation details and dependencies."""
    dist_info = pkg_resources.require(module_name)  # distribution information
    print(f"{module_name} installation details and dependencies:")

    da = dist_info[0]  # distribution attributes of the module

    print(f"module name: {da.project_name}")
    print(f"location: {da.location}")
    print(f"version: {da.version}")

    def project_attribute(attribute):
        return attribute.project_name.lower()

    # Now sort the dist_info list in place
    dist_info.sort(key=project_attribute)  # TODO: sort appears to be deprecated

    print("full stack:")
    for item in dist_info:
        print(f"- {item}")

    return True


def copyright_version() -> str:  # This is a an entry point in pyproject.toml
    """Echos version details of the copyright module."""
    da = pkg_resources.require(module_name)[0]  # dist_info_distribution

    print(f"{module_name} version:")
    ver = da.version
    return ver


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
