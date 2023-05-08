from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.dependencies import Base


class TblFavoriteBus(Base):
    __tablename__ = "favorite_bus"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    bus_id = Column(String, nullable=False)
    bus_name = Column(String, nullable=False)

    user = relationship("User", back_populates="favorite_buses")


class TblFavoriteStation(Base):
    __tablename__ = "favorite_station"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    station_id = Column(String, nullable=False)
    station_name = Column(String, nullable=False)

    user = relationship("User", back_populates="favorite_stations")
