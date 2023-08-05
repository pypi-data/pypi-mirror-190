import setuptools

setuptools.setup(
    name="qmse",
    version="0.0.1.4",
    license='MIT',
    author="quantmise",
    author_email="quantmise@naver.com",
    description="qmse",
    long_description=open('README.md').read(),
    url="https://github.com",
    packages=setuptools.find_packages(),
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)