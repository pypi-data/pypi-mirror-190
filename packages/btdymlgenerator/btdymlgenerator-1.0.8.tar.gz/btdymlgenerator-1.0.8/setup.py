from distutils.core import setup
from setuptools import find_packages
with open("README.rst", "r") as f:
    long_description = f.read()
setup(name='btdymlgenerator',  # 包名
      version='1.0.8',  # 版本号
      description='A small example package',
      long_description=long_description,
      author='ddhjy',
      author_email='510893492@qq.com',
      install_requires=[],
      license='BSD License',
      packages=find_packages(exclude=["tests", "docs", "build.sh"]),
      entry_points='''
        [console_scripts]
        btdymlgenerator=btdymlgenerator.main:main
      ''',
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )
