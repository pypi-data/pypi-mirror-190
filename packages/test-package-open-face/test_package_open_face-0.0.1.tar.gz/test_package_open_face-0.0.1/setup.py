import setuptools

with open("README.md", "r") as fh:
    description = fh.read()

setuptools.setup(
    name="test_package_open_face",
    version="0.0.1",
    author="pargim",
    author_email="mohan.tita@gmail.com",
    packages=["test_package_open_face"],
    description="A sample test package",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/mohankashyap/test-tackage",
    license='MIT',
    python_requires='>=3.6',
    install_requires=[]
)
