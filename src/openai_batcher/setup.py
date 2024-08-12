from setuptools import setup, find_packages

setup(
    name="openai-batcher",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # List your dependencies here
        "openai",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A package for batching OpenAI API requests",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/openai-batcher",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    license="Apache License 2.0",
    python_requires=">=3.6",
)
