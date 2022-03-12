from menu import *
from blockchain import blockchain
from funzioni import *

bch = blockchain()


# Funzione operazioni admin
def admin_home():
    print("Benvenuto Amministratore")
    while (True):
        s_admin = menu_admin()        # mostra il menu dell'amministratore

        # Inserisce un nuovo agente
        if s_admin in {"1", "2", "3"}:  # tipologie di account ammessi
            print("Inserisci indirizzo portafoglio", tipo_utente.get(int(s_admin)) + ",",
                  bcolors.WARNING + "c" + bcolors.ENDC + " per generarlo automaticamente, " + bcolors.OKCYAN + "q" + bcolors.ENDC + " per annullare")

            address = input_val(max_len=42)
            if (address != "q"):    # l'admin intende inserire l'account

                if (address == "c"):
                    # generazione automatica di indirizzo e chiave privata
                    private_key, address = genera_portafoglio()
                    print("Indirizzo generato:\n","Address:" ,address, "\n","Private Key:", private_key)
                else:
                    # l'admin ha inserito un indirizzo manualmente, chiedo la relativa chiave privata
                    private_key = input_val(messaggio="Inserisci la chiave privata: ")

                # Scelta password di sblocco
                password = richiedi_password()

                # Aggiunta account nella blockchain
                bch.aggiunta_agenti(int(s_admin), address)

                # Inserimento account nel nodo corrente
                if bch.inserimento_account(private_key, password):
                    print("Indirizzo inserito nel nodo corrente")
                else:
                    print("Errore nell'inserimento dell'Account")

            else:
                pass

        elif (s_admin == "b"):      # stampa l'elenco degli account creati
            print("Elenco Fornitori:")
            print(bch.ricerca_agenti(1))
            print("Elenco Trasformatori:")
            print(bch.ricerca_agenti(2))
            print("Elenco Clienti:")
            print(bch.ricerca_agenti(3))

        elif (s_admin == "q"):
            break
        else:
            print("Inserisci un carattere valido")


def login(tipo):
    print("Elenco indirizzi esistenti")
    print(bch.ricerca_agenti(tipo))
    print("Inserisci indirizzo portafoglio", tipo_utente.get(int(tipo)) + "," + bcolors.OKCYAN + " q" + bcolors.ENDC + " per uscire")
    address = input_val(max_len=42)
    if (address == "q"):    # logout
        return False
    else:
        if bch.account_bloccato(address):
            password = richiedi_password()    # inserimento password account
            logged = bch.unlock_account(tipo, address, password)
            if (logged):
                print("account sbloccato")
            else:
                print("errore nello sblocco dell'account")
                return False    # sblocco account non andato a buon fine, logout
        else:
            print("account gia sbloccato")
        return address  # se l'account era già sbloccato o è stato sbloccato


def fornitore_home():
    print("Buongiorno sig. fornitore")
    address = login(1)  # funzione per sblocco account
    if not address:
        pass    # se è stato chiesto un logout o lo sblocco non è andato a buon fine
    else:
        while(True):
            s_fornitore = menu_fornitore()
            if s_fornitore == "1":
                id_lotto = int(input_val(messaggio = "Inserisci il lotto relativo al prodotto", max_len = 20))
                CO2 = int(input_val(messaggio = "Inserisci il totale di CO2 emessa in grammi", max_len = 10))
                bch.crea_nft_fornitore(address, id_lotto, CO2)
            if (s_fornitore == "q"):
                # TODO lock account
                break
            # TODO GESTISCI ALTRE AZIONI FORNITORE


def trasformatore_home():
    print("Buongiorno sig. trasformatore")


def cliente_home():
    print("Buongiorno sig. cliente")


if __name__ == "__main__":

    # Stampe inziali, Benvenuto e controllo connessione blockchain
    print(bcolors.HEADER + "Benvenuto nella Dapp" + bcolors.ENDC)

    if bch.connessione():
        print("Sei connesso alla blockchain")
    else:
        print("Connessione fallita")
        # exit(10)

    while (True):
        utente = scelta_utente()  # Stampa il menù per la scelta utente

        if (utente == "0"):
            admin_home()
        elif (utente == "1"):
            fornitore_home()
        elif (utente == "2"):
            trasformatore_home()
        elif (utente == "3"):
            cliente_home()
        elif (utente == "h"):
            helper()
        elif (utente == "q"):
            exit("Arrivederci!!")
        else:
            print("Inserisci un carattere valido")
