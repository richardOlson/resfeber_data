# in here we will load the environmental variables

from dotenv import load_dotenv
import os
load_dotenv()




username = os.getenv("username")
password = os.getenv("password")
host = os.getenv("host")
database = os.getenv("database")





if __name__ == "__main__":
    print(f"the username is {username}")
    print(f"the password is {password}")

