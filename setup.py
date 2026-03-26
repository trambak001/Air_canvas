"""
setup.py – Package configuration for Air Canvas.

Install in development mode:
    pip install -e .

Build a distribution:
    python setup.py sdist bdist_wheel
"""

from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="air-canvas",
    version="1.0.0",
    author="trambak001",
    author_email="",
    description="Touchless air drawing using hand gesture recognition (OpenCV + MediaPipe)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/trambak001/Air_canvas",
    packages=find_packages(exclude=["tests*", "demo*"]),
    python_requires=">=3.8",
    install_requires=[
        "opencv-python>=4.8.0",
        "mediapipe>=0.10.9,<0.11.0",
        "numpy>=1.24.0",
    ],
    entry_points={
        "console_scripts": [
            "air-canvas=handop:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
    keywords="opencv mediapipe hand-tracking gesture-recognition air-canvas drawing",
)
