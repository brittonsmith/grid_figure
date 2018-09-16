from setuptools import setup

setup(name="grid_figure",
      version="1.0",
      description="A utility to set up matplotlib axes for multi-panel plots.",
      author="Britton Smith",
      author_email="brittonsmith@gmail.com",
      license="BSD 3-Clause",
      url="https://github.com/brittonsmith/grid_figure",
      packages=["grid_figure"],
      classifiers=[
          "Development Status :: 2 - Pre-Alpha",
          "Environment :: Console",
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: BSD License",
          "Operating System :: MacOS :: MacOS X",
          "Operating System :: POSIX :: AIX",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python",
          "Topic :: Utilities",
          ],
      install_requires=[
          'matplotlib',
          'numpy'
      ]
)
