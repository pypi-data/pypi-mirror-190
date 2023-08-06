from setuptools import setup, find_packages


VERSION = '0.0.1'
DESCRIPTION = 'Inhibitory Drug Target Analyser'
LONG_DESCRIPTION = 'Viruses, in particular, RNA viruses show increased drug resistance to antivirals that directly act on viral proteins. IDTA module aims to find the candidate drugs/antivirals by using /' \
                   'high-throughput screening of FDA approved drug databases to target historically conserved sequences (HCS) of a given virus.'


setup(
    name='idta',
    version=VERSION,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    author='Faruk Üstünel',
    author_email='<faruk.ustunel@bezmialem.edu.tr>',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['idta/zincdb/*']
    },
    keywords=["drug target","viruses"],
    classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Science/Research",
    "Intended Audience :: Healthcare Industry",
    "Programming Language :: Python :: 3",
    "Operating System :: Unix",
    ]
)