import uuid

from utilities.database import SalesDatabase
from utilities.database import WarehouseDatabase


class Sales:
    """
    Sales manager utility
    """

    def __init__(self):
        self._sales_db = SalesDatabase()
        self._warehouse_db = WarehouseDatabase()

    def get_profits(self):
        """
        Get all sales and calculate the gross profit and the net profit
        """

        total_purchase_price = 0
        total_selling_price = 0

        sales = self._sales_db.load()
        for sale in sales:
            total_purchase_price += float(sale['purchase_price']) * int(sale['quantity'])
            total_selling_price += float(sale['selling_price']) * int(sale['quantity'])

        gross_profit = total_selling_price
        net_profit = total_selling_price - total_purchase_price

        print(f"Profitto: lordo=€{gross_profit:.2f} netto=€{net_profit:.2f}\n")

    def new_sale(self):
        """
        Register new sale in sales database and update quantity in warehouse database
        """

        sale_uid = uuid.uuid4().hex
        insert_another_product = None
        existing_product = False
        current_sale_details = []

        while insert_another_product != "no":

            new_sale = {
                "name": '',
                "quantity": 0,
                "purchase_price": 0.0,
                "selling_price": 0.0,
                "sale_id": str(sale_uid)
            }

            while new_sale["name"] == '':
                try:
                    new_sale["name"] = str(input("Nome del prodotto: ").strip().lower())
                    assert (len(new_sale["name"]) > 0), "Il nome del prodotto non può essere vuoto!"
                    existing_product = self._warehouse_db.get_item_by_name(new_sale["name"])
                    assert (existing_product != False), "Il prodotto non è presente in magazzino!"
                except ValueError:
                    print("Il nome del prodotto deve essere una stringa valida (es. tofu)!")
                    new_sale["name"] = ''
                except AssertionError as e:
                    print(e)
                    new_sale["name"] = ''
                except Exception:
                    print("Si è verificato un errore durante l'inserimento del nome del prodotto!")
                    new_sale["name"] = ''

            while new_sale['quantity'] == 0:
                try:
                    new_sale["quantity"] = int(input("Quantità: "))
                    assert (new_sale["quantity"] > 0), "La quantità deve essere maggiore di zero!"
                    assert (new_sale["quantity"] <= existing_product["quantity"]), f"La quantità inserita è maggiore di quella disponibile: {existing_product['quantity']}!"
                except ValueError:
                    print("La quantità deve essere un numero intero maggiore di zero (es. 5)!")
                    new_sale["quantity"] = 0
                except AssertionError as e:
                    print(e)
                    new_sale["quantity"] = 0
                except Exception:
                    print("Si è verificato un errore durante l'inserimento della quantità!")
                    new_sale["quantity"] = 0

            try:
                new_sale["purchase_price"] = float(existing_product["purchase_price"])
                new_sale["selling_price"] = float(existing_product["selling_price"])
                current_sale_details.append(new_sale)
                # Insert new sale in sales database
                self._sales_db.insert(new_sale)
            except Exception:
                print("Errore durante la registrazione della vendita!")
                break

            try:
                existing_product["quantity"] = int(existing_product["quantity"]) - int(new_sale["quantity"])
                if existing_product["quantity"] == 0:
                    # delete product from warehouse database if available quantity
                    # after sale is equal to zero
                    self._warehouse_db.delete_by_name(existing_product["name"])
                else:
                    # update product in warehouse database if available quantity
                    # after sale is major to zero
                    self._warehouse_db.update(existing_product)
            except Exception:
                print("Errore duranta l'aggiornamento delle quantità del prodotto a magazzino!")
                break

            another_product_input = None

            while another_product_input not in ("si","no"):
                try:
                    another_product_input = str(input("Aggiungere un altro prodotto? (si/no): ").strip().lower())
                    assert (len(another_product_input) > 0), "Inserire una risposta (si/no)!"
                    assert (another_product_input in ('si', 'no')), "La risposta deve essere 'si' oppure 'no'!"
                    insert_another_product = another_product_input
                except ValueError:
                    print("La risposta deve essere una stringa valida (si/no)!")
                    another_product_input = None
                except AssertionError as e:
                    print(e)
                    another_product_input = None
                except Exception:
                    print("Si è verificato un errore durante l'inserimento della risposta!")
                    another_product_input = None

            if insert_another_product == 'no':
                total = 0
                print("VENDITA REGISTRATA")

                for details in current_sale_details:
                    print(f"- {details['quantity']} X {details['name']}: €{details['selling_price']:.2f}")
                    total += float(details['selling_price']) * int(float(details['quantity']))

                print(f"Totale: €{total:.2f}\n")
