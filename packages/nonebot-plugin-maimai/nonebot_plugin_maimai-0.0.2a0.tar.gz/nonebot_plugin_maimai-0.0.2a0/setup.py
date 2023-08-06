import setuptools
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="nonebot_plugin_maimai",
    version="0.0.2a", 
    author="Umamusume-Agnes-Digital", 
    author_email="Z735803792@163.com", 
    description="Maimai DX plugin for NoneBot",
    long_description=long_description, 
    long_description_content_type="text/markdown",
    url="https://github.com/Umamusume-Agnes-Digital/nonebot_plugin_maimai",
    packages=["nonebot_plugin_maimai", "nonebot_plugin_maimai.libraries"],
    project_urls={
        "Bug Tracker": "https://github.com/Umamusume-Agnes-Digital/nonebot_plugin_maimai/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "nonebot2>=2.0.0rc1",
        "nonebot-adapter-onebot>=2.1.3,<3.0.0",
        "aiohttp==3.8.1",
        ],
)