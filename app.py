from utilities.warehouse import Warehouse
from utilities.sales import Sales


class App:
    """
    Vegan Store Warehouse Manager Application
    """

    def start(self):
        """
        Start Application and wait for command
        """

        command = None
        ware_house = Warehouse()
        sales = Sales()

        while command != "chiudi":

            command = input("Inserisci un comando: ").strip().lower()

            if command == "aggiungi":
                ware_house.add_product()
            elif command == "elenca":
                ware_house.get_products()
            elif command == "vendita":
                sales.new_sale()
            elif command == "profitti":
                sales.get_profits()
            elif command == "aiuto":
                self.help()
            elif command == "chiudi":
                print("Bye bye")
            else:
                print("Comando non valido")
                self.help()

    @staticmethod
    def help():
        """
        View help of application and show available command
        """

        print("I comandi disponibili sono i seguenti:")
        print("aggiungi: aggiungi un prodotto al magazzino")
        print("elenca: elenca i prodotto in magazzino")
        print("vendita: registra una vendita effettuata")
        print("profitti: mostra i profitti totali")
        print("aiuto: mostra i possibili comandi")
        print("chiudi: esci dal programma")
        print("\n", end="")
