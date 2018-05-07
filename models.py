from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurant'

    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    address = Column(String(80), nullable = False) 
    image = Column(String(80), nullable = False)

    @property
    def serialize(self):
    	return {
            'id': self.id,
    		'name': self.name,
    		'address': self.address,
            'image': self.image
    	}



engine = create_engine('sqlite:///restaurants.db')
Base.metadata.create_all(engine)