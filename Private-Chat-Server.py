from socket import socket, AF_INET, SOCK_STREAM
from os import system, path
from sys import stdout
import threading

from loguru import logger
import configparser

@logger.catch
class Server():
    def __init__(self):
        system("title Private Chat Server")
        self.cfg_file = "srv_config.ini"
        self.config = configparser.ConfigParser()

        logging_model = {
            "handlers": [
                {"sink": stdout, "format": "[<cyan>{time:YYYY-MM-DD HH:mm:ss}</cyan>] [<level>{level}</level>] <level>{message}</level>"},
                {"sink": "server.log", "diagnose": False, "compression": "zip", "encoding": "utf8", "rotation": "10 MB", "format": "[<cyan>{time:YYYY-MM-DD HH:mm:ss}</cyan>] [<level>{level}</level>] {message}"},
                ]
        }

        logger.configure(**logging_model)
        new_level = logger.level("CHAT", no=38, color="<yellow>")

        logger.success("<--- Запуск сервера <---")

    def checkConfigExist(self):
        if path.isfile(self.cfg_file):
            logger.success(f"Конфиг файл {self.cfg_file} обнаружен")
        else:
            logger.error(f"Конфиг файл {self.cfg_file} не найден")
            logger.info("Создаю новый конфиг!")
            self.createConfig()
            logger.success("Конфиг создан! Необходим перезапуск!")
            input("Нажмите любую клавишу, чтобы закрыть!")
            exit(0)

    def createConfig(self, host='127.0.0.1', port=25560, day_message="Welcome to the club buddy! Type !help for more info."):
        self.config.add_section("server_settings")
        self.config.set("server_settings", "host", f"{host}")
        self.config.set("server_settings", "port", f"{port}")
        self.config.set("server_settings", "day_message", f"{day_message}")
        with open(self.cfg_file, "w") as self.config_file:
            self.config.write(self.config_file)

    def getConfigSettings(self):
        self.config.read(self.cfg_file)
        self.host = self.config.get("server_settings", "host")
        self.port = int(self.config.get("server_settings", "port"))
        self.day_message = self.config.get("server_settings", "day_message")
        system("cls||clear")

    def setupServerConnection(self):
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.clients = []
        self.nicknames = []

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.broadcast('[*] '.encode('utf8') + message)
                temp_message = (message.decode('utf8'))
                logger.log("CHAT", temp_message)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.broadcast(f"[-] {nickname}".encode('utf8'))
                logger.info(f"[-] {nickname}")
                self.nicknames.remove(nickname)
                self.broadcast(f'Онлайн ({len(self.nicknames)}): {self.nicknames}'.encode('utf8'))
                logger.info(f'Онлайн ({len(self.nicknames)}): {self.nicknames}')
                break
    
    def receive(self):
        while True:
            client, address = self.server.accept()
            client.send('NAME'.encode('utf8'))
            nickname = client.recv(1024).decode('utf8')
            self.nicknames.append(nickname)
            self.clients.append(client)

            logger.info(f"[+] {nickname} / {address[0]}:{address[1]}")
            logger.info(f'Онлайн ({len(self.nicknames)}): {self.nicknames}')
            client.send(f'{self.day_message}'.encode('utf8'))
            client.send(f'Онлайн ({len(self.nicknames)}): {self.nicknames}\n'.encode('utf8'))
            self.broadcast(f'[+] {nickname}'.encode('utf8'))
            self.thread = threading.Thread(target=self.handle, args=(client,))
            self.thread.start()

if __name__ == "__main__":
    srv = Server()
    srv.checkConfigExist()
    srv.getConfigSettings()
    srv.setupServerConnection()
    logger.info("[~] Жду подключения пользователей...")
    srv.receive()