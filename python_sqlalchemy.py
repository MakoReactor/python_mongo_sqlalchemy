from typing import List, Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


# Declaração dos Models
class Base(DeclarativeBase):
    pass


class Client(Base):
    __tablename__ = "client_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    cpf: Mapped[str] = mapped_column(String(11), unique=True)
    address: Mapped[str] = mapped_column(String(50))

    account: Mapped[List["Account"]] = relationship(
        back_populates="client", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Client(id={self.id!r}, name={self.name!r},cpf={self.cpf!r})"


class Account(Base):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_type: Mapped[str] = mapped_column(String(15))
    agency: Mapped[str]
    account_num: Mapped[int]
    client_id: Mapped[int] = mapped_column(ForeignKey("client_account.id"))
    balance: Mapped[float]

    client: Mapped["Client"] = relationship(back_populates="account")

    def __repr__(self) -> str:
        return f"Account(id={self.id!r}, account_type={self.account_type}, client_id={self.client_id})"


# Criando a Engine e fazendo a conexão
from sqlalchemy import create_engine

engine = create_engine("sqlite://", echo=True)
Base.metadata.create_all(engine)


# Criando e persistindo objetos
from sqlalchemy.orm import Session

with Session(engine) as session:
    doug = Client(
        name="douglas",
        fullname="Douglas Barbosa dos Santos",
        cpf="28046186848",
        address="Eulina do Vale, 65",
        account=[
            Account(
                account_type="Conta Corrente",
                agency="8484",
                account_num=1234,
                balance=3500.33,
            ),
            Account(
                account_type="Poupança",
                agency="8484",
                account_num=2345,
                balance=1000.00,
            ),
        ],
    )

    sandy = Client(
        name="sandy",
        fullname="Sandy Lea",
        cpf="12345678912",
        address="Rua do Sandy e Júnior",
        account=[
            Account(
                account_type="Poupança",
                agency="8484",
                account_num=4321,
                balance=150323.42,
            )
        ],
    )

    pedro = Client(
        name="pedro",
        fullname="Pedro Malazartes",
        cpf="98765432198",
        address="Rua do Pé de Limão, 99",
        account=[
            Account(
                account_type="Conta Corrente",
                agency="9514",
                account_num=7913,
                balance=500.00,
            )
        ],
    )

    session.add_all([doug, sandy, pedro])
    session.commit()

# Select Simples
from sqlalchemy import select

session = Session(engine)
stmt = select(Client).where(Client.name.in_(["douglas", "sandy", "pedro"]))
for user in session.scalars(stmt):
    print(user)


# Select with Join
stmt = (
    select(Account)
    .join(Account.client)
    .where(Client.name == "douglas")
    .where(Account.account_type == "Conta Corrente")
)

print("\n----------- Select com clausula WHERE ----------")
result = session.scalars(stmt).one()
print(result)

# Imprimindo todas as contas e os clientes relacionados a elas.


def imprime_contas():
    stmt = select(Account)
    contas = session.scalars(stmt).all()

    print("\n----------- Imprimindo dados das contas -------------")
    for conta in contas:
        print(
            f"""
        Id: {conta.client.id}
        Nome: {conta.client.fullname} 
        Apelido: {conta.client.name}
        CPF: {conta.client.cpf}
        Tipo de Conta: {conta.account_type} Ag: {conta.agency} Nº {conta.account_num}
        Saldo: {conta.balance}
        """
        )


# Alterando cadastros
stmt = select(Client).where(Client.name == "sandy")
# Criar um objeto unico com o nome escolhido
sandy = session.scalars(stmt).one()

sandy.cpf = "11111111111"
sandy.address = "Fazenda do Xororó, 22 Interior de Algum lugar."
session.commit()


stmt = select(Account)
contas = session.scalars(stmt).all()

imprime_contas()

# Apagar objetos
# Apagar a segunda conta de Douglas
# selecionar o cliente
doug = session.get(Client, 1)
print(doug.account)


session.delete(doug.account[1])
session.commit()

imprime_contas()
