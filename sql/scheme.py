from sqlalchemy.orm import DeclarativeBase
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String, ForeignKey, DateTime, Text, BigInteger, Boolean
from datetime import datetime
from .engine import engine

class Base(DeclarativeBase):
     pass

class Users(Base):
     __tablename__ = "users"

     users_id: Mapped[int] = mapped_column(primary_key=True)
     user_id_tg: Mapped[int] = mapped_column(BigInteger)
     tg_name: Mapped[str] = mapped_column(String(100))
     full_name: Mapped[str] = mapped_column(String(100))
     created_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)
     update_on: Mapped[Optional[datetime]] = mapped_column(DateTime(), default=datetime.now, onupdate=datetime.now)
     
     logmessages: Mapped[List["LogMessage"]] = relationship(back_populates="users")

class LogMessage(Base):
     __tablename__ = "logmessage"

     logmessage_id:Mapped[int] = mapped_column(primary_key=True)
     users_id = mapped_column(ForeignKey("users.users_id"))
     created_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)
     type_message: Mapped[str] = mapped_column(String(10))
     message: Mapped[str] = mapped_column(Text())

     users: Mapped[List["Users"]] = relationship(back_populates="logmessages")

class NodeUnameInfo(Base):
     __tablename__ = "node_uname_info"

     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
     nodename: Mapped[str | None] = mapped_column(Text())
     job: Mapped[str | None] = mapped_column(Text())
     instance: Mapped[str | None] = mapped_column(Text())

class NodeNetworkReceiveBytesTotal(Base):
     __tablename__ = "node_network_receive_bytes_total"

     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
     nodename: Mapped[str | None] = mapped_column(Text())
     job: Mapped[str | None] = mapped_column(Text())
     instance: Mapped[str | None] = mapped_column(Text())
     summa: Mapped[int] = mapped_column(BigInteger)
     date: Mapped[datetime] = mapped_column(DateTime())

class NodeNetworkTransmitBytesTotal(Base):
     __tablename__ = "node_network_transmit_bytes_total"

     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
     nodename: Mapped[str | None] = mapped_column(Text())
     job: Mapped[str | None] = mapped_column(Text())
     instance: Mapped[str | None] = mapped_column(Text())
     summa: Mapped[int] = mapped_column(BigInteger)
     date: Mapped[datetime] = mapped_column(DateTime())

class UsersPnr(Base):
     __tablename__ = "users_pnr"

     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
     user_id: Mapped[int] = mapped_column(Text())
     username: Mapped[str | None] = mapped_column(Text())
     first_name: Mapped[str | None] = mapped_column(Text())
     last_name: Mapped[str | None] = mapped_column(Text())
     full_name: Mapped[str | None] = mapped_column(Text())
     admin: Mapped[Boolean] = mapped_column(Boolean())
     
class KroksNetworkBytes(Base):
     __tablename__ = "kroks_network_bytes"

     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
     nodename: Mapped[str | None] = mapped_column(Text())
     job: Mapped[str | None] = mapped_column(Text())
     instance: Mapped[str | None] = mapped_column(Text())
     iccid: Mapped[str | None] = mapped_column(Text())
     sim1: Mapped[Boolean] = mapped_column(Boolean())
     sim2: Mapped[Boolean] = mapped_column(Boolean())
     power: Mapped[Boolean] = mapped_column(Boolean())
     receive: Mapped[int] = mapped_column(BigInteger)	 
     transmit: Mapped[int] = mapped_column(BigInteger)
     date: Mapped[datetime] = mapped_column(DateTime())

class KroksNetworkBytesSum(Base):
     __tablename__ = "kroks_network_bytes_sum"

     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
     nodename: Mapped[str | None] = mapped_column(Text())
     job: Mapped[str | None] = mapped_column(Text())
     instance: Mapped[str | None] = mapped_column(Text())
     iccid: Mapped[str | None] = mapped_column(Text())
     sim1: Mapped[Boolean] = mapped_column(Boolean())
     sim2: Mapped[Boolean] = mapped_column(Boolean())
     power: Mapped[Boolean] = mapped_column(Boolean())
     receive: Mapped[int] = mapped_column(BigInteger)
     sumreceive: Mapped[int] = mapped_column(BigInteger)
     transmit: Mapped[int] = mapped_column(BigInteger)
     sumtransmit: Mapped[int] = mapped_column(BigInteger)
     summa: Mapped[int] = mapped_column(BigInteger)
     date: Mapped[datetime] = mapped_column(DateTime())

def create_db():
     Base.metadata.create_all(engine)     
