from setuptools import setup, find_packages
import os

def get_readme():
  f = open('README.md')
  readme = f.read()
  f.close()
  return readme

def get_install_requirements():
  if os.name == 'nt':
    return [ 'windows-curses' ]  # Only install for Windows
  return []

def get_version():
  f = open('periodic_table_cli/version.txt')
  version = f.read()
  f.close()
  return version

setup(
  name = 'periodic-table-cli',
  packages = find_packages(),
  version = get_version(),
  license='MIT',
  description = 'An interactive Periodic Table of Elements app for the console!',
  long_description_content_type='text/markdown',
  long_description=get_readme(),
  author = 'Spiro Metaxas',
  author_email = 'spirometaxas@outlook.com',
  url = 'https://spirometaxas.com/projects/periodic-table-cli/',
  download_url = 'https://github.com/spirometaxas/periodic-table-cli-py/archive/refs/tags/v' + get_version() + '.tar.gz',
  project_urls={
    'Source Code': 'https://github.com/spirometaxas/periodic-table-cli-py',
  },
  keywords = [ 'Periodic Table', 'Periodic Table of Elements', 'periodic', 'periodic-table-cli', 'Chemistry', 'elements', 'atoms', 'atomic', 'cli', 'console', 'terminal', 'shell', 'unicode' ],
  entry_points={'console_scripts': ['periodic-table-cli=periodic_table_cli.cli:main']},
  install_requires=get_install_requirements(),
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Environment :: Console :: Curses',

    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',

    'Topic :: Education',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'Topic :: Scientific/Engineering :: Chemistry',
    'Topic :: Scientific/Engineering :: Medical Science Apps.',
    'Topic :: Terminals',

    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.12',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 2.7',
    'Operating System :: OS Independent',
  ],
  include_package_data=True,
  python_requires='>=2.7',
)