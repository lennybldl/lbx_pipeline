name = "lbx_plumber"
version = "1.0.0"
authors = ["Lenny Blondel"]
description = "A python based tool made to manage, keep track, manipulate and perform automated actions."  # noqa E501
requires = ["python-2.7+", "lbx_python-1.0+"]
build_command = "python {root}/install.py {install}"


def commands():
    """Define how the environment is configured."""
    env.PYTHONPATH.append("{root}/src")  # noqa F821 - behaviour of rez-env
