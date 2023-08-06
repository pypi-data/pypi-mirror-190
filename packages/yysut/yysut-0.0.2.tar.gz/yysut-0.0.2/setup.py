from setuptools import setup, find_packages
with open('README.md',mode="r",encoding="UTF-8") as f:
    long_description = f.read()
requirements = []
setup(
    name='yysut',
    version='0.0.2',
    author='SuperYY',
    description='YYSuperUtils',
    long_description=long_description,
    long_description_content_type='text/markdown',
    #url='https://github.com/wkmyws/pysut',
    packages=find_packages(),
    install_requires=requirements,
)