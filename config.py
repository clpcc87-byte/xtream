# -*- coding: utf-8 -*-
import sys
import os
import json
import base64
from itertools import cycle

rConfigPath = "/home/xtreamcodes/iptv_xtream_codes/config"

def doDecrypt():
    rDecrypt = decrypt()
    if rDecrypt:
        print(f"Server ID: {' '*10}{int(rDecrypt['server_id'])}")
        print(f"Host: {' '*15}{rDecrypt['host']}")
        print(f"Port: {' '*15}{int(rDecrypt['db_port'])}")
        print(f"Username: {' '*11}{rDecrypt['db_user']}")
        print(f"Password: {' '*11}{rDecrypt['db_pass']}")
        print(f"Database: {' '*11}{rDecrypt['db_name']}")
    else: 
        print("Config file could not be read!")

def decrypt():
    try: 
        if not os.path.exists(rConfigPath):
            return None
            
        with open(rConfigPath, 'rb') as f:
            raw_data = f.read().strip()
            
        # Descodifica o Base64 lidando com possíveis resíduos ou quebras de linha
        decoded_bytes = base64.b64decode(raw_data)
        
        # Chave XOR em formato de bytes
        key_bytes = b'5709650b0d7806074842c6de575025b1'
        
        # Operação XOR expandida para evitar erros de sintaxe invisíveis
        decrypted_list = []
        for c, k in zip(decoded_bytes, cycle(key_bytes)):
            decrypted_list.append(c ^ k)
            
        decrypted_bytes = bytes(decrypted_list)
        
        # Converte para string e carrega o JSON
        json_string = decrypted_bytes.decode('utf-8', errors='ignore')
        return json.loads(json_string)
    except Exception as e: 
        return None

def encrypt(rInfo):
    try: 
        if os.path.exists(rConfigPath):
            os.remove(rConfigPath)
    except: 
        pass
        
    json_str = '{"host":"%s","db_user":"%s","db_pass":"%s","db_name":"%s","server_id":"%d", "db_port":"%d"}' % (
        rInfo["host"], rInfo["db_user"], rInfo["db_pass"], rInfo["db_name"], int(rInfo["server_id"]), int(rInfo["db_port"])
    )
    json_bytes = json_str.encode('utf-8')
    key_bytes = b'5709650b0d7806074842c6de575025b1'
    
    # Operação XOR expandida
    xor_list = []
    for c, k in zip(json_bytes, cycle(key_bytes)):
        xor_list.append(c ^ k)
        
    xor_bytes = bytes(xor_list)
    b64_bytes = base64.b64encode(xor_bytes)
    
    with open(rConfigPath, 'wb') as rf:
        rf.write(b64_bytes)

if __name__ == "__main__":
    try: 
        rCommand = sys.argv[1]
    except: 
        rCommand = None
        
    if rCommand and rCommand.lower() == "decrypt": 
        doDecrypt()
    elif rCommand and rCommand.lower() == "encrypt":
        print("Current configuration")
        print(" ")
        doDecrypt()
        print(" ")
        rEnc = {"pconnect": 0}
        try:
            rEnc["server_id"] = int(input(f"Server ID: {' '*10}"))
            rEnc["host"] = input(f"Host: {' '*15}")
            rEnc["db_port"] = int(input(f"Port: {' '*15}"))
            rEnc["db_user"] = input(f"Username: {' '*11}")
            rEnc["db_pass"] = input(f"Password: {' '*11}")
            rEnc["db_name"] = input(f"Database: {' '*11}")
            print(" ")
        except Exception as e:
            print("Invalid entries!")
            sys.exit(1)
        try:
            encrypt(rEnc)
            print("Written to config file!")
        except Exception as e: 
            print("Couldn't write to file!")
    else: 
        print("Usage: config.py [ENCRYPT | DECRYPT]")
