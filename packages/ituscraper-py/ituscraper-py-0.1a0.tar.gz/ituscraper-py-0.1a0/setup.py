from distutils.core import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(name='ituscraper-py',
      version='0.1a',
      description='Python library for scraping data from Istanbul Technical University websites.',
      author="SerhanCeetin",
      author_email="ceetinserhan@gmail.com",
      url="https://github.com/SerhanCeetin/ituscraper-py",
      packages=['ituscraperpy', 'ituscraperpy.sis'],
      install_requires=['requests>=2.20', 'beautifulsoup4>=4.0'],
      license="MIT",
      python_requires=">=3.8",
      long_description=long_description,
      long_description_content_type="text/markdown",
      )
