from setuptools import setup

setup(
    name='wiuppy',
    version='1.0.0',
    description="A Python3 client for the Where's It Up? API",
    url='https://github.com/WonderNetwork/wiuppy',
    author='WonderNetwork',
    author_email='support@wheresitup.com',
    license='MIT',
    keywords=['api', 'wheresitup', 'wondernetwork', 'wonderproxy'],
    packages=['wiuppy'],
    install_requires=['requests'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
