from setuptools import setup
from setuptools import find_packages

# read the contents of your README file for long_description
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='bbcpy',
      version='0.1.1',
      description='A novel Python BCI toolbox',
      url='https://github.com/bbcpy/bbcpy',
      author='Neurotechnology Group TU Berlin',
      author_email='bbcpy@tu-berlin.de',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'scikit-learn', 'pyriemann', 'numpy', 'scipy', 'matplotlib', ''
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      extras_require=dict(tests=['pytest']),
      zip_safe=False,
      long_description=long_description,
      long_description_content_type='text/markdown'
      )
