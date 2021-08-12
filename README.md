# Socket Private Chat

[![downloads](https://img.shields.io/github/downloads/nikkdusky/Socket-Private-Chat/total?color=pink&style=flat-square)](https://github.com/NikkDusky/Socket-Private-Chat/releases)
[![repo size](https://img.shields.io/github/repo-size/nikkdusky/Socket-Private-Chat?color=pink&style=flat-square)](https://github.com/NikkDusky/Socket-Private-Chat/)

## Server Requirements

```
Python 3
pip install loguru
pip install configparser
```
[![loguru](https://img.shields.io/pypi/v/loguru?color=pink&label=loguru&style=flat-square)](https://pypi.org/project/loguru/)
[![configparser](https://img.shields.io/pypi/v/configparser?color=pink&label=configparser&style=flat-square)](https://pypi.org/project/configparser/)

## Client Requirements

```
Python 3
pip install loguru
pip install configparser
pip install cryptography
```
[![loguru](https://img.shields.io/pypi/v/loguru?color=pink&label=loguru&style=flat-square)](https://pypi.org/project/loguru/)
[![configparser](https://img.shields.io/pypi/v/configparser?color=pink&label=configparser&style=flat-square)](https://pypi.org/project/configparser/)
[![cryptography](https://img.shields.io/pypi/v/cryptography?color=pink&label=cryptography&style=flat-square)](https://pypi.org/project/cryptography/)

## About

Клиент-серверное приложение для создания приватного чата с шифрованием на клиентской стороне. Общение в данном чате передаётся в зашифрованном виде с помощью Fernet (AES-CBC). Для общения необходимо, указать в конфигах клиентов единый ключ, который можно сгенерировать посредством ввода команды !keygen. Если у участника чата ключ не совпадает с людьми ведущими беседу, данный участник не сможет расшифровать сообщения.

## Screenshots

![](screenshots/1.png)
![](screenshots/2.png)
