from setuptools import setup
from distutils.command.install import install

from flytekitplugins.flyin.vscode_lib.decorator import VscodeConfig, download_vscode

PLUGIN_NAME = "flyin"

microlib_name = f"flytekitplugins-{PLUGIN_NAME}"

plugin_requires = ["flytekit>=1.1.0b0,<2.0.0", "jupyter"]

__version__ = "0.0.0+develop"


class CodeServerInstall(install):
    def run(self):
        config = VscodeConfig()
        download_vscode(config)
        install.run(self)


setup(
    name=microlib_name,
    version=__version__,
    author="flyteorg",
    author_email="admin@flyte.org",
    description="This package holds the flyin plugins for flytekit",
    namespace_packages=["flytekitplugins"],
    packages=[
        f"flytekitplugins.{PLUGIN_NAME}",
        f"flytekitplugins.{PLUGIN_NAME}.vscode_lib",
        f"flytekitplugins.{PLUGIN_NAME}.jupyter_lib",
    ],
    cmdclass={'install': CodeServerInstall},
    install_requires=plugin_requires,
    license="apache2",
    python_requires=">=3.8",
    classifiers=[
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={"flytekit.plugins": [f"{PLUGIN_NAME}=flytekitplugins.{PLUGIN_NAME}"]},
)
