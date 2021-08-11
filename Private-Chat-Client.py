from socket import socket, AF_INET, SOCK_STREAM
from time import localtime, strftime
from os import system, path
from sys import stdout
import threading

from cryptography.fernet import Fernet
from loguru import logger
import configparser

@logger.catch
class Client():
    def __init__(self):
        system("title Private Chat Client")
        self.cfg_file = "cli_config.ini"
        self.config = configparser.ConfigParser()

        logging_model = {
            "handlers": [
                {"sink": stdout, "format": "[<cyan>{time:HH:mm:ss}</cyan>] [<level>{level}</level>] <level>{message}</level>"}
                ]
        }

        logger.configure(**logging_model)
        new_level_chat = logger.level("CHAT", no=38, color="<light-cyan>")
        new_level_connect = logger.level("+", no=38, color="<light-green>")
        new_level_disconnect = logger.level("-", no=38, color="<light-red>")
        new_level_system = logger.level("SYS.", no=38, color="<light-yellow>")

    def createConfig(self, host='127.0.0.1', port=25560, key="C3YU7E9UMcKZhVg4OsnGs4K26cI54URM_KeYEVgrXsI="):
        self.config.add_section("client_settings")
        self.config.set("client_settings", "host", f"{host}")
        self.config.set("client_settings", "port", f"{port}")
        self.config.set("client_settings", "key", f"{key}")
        with open(self.cfg_file, "w") as config_file:
            self.config.write(config_file)

    def checkConfigExist(self):
        if path.isfile(self.cfg_file):
            pass
        else:
            self.createConfig()
            print(f"{self.cfg_file} не найден, создаю новый!")
            input("Нажмите любую клавишу, чтобы закрыть!")
            exit(0)

    def getConfigSettings(self):
        self.config.read(self.cfg_file)
        self.host = self.config.get("client_settings", "host")
        self.port = int(self.config.get("client_settings", "port"))
        self.key = self.config.get("client_settings", "key")

    def updateConfig(self, key):
        self.config.set("client_settings", "host", f"{self.host}")
        self.config.set("client_settings", "port", f"{self.port}")
        self.config.set("client_settings", "key", f"{key}")
        with open(self.cfg_file, "w") as config_file:
            self.config.write(config_file)

    def keygen(self):
        newkey = (Fernet.generate_key()).decode('utf8')
        self.updateConfig(newkey)
        print(f"\nНовый ключ был сгенерирован и записан в '{self.cfg_file}'\nНе забывайте, что ключи у собеседников должны совпадать!\n")
        print("Внимание необходим перезапуск, программы, чтобы ключ обновился!\n")

    def encrypt(self, text):
        fernet = Fernet(self.key.encode("utf8"))
        encMessage = fernet.encrypt(text.encode())
        return encMessage

    def decrypt(self, text):
        fernet = Fernet(self.key.encode("utf8"))
        decMessage = fernet.decrypt(text).decode()
        return decMessage

    def connectServer(self):
        print(f"\tPrivate Chat Client")
        self.nickname = input(f"\tВыберите имя: ")

        system("cls||clear")
        self.client = socket(AF_INET, SOCK_STREAM)

        try:
            self.client.connect((self.host, self.port))
            print(f"*** Сервер найден, подключаюсь ***")
        except ConnectionRefusedError:
            print(f"*** Сервер не найден, попробуйте позже ***")
            input(f"Нажмите Enter, чтобы закрыть приложение\n")
            exit(0)

    def get_time(self):
        named_tuple = localtime()
        return (f'[{strftime("%H:%M:%S", named_tuple)}]')

    def receive(self):
        while True:
            try:
                message = str(self.client.recv(1024).decode('utf8'))
                if message == "NAME":
                    self.client.send(self.nickname.encode('utf8'))
                elif message.startswith("[*]"):
                    message = message.replace("[*] ", "")
                    message = message.encode("utf8")
                    try:
                        logger.log("CHAT", f"{self.decrypt(message)}")
                    except:
                        logger.error(f"Кто-то отправил сообщение, но вам не удалось его расшифровать.\nПроверьте совпадают ли ключи в '{self.cfg_file}'")
                elif message.startswith("[+]"):
                    logger.log("+", message.replace("[+] ", ""))
                elif message.startswith("[-]"):
                    logger.log("-", message.replace("[-] ", ""))
                else:
                    logger.log("SYS.", message)
            except:
                print(f"Произошла ошибка, возможно сервер перестал отвечать...")
                self.client.close()
                break

    def write(self):
        while True:
            text = input(f"")
            if text == "!help":
                print("\n\t!keygen - сгенерировать новый ключ;")
                print("\t!about - о методе шифрования;\n")
            elif text == "!keygen":
                system("cls||clear")
                self.keygen()
            elif text == "!about":
                system("cls||clear")
                print("""
        
        * Программа использует метод шифрования Fernet;
        * Fernet гарантирует, что сообщение, зашифрованное с его помощью,
        невозможно будет обработать или прочитать без ключа;
        * Fernet - это реализация симметричной аутентифицированной криптографии;
        * Все сообщения шифруются на клиенте с помощью заданного ключа в 'cli_config.ini';
        * При получении сообщения, клиент будет пытаться его
        расшифровать с помощью заданного ключа в 'cli_config.ini';
        * Информация передаваемая в открытом виде:
            - [+] User <- Сообщения о присоединении;
            - [-] User <- Сообщения о дисконнекте;
            - Стартовое сообщение с приветствием.

    """)
            elif text == "":
                print("\033[A\033[A")
                pass
            else:
                print("\033[A\033[A")
                message = (self.encrypt(f'{self.nickname}: {text}')).decode('utf8')
                self.client.send(message.encode('utf8'))

if __name__ == '__main__':    
    cli = Client()
    cli.checkConfigExist()
    cli.getConfigSettings()
    cli.connectServer()
    receive_thread = threading.Thread(target=cli.receive)
    receive_thread.start()
    write_thread = threading.Thread(target=cli.write)
    write_thread.start()