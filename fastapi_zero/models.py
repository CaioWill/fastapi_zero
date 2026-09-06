# Como nao temos typo data padrao no py importamos o dt
from datetime import datetime
from enum import Enum

# func coloca antes de funcoes nativas como o SUM, AVG, NOW(), COUNT ...
from sqlalchemy import ForeignKey, func

# O Mapped mapeia o tipo em python para enviar o aceitavel para o db
# STR em python e TEXT em postgres
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

# Registry registra tableas
# Variavel para gegistrar as tabelas -> onde irar ficar os metadados
table_registry = registry()


# Tabela User -> registrada na variavel como dataclass
# Dataclass -> class com metadados
@table_registry.mapped_as_dataclass
class User:  # ORM
    __tablename__ = 'user'

    # init - seria uma coluna sem o NOT NULL
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    # onupdate - atualiza a data sempre que a linha é atualizada
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    todos: Mapped[list['Todo']] = relationship(
        init=False,
        cascade='all, delete-orphan',
        # cascade Apaga os todos relacionados ao user quando ele for deletado
        lazy='selectin',  # ->
    )


# Enum -> classe numerada
class TodoState(str, Enum):
    draft = 'draft'
    todo = 'todo'
    doing = 'doing'
    done = 'done'
    trash = 'trash'


@table_registry.mapped_as_dataclass
class Todo:
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    state: Mapped[TodoState]
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
