from setuptools import setup

setup(
    name='GFLPBot',
    version='0.1.0',
    packages=['GFLPBot'],
    url='',
    license='MIT',
    author='Addison Wojciechowski',
    author_email='',
    description='',
    scripts=[
        'bin/run',
        'bin/run.bat',
    ],
    install_requires=[
        'discord',
        'aiohttp',
    ]

)
