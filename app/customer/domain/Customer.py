# class Customer(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     email = Column(String, unique=True, index=True)
#     is_admin = Column(Boolean, default=False)
#
#     reservations = relationship("Reservation", back_populates="user")