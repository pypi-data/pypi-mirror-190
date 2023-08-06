# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_whateat_pic']

package_data = \
{'': ['*'], 'nonebot_plugin_whateat_pic': ['drink_pic/*', 'eat_pic/*']}

install_requires = \
['aiofiles>=0.7.0',
 'httpx>=0.19.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1',
 'nonebot-plugin-apscheduler>=0.1.3',
 'nonebot2>=2.0.0-beta.1',
 'pydantic>=1.10.2',
 'requests>=2.28.1']

setup_kwargs = {
    'name': 'nonebot-plugin-whateat-pic',
    'version': '1.0.3',
    'description': '基于Nonebot2的今天吃什么（离线版）',
    'long_description': '<div align="center">\n\n<a href="https://v2.nonebot.dev/store"><img src="https://i3.meishichina.com/atta/recipe/2023/01/06/20230106167298595549937310737312.JPG?x-oss-process=style/p800" width="180" height="180" alt="NoneBotPluginLogo"></a>\n\n</div>\n\n<div align="center">\n\n# nonebot-plugin-whateat-pic\n\n_⭐基于Nonebot2的一款今天吃什么喝什么的插件⭐_\n\n\n</div>\n\n\n## ⭐ 介绍\n\n一款离线版决定今天吃喝什么的nb2插件，功能及其简单。\n~~借用~~改编自hosinoBot的插件[今天吃什么](https://github.com/A-kirami/whattoeat)\n由于本人第一次创建，有不足的地方还请指出\n\n## 💿 安装\n\n<details>\n<summary>安装</summary>\n 将目标文件下载拖进nb2的插件文件夹就可\n \n 一般路劲为/src/plugin\n \n</details>\n\n\n## ⚙️ 配置\n\n没有配置，有什么美食图片自己拖进去就行\n\n## ⭐ 使用\n\n### 指令：**吃什么，**喝什么\n如：```\n    /今天吃什么、/早上吃什么，/夜宵喝什么\n    ```\n    \n**注意**\n\n默认情况下, 您应该在指令前加上命令前缀, 通常是 /\n\n## 🌙 未来\n- [ ] 或许添加更多的美食图片吧……\n- [ ] 添加更多功能\n',
    'author': 'Cvandia',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Cvandia/nonebot-plugin-whateat-pic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
