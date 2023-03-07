import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='smith-waterman-affine-gap',
    version='0.0.1',
    author='Suchen Zheng',
    author_email='suzy897897@gmail.com',
    description='function for smith-waterman local alignment with affine gap',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/suchzheng2/smith-waterman-affine-gap',
    license='MIT',
    packages=['smith-waterman-affine-gap'],
)
