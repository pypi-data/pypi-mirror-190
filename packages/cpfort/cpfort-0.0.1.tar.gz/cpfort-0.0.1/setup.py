import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='cpfort',                           # should match the package folder
    packages=['cpfort'],                     # should match the package folder
    version='0.0.1',                                # important for updates
    license='MIT',                                  # should match your chosen license
    description='cpfort package',
    long_description=long_description,              # loads your README.md
    long_description_content_type="text/markdown",  # README.md is of type 'markdown'
    author='NTNU',
    author_email='kimbienes@gmail.com',
    url='https://github.com/diannekb/cpfort', 
    include_package_data=True,
    keywords=["pypi", "cpfort"], #descriptive meta-data
    classifiers=[                                   # https://pypi.org/classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    
    download_url="https://github.com/diannekb/cpfort/archive/refs/tags/0.0.1.tar.gz",
)