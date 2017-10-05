from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='n0library',
    version='0.0.0',
    description='n0stack common library',
    long_description=readme,
    url='https://github.com/n0stack/n0library',
    author='yatuhashi kei',
    author_email='keyansuiya@gmail.com',
    packages=find_packages("n0library")
)
