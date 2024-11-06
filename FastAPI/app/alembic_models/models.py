""""
models module for alembic migrations
"""

from sqlalchemy import Column,Integer,String,ForeignKey,create_engine # pylint: disable=E0401
from sqlalchemy.orm import relationship, sessionmaker  # pylint: disable=E0401
from sqlalchemy.ext.declarative import declarative_base  # pylint: disable=E0401
from config.settings import DATABASE  # pylint: disable=E0401

# Declaración de la base
Base = declarative_base()


# 1. Clase Person
class Person(Base):  # pylint: disable=too-few-public-methods
    """
    Representa a una persona en el sistema.
    """

    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    test = Column(String(250))


class Permission(Base):  # pylint: disable=too-few-public-methods
    """
    Representa un permiso en el sistema.
    """

    __tablename__ = "permission"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class RolePermission(Base):  # pylint: disable=too-few-public-methods
    """
    Representa la relación entre un rol y un permiso.
    """

    __tablename__ = "role_permission"

    id = Column(Integer, primary_key=True)
    permission_id = Column(Integer, ForeignKey("permission.id"), nullable=False)
    person_id = Column(Integer, ForeignKey("person.id"), nullable=False)


# 2. Clase Promotion
class Promotion(Base):  # pylint: disable=too-few-public-methods
    """
    Representa una promoción aplicable a una reserva.
    """

    __tablename__ = "promotion"

    id = Column(Integer, primary_key=True)
    description = Column(String(250), nullable=False)
    discount = Column(String(250), nullable=False)
    startTime = Column(String(250), nullable=False)
    endTime = Column(String(250), nullable=False)
    status = Column(String(250), nullable=False)
    # Relación con Reservation (Many-to-One, si una promoción se aplica a varias reservas)
    reservation_id = Column(Integer, ForeignKey("reservation.id"), nullable=False)
    createdBy = Column(String(250), nullable=False)


# 3. Clase Reservation
class Reservation(Base):  # pylint: disable=too-few-public-methods
    """
    Representa una reserva de un espacio de trabajo.
    """

    __tablename__ = "reservation"

    id = Column(Integer, primary_key=True)
    reservedBy = Column(
        Integer, ForeignKey("person.id"), nullable=False
    )  # Relaciona con Person
    workspace_id = Column(
        Integer, ForeignKey("workspace.id"), nullable=False
    )  # Relaciona con Workspace
    startTime = Column(String(250), nullable=False)
    endTime = Column(String(250), nullable=False)
    status = Column(String(250), nullable=False)
    price = Column(String(250), nullable=False)

    # Relaciones
    person = relationship("Person", back_populates="reservations")
    workspace = relationship("Workspace", back_populates="reservations")


# 4. Clase Workspace
class Workspace(Base):  # pylint: disable=too-few-public-methods
    """
    Representa un espacio de trabajo que puede ser reservado.
    """

    __tablename__ = "workspace"

    id = Column(Integer, primary_key=True)
    type = Column(String(250), nullable=False)
    capacity = Column(String(250), nullable=False)
    hourlyRate = Column(String(250), nullable=False)
    availableSchedules = Column(String(250), nullable=False)
    createdBy = Column(
        String(250), nullable=False
    )  # Puede referirse a un admin que creó el espacio

    # Relación con Reservation (One-to-Many)
    reservations = relationship("Reservation", back_populates="workspace")


# 5. Clase Schedule
class Schedule(Base):  # pylint: disable=too-few-public-methods
    """
    Representa los horarios de apertura y cierre de un espacio de trabajo.
    """

    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True)
    openingTime = Column(String(250), nullable=False)
    closingTime = Column(String(250), nullable=False)
    status = Column(String(250), nullable=False)
    # Relación con Workspace (One-to-Many)
    workspace_id = Column(Integer, ForeignKey("workspace.id"))
    workspace = relationship("Workspace", back_populates="availableSchedules")


# Configuración de la base de datos
DATABASE_URL = (
    f"mysql+pymysql://{DATABASE['user']}:{DATABASE['password']}"
    f"@{DATABASE['host']}/{DATABASE['name']}"
)

engine = create_engine(DATABASE_URL)

# Crear una sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
