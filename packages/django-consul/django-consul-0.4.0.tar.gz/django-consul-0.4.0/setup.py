import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="django-consul",
    version="0.4.0",
    author="Xujia Li",
    author_email="lixujiacn@outlook.com",
    description="A django app which register django service to consul server.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(
        exclude=[
            'DjangoConsul',
            'manage.py',
            'setup.py'
        ]
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'Django',
        'requests'
    ],
    python_requires='>=3.6'
)
