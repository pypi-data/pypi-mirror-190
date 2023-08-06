import setuptools

requirements = ['numpy','matplotlib','networkx','tqdm','scipy']       # 自定义工具中需要的依赖包

setuptools.setup(
    name="HIT_network",       # 自定义工具包的名字
    version="0.0.3",             # 版本号
    author="Jinyan",           # 作者名字
    author_email="duanjinyan8866@outlook.com",  # 作者邮箱
    description="This is an integrated shortcut network related programming toolkit, the content is still in the development stage", # 自定义工具包的简介
    license='MIT-0',           # 许可协议
    url="https://github.com/656756130/Network_basementlearning",              # 项目开源地址
    packages=setuptools.find_packages(),  # 自动发现自定义工具包中的所有包和子包
    install_requires=requirements,  # 安装自定义工具包需要依赖的包
    python_requires='>=3.5'         # 自定义工具包对于python版本的要求
)