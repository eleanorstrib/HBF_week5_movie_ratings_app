import model
import csv

def load_users(session):
    # use u.user
    with open('seed_data/u.user') as file:
        reader = csv.reader(file, delimiter='|')    # reader function takes each line of the file & makes a list containing all that line's columns
        for row in reader:
            id, age, gender, occupation, zipcode = row  # unpacking row   
            u = User(id=id,email=None, password=None, age=age, zipcode=zipcode)
            session.add(u)
    session.commit()

def load_movies(session):
    # use u.item
    pass

def load_ratings(session):
    # use u.data
    pass

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    pass

if __name__ == "__main__":
    s= model.connect()
    main(s)
