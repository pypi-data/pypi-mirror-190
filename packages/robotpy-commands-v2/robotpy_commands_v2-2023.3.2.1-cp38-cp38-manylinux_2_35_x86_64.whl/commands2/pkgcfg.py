# fmt: off
# This file is automatically generated, DO NOT EDIT

from os.path import abspath, join, dirname
_root = abspath(dirname(__file__))

libinit_import = "commands2._init_impl"
depends = ['wpilib_core', 'wpilibc_interfaces', 'wpilibc', 'wpimath_cpp', 'wpimath_controls', 'wpimath_geometry', 'wpimath_filter', 'wpimath_kinematics', 'wpimath_spline', 'wpiHal', 'wpiutil', 'ntcore']
pypi_package = 'robotpy-commands-v2'

def get_include_dirs():
    return [join(_root, "include"), join(_root, "rpy-include"), join(_root, "src", "include")]

def get_library_dirs():
    return []

def get_library_dirs_rel():
    return []

def get_library_names():
    return []

def get_library_full_names():
    return []