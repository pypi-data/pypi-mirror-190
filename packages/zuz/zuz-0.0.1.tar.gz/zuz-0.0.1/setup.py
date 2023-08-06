from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["numpy", "pandas"]

setup(
    name="zuz",
    version="0.0.1",
    author="Eyal Gal",
    author_email="eyalgl@gmail.com",
    description="Dezabin aba bitrei zuzei",
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords=[],
    url="https://github.com/gialdetti/zuz",
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    # package_data={"datasets": ["zuz/resources/*"]},
    classifiers=[
        "Programming Language :: Python :: 3.10",
    ],
)
