import os
from setuptools import setup

requirements = []
if os.path.exists('requirements.txt'):
    with open('requirements.txt') as f:
        content = f.read()
        requirements = list(filter(lambda c: bool(c), content.split('\n')))


setup(
    name='game-tournament',
    version='0.10.0',
    description='Get tournament updates',
    url='https://github.com/jyothikp/game-tournament',
    author='Jyothi',
    author_email='jyothikp9999@gmail.com',
    license='MIT',
    install_requires=requirements,
    packages=['tournament'],
    package_data={
        'tournament': ['config.json'],
    },
)
