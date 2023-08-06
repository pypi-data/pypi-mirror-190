# ╔══════════════════════════════════════════════════════════════════════════╗
# ║ Copyright 2022. quinn.7@foxmail.com All rights reserved.                 ║
# ║                                                                          ║
# ║ Licensed under the Apache License, Version 2.0 (the "License");          ║
# ║ you may not use this file except in compliance with the License.         ║
# ║ You may obtain a copy of the License at                                  ║
# ║                                                                          ║
# ║ http://www.apache.org/licenses/LICENSE-2.0                               ║
# ║                                                                          ║
# ║ Unless required by applicable law or agreed to in writing, software      ║
# ║ distributed under the License is distributed on an "AS IS" BASIS,        ║
# ║ WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. ║
# ║ See the License for the specific language governing permissions and      ║
# ║ limitations under the License.                                           ║
# ╚══════════════════════════════════════════════════════════════════════════╝
"""
@ 模块 : CotyBot-Setup
@ 作者 : chenjiancheng
@ 邮箱 : quinn.7@foxmail.com
@ 描述 : PIP package manager build script.

"""
from setuptools import setup
from setuptools import find_packages
from src.cotyBot import CotyBotInformation


LEGAL_PY_VERSION = [
    'Programming Language :: Python :: 3.10',
]

INSTALL_REQUIRES = [
    'playwright',
    'flask',
    'websockets-routes',
]

with open('README.md', 'r', encoding='UTF-8') as file:
    LONG_DESCRIPTION = file.read()

setup(
    name                          = CotyBotInformation.Name, 
    version                       = CotyBotInformation.Version, 
    author                        = CotyBotInformation.Author, 
    author_email                  = CotyBotInformation.Email, 
    description                   = CotyBotInformation.Desc,
    keywords                      = CotyBotInformation.Keywords,
    url                           = CotyBotInformation.Url,
    classifiers                   = LEGAL_PY_VERSION,
    install_requires              = INSTALL_REQUIRES,
    long_description              = LONG_DESCRIPTION, 
    long_description_content_type = 'text/markdown',
    packages                      = find_packages('src'), 
    package_dir                   = {'' : 'src'},
    
    entry_points = {
        'console_scripts':[
            'coty = cotyBot.cotyBotConsole:main',
        ],
    },
)
