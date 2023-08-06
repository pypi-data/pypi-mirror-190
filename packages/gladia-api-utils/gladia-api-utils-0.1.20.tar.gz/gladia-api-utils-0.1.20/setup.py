from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


REQUIREMENTS = ["PyYAML",
                "pytest",
                "requests",
                "scikit-image",
                "Pillow",
                "numpy",
                "xtract",
                "gdown",
                "python-magic",
                "GitPython",
                "pandas",
                "lxml",
                "fastapi-utils",
                "googledrivedownloader",
                "opencv-python",
                "python-forge",
                "python-multipart",
                "tritonclient",
                "tritonclient[http]"]


setup(
    name="gladia-api-utils",
    version="0.1.20",
    description="Utils for Gladia APIs Framework",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    author="Jean-Louis Queguiner",
    author_email="jlqueguiner@gladia.io",
    keywords="ai api fastapi artificial_intelligence gladia",
    license="MIT",
    packages=[
        "gladia_api_utils",
        "gladia_api_utils.tester",
        "gladia_api_utils.tester.utils",
        "gladia_api_utils.triton_helper",
        "gladia_api_utils.deepspeed_helper",
        "gladia_api_utils.inpainting_helper",
        "gladia_api_utils.model_architectures",
    ],
    install_requires=REQUIREMENTS,
    include_package_data=True,
    zip_safe=False,
)

# need sudo apt-get install git-lfs or brew install git-lfs
