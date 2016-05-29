from sqlalchemy import Table, Column, Integer, ForeignKey, String, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://app:1qazxsw23edc@127.0.0.1:3306/testdb"
Base = declarative_base()

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

class Parent(Base):
    __tablename__ = "parents"
    name = Column(String(16))
    id = Column(Integer, primary_key=True)
    children = relationship('Child', back_populates = "parent")

    def __repr__(self):
        return "PARENT: {} with {} children".format(self.name, len(self.children))

    def __init__(self, name, child_list=None):
        self.name = name
        if child_list is not None:
            for child in child_list:
                self.children.append(Child(name=child))
        print(self)


class Child(Base):
    __tablename__ = "children"
    id = Column(Integer, primary_key=True)
    name = Column(String(16))
    parent_id = Column(Integer, ForeignKey('parents.id'))
    parent = relationship('Parent', back_populates = "children")

    def __repr__(self):
        return "CHILD: {} with parent: {}".format(self.name, self.parent.name)


def buildParent(name, child_list):
    parent_test = Parent(name=name)
    children_list = []
    for child in child_list:
        children_list.append(Child(name=child))
    parent_test.children = children_list
    print(parent_test)
    return parent_test


person1 = buildParent(name="bob",child_list=["janet","jill","jim"])
person2 = Parent(name="Joe",child_list=["ted","bill","yont"])
person3 = Parent(name="frank",child_list=["george","juan","hank"])

Base.metadata.create_all(engine)
print(person1)

Session = sessionmaker(bind=engine)
session = Session()

session.add_all([person1, person2, person3])
session.commit()
session.close()
