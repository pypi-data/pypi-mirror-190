from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name="diki_scraper",
    version=1.3,
    license="MIT",
    author="Michał Pawłowski",
    author_email="<michal.paw000@gmail.com>",
    url='https://github.com/mepavv/diki_scraper',
    description='A library for generating diki.pl ENG-PL translations',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['requests', 'beautifulsoup4'],
    keywords=['scraper', 'api', 'translation', 'polish', 'english'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)