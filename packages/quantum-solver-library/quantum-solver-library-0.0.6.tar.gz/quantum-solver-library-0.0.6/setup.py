import setuptools

readme = open("./README.md", "r")

setuptools.setup(
    name = "quantum-solver-library",
    version = "0.0.6",
    author = "Andrea Hernández",
    author_email = "alu0101119137@example.com",
    description = "A little quantum toolset developed using Qiskit",
    long_description =  readme.read(),
    long_description_content_type = "text/markdown",
    url = "https://github.com/alu0101119137/quantum-solver",
    project_urls = {
        "Bug Tracker": "https://github.com/alu0101119137/quantum-solver/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6",
    include_package_data=True
)