from setuptools import setup, find_packages

setup(
    name='publishagain_to_pypi',
    version='1.1',
    license='MIT',
    author="SpiralTrain",
    author_email='spiraltrain@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='demo project',
    install_requires=[
          'scikit-learn',
      ],
)
