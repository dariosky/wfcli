from distutils.core import setup

setup(
    name='wfcli',
    version='0.2',
    packages=['wfcli'],
    url='https://github.com/dariosky/wfcli',
    license='MIT',
    author='Dario Varotto',
    author_email='dario.varotto@gmail.com',
    description='WebFaction utilities',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: System :: Software Distribution',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='deployment webfaction cli letsencrypt certificate',
    install_requires=['fabric3'],
    console_scripts=['wfcli = wfcli.__main__:main'],
)
