# This is an app to encrypt and decrypt messages

from ctypes.wintypes import PLARGE_INTEGER
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import os
import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


class EncryptMessage(ttk.Frame):

    def __init__(self, master):
        self.master = master
        super().__init__(master=self.master)

        self.configure_interface()
        self.create_widgets()

    def configure_interface(self):
        self.private_key = None
        self.public_key = None
        self.key_name = "mutable-learning"
        self.path = os.path.dirname(os.path.abspath(__file__))

    def create_widgets(self):
        # Use a notebook to show some tabs
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(expand=1, fill=tk.BOTH)

        # Frame for decrypting messages
        self.decrypt = ttk.Frame(self.tabs, width=650, height=550)
        self.load_secret = ttk.Button(
            self.decrypt,
            text="Load Private Key",
            command=self.load_private_key,
        )
        self.load_secret.grid(row=0, column=0, sticky=tk.E)
        self.private_key_status = ttk.Label(
            self.decrypt, text="no private key loaded")
        self.private_key_status.grid(row=0, column=1, sticky=tk.W)

        self.encrypted_text = tk.Text(self.decrypt, height=15)
        self.encrypted_text.grid(row=1, column=0, columnspan=2)

        self.decrypt_button = ttk.Button(
            self.decrypt, text="Decrypt text", command=self.decrypt_message)
        self.decrypt_button.grid(row=2, column=0, sticky=tk.E)

        self.decrypted_message = tk.Text(self.decrypt, height=15)
        self.decrypted_message.grid(row=3, column=0, columnspan=2)

        self.generate_key_pair = ttk.Button(
            self.decrypt, text="Generate Public/Private Keys", command=self.generate_keys)
        self.generate_key_pair.grid(row=4, column=0, sticky=tk.E)

        self.decrypt.pack(expand=1, fill=tk.BOTH)

        # Add a frame to encrypt messages
        self.encrypt = ttk.Frame(self.tabs, width=650, height=550)

        self.public_keys = ttk.Combobox(
            self.encrypt, values=self.get_public_key_list())
        self.public_keys.bind("<<ComboboxSelected>>", self.load_public_key)
        self.public_keys.grid(row=0, column=0)

        self.message = tk.Text(self.encrypt, height=15)
        self.message.grid(row=1, column=0)

        self.encrypt_button = ttk.Button(
            self.encrypt, text="Encrypt Message", command=self.encrypt_message)
        self.encrypt_button.grid(row=2, column=0)

        self.encrypted_message = tk.Text(self.encrypt, height=15)
        self.encrypted_message.grid(row=3, column=0)

        self.copy_message = ttk.Button(
            self.encrypt, text="Copy encrypted message", command=self.copy_encrypted_message)
        self.copy_message.grid(row=4, column=0)

        self.encrypt.pack(expand=1, fill=tk.BOTH)

        # Add the frames as tabs in the notebook
        self.tabs.add(self.decrypt, text="Decrypt")
        self.tabs.add(self.encrypt, text="Encrypt")

    def get_public_key_list(self):
        public_keys = os.listdir(f"{self.path}/public_keys/")
        public_keys = [file for file in public_keys if file[-4:] == ".pem"]
        return public_keys

    def load_private_key(self):
        private_keyfile = askopenfilename(
            title="Select your private key",
            initialdir=f"{self.path}/secret_key/",
            filetypes=[("PEM files", "*.pem")]
        )
        with open(private_keyfile, "rb") as key_file:
            self.private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
            )
            self.private_key_status.config(text="Private key loaded")

    def load_public_key(self, event):
        public_keyfile = f"{self.path}/public_keys/{self.public_keys.get()}"
        with open(public_keyfile, "rb") as key_file:
            self.public_key = serialization.load_pem_public_key(
                key_file.read()
            )

    def decrypt_message(self):
        plaintext = self.private_key.decrypt(
            base64.urlsafe_b64decode(self.encrypted_text.get('1.0', tk.END)),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        self.decrypted_message.delete('1.0', tk.END)
        self.decrypted_message.insert('1.0', plaintext)

    def encrypt_message(self):
        if self.public_key:
            ciphertext = self.public_key.encrypt(
                self.message.get('1.0', tk.END).encode('utf-8'),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            self.encrypted_message.delete('1.0', tk.END)
            self.encrypted_message.insert(
                '1.0',
                base64.urlsafe_b64encode(ciphertext)
            )

    def copy_encrypted_message(self):
        self.clipboard_clear()
        self.clipboard_append(self.encrypted_message.get('1.0', tk.END))

    def generate_keys(self):
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        public_key = key.public_key()
        private_pem = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
        private_keyfile = f"{self.path}/secret_key/{self.key_name}-private.pem"
        with open(private_keyfile, 'wb') as private:
            private.write(private_pem)

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        public_keyfile = f"{self.path}/public_keys/{self.key_name}.pem"
        with open(public_keyfile, 'wb') as public:
            public.write(public_pem)


if __name__ == "__main__":
    root = tk.Tk()
    frame = EncryptMessage(root)
    frame.pack()
    root.mainloop()
