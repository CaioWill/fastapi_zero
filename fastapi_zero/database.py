from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from fastapi_zero.settings import Settings

# Criação da engine, motor de conexão com o banco
engine = create_async_engine(Settings().DATABASE_URL)


# abre uma Sessao com o db -> Como uma Transação
async def get_session():  # pragma: no cover

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
