from setuptools import setup, find_packages

setup(
    name="diki_scraper",
    version=1.0,
    author="mepavv",
    author_email="<michal.paw000@gmail.com>",
    description='Library for generating Diki.pl ENG-PL translations',
    packages=find_packages(),
    install_requires=['requests', 'beautifulsoup4'],
    keywords=['scrapper', 'api', 'translation', 'polish', 'english'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)