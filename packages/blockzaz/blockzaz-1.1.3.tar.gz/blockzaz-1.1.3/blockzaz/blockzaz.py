from typing import Optional

from prefect.blocks.core import Block
from pydantic import SecretStr

class CubeJs(Block):
    urlCube: Optional[str] = None
    apiSecret: Optional[SecretStr] = None
    urlAtualizacao: Optional[str] = None

class Pentaho(Block):
    urlPentaho: Optional[str] = None
    apiSecret: Optional[SecretStr] = None
    urlAtualizacao: Optional[str] = None

class DataBase(Block):
    nome: Optional[str] = None
    host: Optional[str] = None
    username: Optional[str] = None
    password: Optional[SecretStr] = None
    database: Optional[str] = None
    port: Optional[str] = None