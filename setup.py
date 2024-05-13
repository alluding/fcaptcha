from setuptools import setup

version: str = "1.0.0"

if not version:
    raise RuntimeError("Version is not set!")

setup(
    name="fcaptcha",
    author="alluding",
    version=version,
    url="https://github.com/alluding/fcaptcha",
    license="MIT",
    description="An unofficial Python wrapper for FCaptcha.",
    install_requires=[
        "typing",
        "requests",
        "typing_extensions"
    ],
    python_requires=">=3.8.0",
)
