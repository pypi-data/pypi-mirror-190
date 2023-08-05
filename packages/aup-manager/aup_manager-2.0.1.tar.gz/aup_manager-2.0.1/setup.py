from subprocess import check_call
import setuptools
from setuptools.command.install import install


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        check_call(
            "cd aup_manager/static && npm install && npm run compile_sass", shell=True
        )
        install.run(self)


setuptools.setup(
    name="aup_manager",
    python_requires=">=3.9",
    url="https://gitlab.ics.muni.cz/perun-proxy-aai/python/aup-manager.git",
    description="Module for managing AUPs",
    include_package_data=True,
    package_data={"": ["open-api-specification.yaml"]},
    packages=setuptools.find_packages(),
    install_requires=[
        "setuptools",
        "pymongo~=4.2",
        "jsonpatch~=1.22",
        "connexion[swagger-ui]~=2.14",
        "markdown2~=2.4",
        "Flask-pyoidc~=3.11",
        "jwcrypto~=1.4.2",
    ],
    extras_require={
        "perun": ["perun.connector~=3.3"],
    },
    cmdclass={
        "install": PostInstallCommand,
    },
)
