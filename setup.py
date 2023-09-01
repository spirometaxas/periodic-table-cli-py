from setuptools import setup

def get_readme():
    with open('README.md', encoding='utf8') as f:
        return f.read()

setup(
  name = 'periodic-table-cli',
  packages = ['periodic_table_cli'],
  version = '0.0.2',
  license='MIT',
  description = '[BETA] An interactive Periodic Table of Elements app for the console!',
  long_description_content_type='text/markdown',
  long_description=get_readme(),
  author = 'Spiro Metaxas',
  author_email = 'spirometaxas@outlook.com',
  url = 'https://spirometaxas.com/projects/periodic-table-cli/',
  download_url = 'https://github.com/spirometaxas/periodic-table-cli-py/archive/refs/tags/v0.0.2.tar.gz',
  keywords = [ 'Periodic Table', 'Periodic Table of Elements', 'periodic', 'periodic-table-cli', 'Chemistry', 'elements', 'atoms', 'atomic', 'cli', 'console', 'terminal', 'shell', 'unicode' ],
  entry_points={'console_scripts': ['periodic-table-cli=periodic_table_cli.cli:main']},
  classifiers=[
    'Development Status :: 4 - Beta',

    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',

    'Topic :: Scientific/Engineering :: Chemistry',

    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent',
  ],
  include_package_data=True,
  python_requires='>=3.0',
)