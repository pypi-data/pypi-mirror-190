from setuptools import setup

setup(
    name="maptasker",
    version="1.2.1",
    description="Display your Android device's Tasker configuration from its backup file on a Mac",
    url="https://github.com/mctinker/Map-Tasker",
    author="Michael Rubin",
    author_email="mikrubin@gmail.com",
    license="GNU General Public License v3 or later (GPLv3+)",
    packages=["maptasker"],
    install_requires=[
        "CTkColorPicker==0.3.0",
        "customtkinter==5.0.5",
        "darkdetect==0.8.0",
        "Pillow==9.4.0",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Environment :: MacOS X",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
    ],
)
