import paramiko
import random
import string

# Настройки маршрутизатора MikroTik
router_ip = "192.168.88.1"
router_user = "admin"
router_password = "pass@125"

# Настройки профиля и новых паролей
profile_to_change = "default-encryption"
password_length = 10


def generate_password(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def change_password():
    # Подключение к маршрутизатору MikroTik через SSH
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(router_ip, username=router_user, password=router_password)

    # Получение списка пользователей с указанным профилем
    stdin, stdout, stderr = ssh_client.exec_command(f"/ppp secret print detail where profile={profile_to_change}")
    users = stdout.readlines()

    # Меняем пароли пользователям из полученного списка
    for user in users:
        if "name=" in user:
            username = user.split("name=")[1].split()[0].strip('"')
            users.append(username)
            new_password = generate_password(password_length)
            ssh_client.exec_command(f"/ppp secret set {username} password=\"{new_password}\"")
            error_msg = stderr.read().decode().strip()
            if error_msg:
                print(f"Ошибка при изменении пароля для пользователя {username}: {error_msg}")
            else:
                print(f"Пароль для пользователя {username} изменен на '{new_password}'")

    # Закрываем SSH сессию
    ssh_client.close()


change_password()
