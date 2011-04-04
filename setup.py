from distutils.core import setup

setup(
    name='namalizer',
    version='0.1.1',
    description='Normalizes method names according to PEP8.',
    long_description=open('README.md').read(),
    author='Alexander Artemenko',
    author_email='svetlyak.40wt@gmail.com',
    license = 'New BSD License',
    keywords='python library pep8 pep normalizer naming',
    url = 'http://github.com/svetlyak40wt/namalizer/',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    py_modules=['namalizer'],
)
