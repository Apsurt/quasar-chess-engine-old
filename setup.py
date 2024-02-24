from setuptools import setup
from quasar import __version__

requirements = []
with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="quasar",
    version=__version__,
    description="A infinite chess engine",
    author="Tymon Becella",
    author_email="tymon.becella@gmail.com",
    packages=["quasar", "quasar/chess", "quasar/engine", "quasar/gui"],
    install_requires=requirements,
    cmdclass={},
    license="MIT",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    python_requires=">=3.8",

)