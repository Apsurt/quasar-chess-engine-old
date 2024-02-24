from setuptools import setup

__version__ = "0.0.1"

requirements = []
with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="quasar-chess",
    version=__version__,
    description="A infinite chess engine",
    author="Tymon Becella",
    author_email="tymon.becella@gmail.com",
    packages=["quasar", "quasar/chess", "quasar/engine", "quasar/gui"],
    install_requires=requirements,
    cmdclass={},
)