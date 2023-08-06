import setuptools

# with open("README.md", "r", encoding="utf-8") as fh:
#   long_description = fh.read()
long_description = """
This package is used to view system and hardware information. 这个包用于查看系统及硬件信息。

It uses the wmi library in order to view some hardware information. 它使用wmi库以查看一些硬件信息。
An example, if you want to use it to view the MAC address, you can code it like this: 例如，如果你想用它来查看MAC地址，你可以这样编码：

>>> import computer_info
>>> print(computer_info.net_mac())
F6:XX:XX:XX:XX:XX

I don't believe I need to write a separate description to point out what the functions do, because the function names are clearly written, and then the system automatically lists all the functions below. 我相信我无需编写一个另外的说明来指出函数们的作用，因为函数名称写得很清楚，然后系统会在下面自动列出所有的函数。
The names of all system-related functions start with system, the names of network-related functions start with net, and the names of hardware-related functions start with hardware. Only one function starts with computer. 所有与系统相关的函数的名称都以system开头，网络相关的函数的名称以net开头，硬件相关函数的名称以hardware开头。只有一个函数以computer开头。
This library is very useful, it is small, convenient and easy to call. You can use and combine these functions as many times as you want to get the most out of them. 这个库十分的好用，它小巧便捷，且调用方便。您可以随意地使用、组合这些函数以发挥您想要的最大效果。
Please forgive me if you can't read the English in this description. I do not know English, this is just a machine translation. 如果你看不懂这篇描述中的英语，请原谅我。我不懂英语，这只是机器翻译。 https://www.deepl.com/translator#zh/en/
"""

setuptools.setup(
    name="computer_info",
    version="1.0.1",
    author="Xingyuan55",
    author_email="dus0963@outlook.com",
    description="This package is used to view system and hardware information.",
    long_description=long_description,
    # description_content_type='text/plain',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",

    ],
)
