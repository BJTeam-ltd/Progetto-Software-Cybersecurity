from menu import *
from blockchain import blockchain
from funzioni import *
from texttable import Texttable

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
                    print(bcolors.FAIL + "Errore nell'inserimento dell'Account nel nodo" + bcolors.ENDC)
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
        if not bch.account_sbloccato(address):
            password = richiedi_password()    # inserimento password account
            logged = bch.sblocco_account(address, password)
            if (logged):
                print(bcolors.OKCYAN + "account sbloccato" + bcolors.ENDC)
            else:
                print(bcolors.FAIL + "errore nello sblocco dell'account" + bcolors.ENDC)
                return False    # sblocco account non andato a buon fine, logout
        else:
            print(bcolors.OKCYAN + "account già sbloccato" + bcolors.ENDC)
        return address  # se l'account era già sbloccato o è stato sbloccato


def accoglienza(tipo):
    print("Elenco indirizzi esistenti")
    print(bch.ricerca_agenti(tipo))
    print("Inserisci indirizzo portafoglio", tipo_utente.get(int(tipo)) + "," + bcolors.OKCYAN + " q" + bcolors.ENDC + " per uscire")
    address = input_val()
    if (address == "q"):
        return False
    else:
        bch.login_account(tipo, address) #TODO DEVE RITORNARE QUALCOSA
        return True


def fornitore_home():
    print("Buongiorno sig. fornitore")
    address = login(1)  # funzione per sblocco account
    if not address:
        pass    # se è stato chiesto un logout o lo sblocco non è andato a buon fine
    else:
        while(True):
            s_fornitore = menu_fornitore()
            if s_fornitore == "1":
                id_lotto = int(input_val(messaggio = "Inserisci il lotto relativo al prodotto: ", max_len = 20))
                CO2 = int(input_val(messaggio = "Inserisci il totale di CO2 emessa in grammi: ", max_len = 10))
                if bch.crea_nft_fornitore(address, id_lotto, CO2):
                    print(bcolors.OKGREEN + "NFT creato con successo" + bcolors.ENDC)
                else:
                    print("NFT non creato")
            if s_fornitore == "q":
                if (bch.blocco_account(address)):
                    print("logout eseguito")
                break
            if s_fornitore == "2":
                tmp = bch.lista_nft(address)
                list = []
                list.append(['ID NFT', 'Lotto', 'CO\u2082', 'NFT precedente'])
                for i in range(0, len(tmp)):
                    list.append([tmp[i]['id_NFT'], tmp[i]['id_lotto'], tmp[i]['CO2'], tmp[i]['NFT_precedente']])
                t = Texttable()
                t.add_rows(list)
                print(t.draw())

            if s_fornitore == "3":
                print("Elenco trasformatori esistenti")
                print(bch.ricerca_agenti(2))
                destinatario = input_val(messaggio = "Inserisci destinatario dell'NFT: ", max_len = 43)
                id_nft = input_val(messaggio="Inserisci id NFT: ", max_len=20)
                if bch.trasferisci_nft(destinatario, int(id_nft), address):
                    print(bcolors.OKGREEN + "Trasferimento NFT", id_nft, "verso", destinatario, "è riuscito" + bcolors.ENDC)

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
        exit(10)

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
