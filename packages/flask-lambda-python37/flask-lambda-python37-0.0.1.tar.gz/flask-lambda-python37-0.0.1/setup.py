from setuptools import setup


with open('README.rst') as f:
    long_description = f.read()

setup(
    name='flask-lambda-python37',
    version='0.0.1',
    description=('Python3.7+ module to make Flask compatible with AWS Lambda'),
    long_description=long_description,
    keywords='flask aws amazon lambda',
    author='Prasad Rajmane',
    author_email='caprasadrajmane@gmail.com',
    url='https://github.com/caprasadrajmane/flask-lambda',
    license='Apache License, Version 2.0',
    py_modules=['flask_lambda'],
    install_requires=['Flask>=2.2.2'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Environment :: Console',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
    ]
)
