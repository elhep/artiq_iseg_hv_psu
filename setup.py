from setuptools import find_packages, setup

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="artiq_iseg_hv_psu",
    install_requires=required,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "artiq_iseg_hv_psu = artiq_iseg_hv_psu.artiq_iseg_hv_psu:main",
        ],
    },
)
