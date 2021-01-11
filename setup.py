import setuptools

with open("README.md", "r") as fh:
    long_description  = fh.read()

with open("VERSION", "r") as fh:
    version = fh.read()

setuptools.setup(
        name='LupSeat',
        version=version,
        scripts=['lupseat'],
        author="Hiroya Gojo",
        author_email="hiroyagojo@gmail.com",
        description="Automatically assigns seats to students in a smart way.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=setuptools.find_packages(),
        package_data={'': ['*']},
        include_package_data=True,
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
)
