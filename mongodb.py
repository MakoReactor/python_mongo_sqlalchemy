# Python e MongoDB

from connection_mongodb import connection
from pprint import pprint


client_mongo = connection()

db = client_mongo.banco
collection = db.banco_collection

cliente = {
    "name": "douglas",
    "fullname": "Douglas Barbosa dos Santos",
    "cpf": "12345678912",
    "address": "Rua que sobe e desce, 21",
    "account": [
        {
            "account_type": "Conta Corrente",
            "agency": "8484",
            "account_num": 123,
            "balance": 3500.00,
        },
        {
            "account_type": "Poupança",
            "agency": "8484",
            "account_num": 321,
            "balance": 300.00,
        },
    ],
}

clientes = db.clientes
cliente_id = clientes.insert_one(cliente).inserted_id

print(cliente_id)
print()
print(db.clientes)
print()

print("********* Imprime uma pessoa do Bancao **********")
pprint(db.clientes.find_one())
print()

clientes2 = [
    {
        "name": "sandy",
        "fullname": "Sandy Léa",
        "cpf": "98765432178",
        "address": "Fazenda do Chororó, 33",
        "account": [
            {
                "account_type": "Conta Corrente",
                "agency": "8484",
                "account_num": 123,
                "balance": 100000.00,
            },
        ],
    },
    {
        "name": "pedro",
        "fullname": "Pedro Malazartes",
        "cpf": "78945612385",
        "address": "Rua do Sopa de Pedra, 171",
        "account": [
            {
                "account_type": "Conta Corrente",
                "agency": "8484",
                "account_num": 123,
                "balance": 1.00,
            },
            {
                "account_type": "Poupança",
                "agency": "8484",
                "account_num": 321,
                "balance": 2.00,
            },
        ],
    },
]

result = clientes.insert_many(clientes2)
print(result.inserted_ids)

pprint(db.clientes.find_one())

# imprime todoas as contas
print("\n********** Imprime todas as pessoas do Banco **********\n")
for cliente in clientes.find():
    pprint(cliente)
    print()

# pesquisa todas as entradas que têm um nome
print("*" * 50)
print("\nImprimindo todos as pessoas com nome Sandy\n")
for nome in db.clientes.find({"name": "sandy"}):
    pprint(nome)
    print()

    # apaga a collection para poder sempre começar zerado
db.drop_collection("clientes")
