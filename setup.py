import os
from setuptools import setup

requirements = []
if os.path.exists('requirements.txt'):
    with open('requirements.txt') as f:
        content = f.read()
        requirements = list(filter(lambda c: bool(c), content.split('\n')))


setup(
    name='game-tournament',
    version='0.1.0',
    description='Get tournament updates',
    url='git@github.com:jyothikp/game-tournament.git',
    author='Jyothi',
    author_email='jyothikp9999@gmail.com',
    license='MIT',
    install_requires=requirements,
    packages=['tournament'],
    data_files=[('tournament', ['tournament/config.json'])],
)
