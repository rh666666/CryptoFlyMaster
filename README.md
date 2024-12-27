# CryptoFlyMaster

A crypto toolbox with python.  

一个古典密码工具箱。

## Python

前往<a href = 'https://www.python.org/downloads/'>Python官网</a>下载并安装

## 安装

打开`cmd`或者`Power Shell`，输入以下命令：

```shell
git clone https://github.com/rh666666/CryptoFlyMaster.git
cd CryptoFlyMaster
python -m pip install -r requirements.txt
```

## 使用

打开`cmd`或者`Power Shell`。  

```shell
python main.py
```

## 关于 Playfair

与市面上的playfair在线工具不同，这个项目的playfair直接采用**插入填充字母**的方式对明文中出现相同字母的分组进行处理。

如明文`hello world!`，对明文进行分组。

替换填充处理方式（将分组中重复的第二个字母替换为预先设定的填充）：

```
HE LX OW OR LD
```

本项目处理方式（在分组中重复字母之间填充）：

```
HE LX LO WO RL DX
```



## 鸣谢

<a href='https://github.com/yanghe90'>@yanghe90</a>

<a href='https://github.com/chen22222222'>@chen22222222</a>

[@Onepear1](https://github.com/Onepear1)