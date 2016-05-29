from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import app, db, models
from config import SQLALCHEMY_DATABASE_URI


engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker()
Session.configure(bind=engine)

session = Session()
print(session)

card1 = models.Card("A", "Type1", "Cat1", [
    {"question": "How can you get four suits for a dollar?",
     "answer": "Buy a deck of cards."},
    {"question": "How do dinosaurs pay their bills?", "answer": "With Tyrannosaurus checks."},
    {"question": "What do you call a dinosaur that smashes everything in its path?", "answer": "Tyrannosaurus wrecks."},
    {"question": "What do you call a dinosaur that wears a cowboy hat and boots?", "answer": "Tyrannosaurus Tex."},
    {"question": "How do we know the Indians were the first people in North America?",
     "answer": "They had reservations."}])

card2 = models.Card("B", "Type2", "Cat2", [
    {"question": "How do you make a hot dog stand?", "answer": "Steal its chair."},
    {"question": "How do you make an egg laugh?", "answer": "Tell it a yolk."},
    {"question": "How do you prevent a Summer cold?", "answer": "Catch it in the Winter!"},
    {"question": "How does a pig go to hospital?", "answer": "In a hambulance."},
    {"question": "If a long dress is evening wear, what is a suit of armor?", "answer": "Silverware."}])

card3 = models.Card("C", "Type1", "Cat2", [
    {"question": "What bird can lift the most?", "answer": "A crane."},
    {"question": "What bone will a dog never eat?", "answer": "A trombone."},
    {"question": "What can you hold without ever touching it?", "answer": "A conversation."},
    {"question": "What clothes does a house wear?", "answer": "Address."},
    {"question": "What country makes you shiver?", "answer": "Chile."}])

card4 = models.Card("D", "Type2", "Cat1", [
    {"question": "What did one elevator say to the other?", "answer": "I think I'm coming down with something!"},
    {"question": "What did one magnet say to the other?", "answer": "I find you very attractive."},
    {"question": "What did the mother broom say to the baby broom?", "answer": "It's time to go to sweep."},
    {"question": "What did the necktie say to the hat?", "answer": "You go on ahead. I'll hang around for a while."},
    {"question": "What did the rug say to the floor?", "answer": "Don't move, I've got you covered."}])

session.add(card1)
session.add(card2)
session.add(card3)
session.add(card4)
session.commit()
