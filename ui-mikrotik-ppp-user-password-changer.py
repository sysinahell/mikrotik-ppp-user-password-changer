import paramiko
import random
import string
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk


def generate_password(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def change_passwords():
    router_ip = ip_entry.get()
    router_user = username_entry.get()
    router_password = password_entry.get()
    profile_to_change = profile_entry.get()
    password_length = 10

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(router_ip, username=router_user, password=router_password)

    stdin, stdout, stderr = ssh_client.exec_command(f"/ppp secret print detail where profile={profile_to_change}")
    users = stdout.readlines()

    for user in users:
        if "name=" in user:
            username = user.split("name=")[1].split()[0].strip('"')
            new_password = generate_password(password_length)
            ssh_client.exec_command(f"/ppp secret set {username} password=\"{new_password}\"")
            error_msg = stderr.read().decode().strip()
            if error_msg:
                result_text.insert(tk.END, f"Ошибка при изменении пароля для пользователя {username}: {error_msg}\n")
            else:
                result_text.insert(tk.END, f"Пароль для пользователя {username} изменен на '{new_password}'\n")

    ssh_client.close()


root = ThemedTk(theme="arc")  # Выберите тему, которая вам нравится
root.title("MikroTik PPP Password Changer")

frame = ttk.Frame(root, padding=(10, 10))
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_rowconfigure(6, weight=1)

ip_label = ttk.Label(frame, text="IP Address:")
ip_label.grid(row=0, column=0, sticky=tk.W,pady=(5,0),padx=(2,0))
ip_entry = ttk.Entry(frame)
ip_entry.grid(row=0, column=1, sticky=(tk.W, tk.E),pady=(5,0),padx=(2,0))

username_label = ttk.Label(frame, text="Username:")
username_label.grid(row=1, column=0, sticky=tk.W,pady=(5,0),padx=(2,0))
username_entry = ttk.Entry(frame)
username_entry.grid(row=1, column=1, sticky=(tk.W, tk.E),pady=(5,0),padx=(2,0))

password_label = ttk.Label(frame, text="Password:")
password_label.grid(row=2, column=0, sticky=tk.W,pady=(5,0),padx=(2,0))
password_entry = ttk.Entry(frame, show="*")
password_entry.grid(row=2, column=1, sticky=(tk.W, tk.E),pady=(5,0),padx=(2,0))

profile_label = ttk.Label(frame, text="PPP Profile:")
profile_label.grid(row=3, column=0, sticky=tk.W,pady=(5,0),padx=(2,0))
profile_entry = ttk.Entry(frame)
profile_entry.grid(row=3, column=1, sticky=(tk.W, tk.E),pady=(5,0),padx=(2,0))

change_password_button = ttk.Button(frame, text="Change Passwords", command=change_passwords)
change_password_button.grid(row=4, column=0, columnspan=2,pady=(10,0))

result_label = ttk.Label(frame, text="Results:")
result_label.grid(row=5, column=0, sticky=tk.W)

result_text = tk.Text(frame, wrap=tk.WORD)
result_text.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

root.mainloop()
