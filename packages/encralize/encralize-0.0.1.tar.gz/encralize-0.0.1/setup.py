from distutils.core import setup

setup(
    name = "encralize",
    packages = ["encralize"],
    version = "0.0.1",
    license = "gpl-3.0",
    description = "A simple package to safely serialize and encrypt data",
    author = "Silvio Amuntenci",
    author_email = "amuntenci.silvio@gmail.com",
    url = "https://github.com/Malasaur/encralize",
    download_url = "https://github.com/Malasaur/encralize/archive/refs/tags/v_0.0.1.tar.gz",
    keywords = ["serialization", "encryption"],
    install_requires = ["cryptography"],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ]
)