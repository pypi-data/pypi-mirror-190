import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="jrlogo",
    version="0.0.1",
    description="A package for Jieer Edu to teach pc-logo and python",
    author="klarkxy",
    author_email="278370456@qq.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/klarkxy/jieer-logo",
    license="SATA",
    packages=["jrlogo"],
    install_requires=["pillow", "numpy"],
)