from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


class Config:
    def __init__(self):
        # Automatically load all environment variables into attributes
        for key, value in os.environ.items():
            setattr(self, key, value)


# Create an instance of Config to use throughout the project
config = Config()
