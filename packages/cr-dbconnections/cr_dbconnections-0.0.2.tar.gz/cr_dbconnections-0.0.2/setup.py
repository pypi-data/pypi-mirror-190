import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cr_dbconnections",
    version="0.0.2",
    author="Henrique Ortiz",
    author_email="henrique.ortiz@consultaremedios.com.br",
    description="Classes básicas de conexão com bancos de dados.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ConsultaRemedios/cr_dbconnections",
    packages=setuptools.find_packages(),
    install_requires=[
        'pymongo',
        'sqlalchemy',
        'python-dotenv',
        'PyYAML'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)