from setuptools import setup, find_packages

setup(
    name='Matador',
    version='0.0.1',
    author='Owen Campbell',
    author_email='owen.campbell@empiria.co.uk',
    entry_points={
        'console_scripts': [
            'matador = core.management:hello',
        ],
    },
    url='http://www.empiria.co.uk',
    packages=find_packages(),
    license='The MIT License (MIT)',
    description='Change management for Agresso systems',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English'
        ]
    )
