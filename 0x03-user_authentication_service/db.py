#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError, NoResultFound
from sqlalchemy.orm.query import Query
from user import Base, User

"""DB module contains the DB class"""
class DB:
    """DB class to interact with the database
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    
    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds user to the database"""
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Finds a user in the database"""
        try:
            query = Query(User).filter_by(**kwargs)
            user = query.first()
            
            if user is None:
                raise NoResultFound("No user found with the given filters.")
            
            return user
        except InvalidRequestError:
            raise InvalidRequestError("Wrong query arguments passed.")


    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates a user in the database"""
        user = self._session.query(User).get(user_id)
        
        if user is None:
            raise NoResultFound("No user found with the given user_id.")
        
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError(f"Attribute '{key}' does not correspond to a user attribute.")
        
        self._session.commit()
        return None
    