class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    country = Column(String)
    population = Column(Integer)
    sunrise = Column(Integer)
    sunset = Column(Integer)
    timezone = Column(Integer)
    lat = Column(Float)
    lon = Column(Float)
