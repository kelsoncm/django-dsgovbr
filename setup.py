
import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-dsgovbr',
    version='0.1.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    license='MIT License',  #  I am assuming MIT, but you should verify this
    description='Compliance com o https://www.gov.br/ds/home',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://codelab.ifrn.edu.br/dead-zl/ava/integration/django-dsgovbr',
    author='Kelson da Costa Medeiros', # Placeholder, change if needed
    author_email='kelsoncm@gmail.com', # Placeholder, change if needed
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 5.2',  # Assuming compatibility, adjust as needed
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License', # Assuming MIT
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
