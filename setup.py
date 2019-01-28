import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jsom",
    version="0.0.3",
    author="Slavfox",
    author_email="slavfoxman@gmail.com",
    description="A fast, simple parser for terribly broken JSON",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/slavfox/jsom",
    packages=['jsom', 'jsom.tests'],
    test_suite="jsom.tests",
    keywords='dirty broken json jsom',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: Public Domain",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    license='WTFPL',
    include_package_data=True,
    install_requires=['lark-parser']
)
