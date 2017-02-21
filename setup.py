from setuptools import setup, find_packages
with open('noselfs/meta.py') as f:
    exec(f.read())

setup(
    name='noselfs',
    version=__version__,
    packages=find_packages(exclude=['tests']),
    description='A nosetest add-on that gets lfs files',
    author='Grant Stephens',
    author_email='grant@stephens.co.za',
    scripts=[],
    install_requires=[
        'nose',
    ],
    license='MIT',
    url='https://github.com/grantstephens/noselfs',
    download_url='https://github.com/grantstephens/noselfs/tarball/%s'
        % (__version__, ),
    keywords='nose test lfs',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    extras_require={
        'test':  ['requests-mock>=0.7.0', 'nose'],
        }
)
