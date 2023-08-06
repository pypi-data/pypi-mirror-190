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
@ 模块 : 科蒂的指令回路
@ 作者 : chenjiancheng
@ 邮箱 : quinn.7@foxmail.com
@ 描述 : 通过 Windows 命令行工具调用科蒂。

"""
import sys


# --------------------------------------------------------------------------
def main():
    command = 'order'
    
    
    # ----------------------------------------------------------------------
    if len(sys.argv) >= 2:
        command = sys.argv[1]
        argv    = sys.argv[2:]


    # ----------------------------------------------------------------------
    if command in ['order', '-order', '-o']:
        print('order')


    # ----------------------------------------------------------------------
    elif command in ['help', '-help', '-h']:
        print('help')
