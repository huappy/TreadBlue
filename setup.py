import setuptools

setuptools.setup(
    name = 'TreadBlue',
    version = '1.0',
    description = 'A speed controller for Bluetooth enabled treadmills',
    author = 'Hap Hausman',
    author_email = 'haphausman@gmail.com',
    packages = setuptools.find_packages(),
    install_requires = [
        "bleak", 
        "PyQt5",
        "PyQt5_sip"
        ],
)