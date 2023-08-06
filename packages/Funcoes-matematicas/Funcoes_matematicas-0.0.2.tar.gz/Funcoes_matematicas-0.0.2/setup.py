from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Funcoes_matematicas",
    version="0.0.2",
    author="Carlos_Falcone",
    author_email="carloseduardo.falcone@gmail.com",
    description="Plotagem de funções matemáticas simples",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carlosfalcone/PacotesPython",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.5',
)