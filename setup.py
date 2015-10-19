from setuptools import setup
import bravado_bitjws

classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development :: Libraries",
]

setup(
    name="bravado-bitjws",
    version=bravado_bitjws.version,
    description="Library for accessing Swagger-enabled API's with bitjws authentication.",
    author='Ira Miller',
    author_email='ira@deginner.com',
    url="https://github.com/deginner/bravado-bitjws",
    license='MIT',
    classifiers=classifiers,
    include_package_data=True,
    packages=["bravado_bitjws"],
    setup_requires=['pytest-runner'],
    install_requires=[
        "bravado-core >= 3.0.2",
        "bravado >= %s" % bravado_bitjws.version,
        "bitjws >= 0.5.3",
    ],
    tests_require=['pytest', 'pytest-cov']
)
