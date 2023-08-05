from setuptools import setup

Version = "v1.0.9"

setup(
    name="niobuild",
    version=Version,
    # install_requires=["conan==1.58.0"],
    entry_points = {
        'console_scripts': [
            'niobuild = conannio.build:main'
        ]
    }
)
