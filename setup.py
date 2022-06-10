import setuptools
import pepaln

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pepaln",
    version=pepaln.VERSION,
    author="Istvan Albert",
    author_email="istvan.albert@gmail.com",
    description="Peptide Matcher ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/biostars/biostar-handbook-code",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'plac>=1.3',
        'intervaltree',
        'FPDF',
    ],

    python_requires='>=3.6',

)
