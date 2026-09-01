# Como nao temos typo data padrao no py importamos o dt
from datetime import datetime

# func coloca antes de funcoes nativas como o SUM, AVG, NOW(), COUNT ...
from sqlalchemy import func

# O Mapped mapeia o tipo em python para enviar o aceitavel para o db
# STR em python e TEXT em postgres
from sqlalchemy.orm import Mapped, mapped_column, registry

# Registry registra tableas


# Variavel pra gegistar tablas
table_registry = registry()


# Tabela User
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
        init=False, server_default= func.now(), onupdate=func.now()
    )
