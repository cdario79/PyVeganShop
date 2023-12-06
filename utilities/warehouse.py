from utilities.database import WarehouseDatabase


class Warehouse:
    """
    Warehouse manager utility
    """

    def __init__(self):
        self._warehouse_db = WarehouseDatabase()

    def get_products(self):
        """
        Get all products in warehouse database and list them
        """

        products = self._warehouse_db.load()

        print(f"PRODOTTO QUANTITA' PREZZZO")

        for product in products:
            print(f"{product['name']} {product['quantity']} €{product['selling_price']}")

        print("\n", end="")

    def add_product(self):
        """
        Add, or Update if exist, a product in warehouse database
        """

        new_product = {
            "name": '',
            "quantity": 0,
            "purchase_price": 0.0,
            "selling_price": 0.0
        }

        while new_product["name"] == '':
            try:
                new_product["name"] = str(input("Nome del prodotto: ").strip().lower())
                assert (len(new_product["name"]) > 0), "Il nome del prodotto non può essere vuoto!"
            except ValueError:
                print("Il nome del prodotto deve essere una stringa valida (es. tofu)!")
                new_product["name"] = ''
            except AssertionError as e:
                print(e)
                new_product["name"] = ''
            except Exception:
                print("Si è verificato un errore durante l'inserimento del nome del prodotto!")
                new_product["name"] = ''

        while new_product['quantity'] == 0:
            try:
                new_product["quantity"] = int(input("Quantità: "))
                assert (new_product["quantity"] > 0), "La quantità deve essere maggiore di zero!"
            except ValueError:
                print("La quantità deve essere un numero intero maggiore di zero (es. 5)!")
                new_product["quantity"] = 0
            except AssertionError as e:
                print(e)
                new_product["quantity"] = 0
            except Exception:
                print("Si è verificato un errore durante l'inserimento della quantità!")
                new_product["quantity"] = 0

        added_quantity = new_product['quantity']  # save the current addedd quantity to show it in the success message

        existing_product = self._warehouse_db.get_item_by_name(new_product["name"])

        if existing_product is False:

            while new_product['purchase_price'] == 0.0:
                try:
                    new_product["purchase_price"] = float(input("Prezzo di acquisto: "))
                    assert (new_product["purchase_price"] > 0), "Il prezzo di acquisto deve essere maggiore di zero!"
                except ValueError:
                    print("Il prezzo di acquisto deve essere un numero con decimali maggiore di zero (es. 1.45)!")
                    new_product["purchase_price"] = 0.0
                except AssertionError as e:
                    print(e)
                    new_product["purchase_price"] = 0.0
                except Exception:
                    print("Si è verificato un errore durante l'inserimento del prezzo di acquisto!")
                    new_product["purchase_price"] = 0.0

            while new_product['selling_price'] == 0.0:
                try:
                    new_product["selling_price"] = float(input("Prezzo di vendita: "))
                    assert (new_product["selling_price"] > 0), "Il prezzo di vendita deve essere maggiore di zero!"
                    assert (new_product["selling_price"] > new_product[
                        "purchase_price"]), "Il prezzo di vendita deve essere maggiore del prezzo di acquisto!"
                except ValueError:
                    print("Il prezzo di vendita deve essere un numero con decimali maggiore di zero (es. 2.87)!")
                    new_product["selling_price"] = 0.0
                except AssertionError as e:
                    print(e)
                    new_product["selling_price"] = 0.0
                except Exception:
                    print("Si è verificato un errore durante l'inserimento del prezzo di vendita!")
                    new_product["selling_price"] = 0.0

        else:
            # if product exist, sum new quantity to stored quantity
            # and retrieve purchase_price and selling_price
            # to prepare new_product for add or update in warehouse database
            new_product["quantity"] = int(new_product["quantity"]) + int(existing_product["quantity"])
            new_product["purchase_price"] = float(existing_product["purchase_price"])
            new_product["selling_price"] = float(existing_product["selling_price"])

        # add or update product in database warehouse
        self._warehouse_db.upsert(new_product)

        print(f"AGGIUNTO: {added_quantity} X {new_product['name']}\n")
