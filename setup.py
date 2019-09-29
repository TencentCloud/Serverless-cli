# -*- coding: utf-8 -*-

import io
import re
import os
import platform
from subprocess import call
from setuptools import setup, find_packages


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', os.linesep)
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


def read_requirements(req='requirements.txt'):
    content = read(os.path.join(req))
    return [line for line in content.split(os.linesep)
            if not line.strip().startswith('#')]


def read_version():
    content = read(os.path.join(
        os.path.dirname(__file__), 'tcfcli', 'cmds', 'cli', '__init__.py'))
    return re.search(r"__version__ = '([^']+)'", content).group(1)


#
# installed exec shell, set scf command completion
#
class post_install():
    def run(self):
        systemName = platform.system()
        if systemName.lower() == 'linux':
            call(['./scf_complete.sh'],
                 cwd=self.install_lib + 'packagename')


cmd_name = "scf"

setup(
    name='scf',
    version=read_version(),
    packages=find_packages(),
    description='This is a local tools for SCF.',
    long_description=io.open('README.md', encoding='utf-8').read(),
    author='Tencent Cloud',
    url='https://github.com/tencentyun/scfcli.git',
    maintainer_email="qcloud_middleware@qq.com",
    license="Apache License 2.0",
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
    entry_points={
        'console_scripts': [
            '{}=tcfcli.cmds.cli.cli:cli'.format(cmd_name)
        ]
    },
    install_requires=read_requirements('requirements.txt'),
    include_package_data=True,
)


