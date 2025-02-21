"""
basic_json_producer_case.py

Generate some streaming buzz message json data to a file without using Kafka.

Example JSON message 
{"message": "I just saw a movie! It was amazing.", "author": "Eve"}
"""

#####################################
# Import Modules
#####################################

# Import packages from Python Standard Library
import json
import os
import random
import time
import pathlib
import re
import string

# Import external packages (must be installed in .venv first)
from dotenv import load_dotenv

# Import functions from local modules
from utils.utils_logger import logger


#####################################
# Load Environment Variables
#####################################

load_dotenv()

#####################################
# Getter Functions for .env Variables
#####################################

def get_message_interval() -> int:
    """Fetch message interval from environment or use default."""
    interval = int(os.getenv("BUZZ_INTERVAL_SECONDS", 1))
    logger.info(f"Message interval: {interval} seconds")
    return interval

#####################################
# Set up Paths - write to a file the consumer will monitor
#####################################

# The parent directory of this file is its folder.
# Go up one more parent level to get the project root.
PROJECT_ROOT = pathlib.Path(__file__).parent.parent
logger.info(f"Project root: {PROJECT_ROOT}")

# Set directory where data is stored
DATA_FOLDER: pathlib.Path = PROJECT_ROOT.joinpath("data")
logger.info(f"Data folder: {DATA_FOLDER}")

# Set the name of the data file for buzz messages
DATA_FILE: pathlib.Path = DATA_FOLDER.joinpath("buzz_live.json")
logger.info(f"Data file: {DATA_FILE}")

# Instantiate a new JSON file for letter distribution updates.
DATA_LETTERS_FILE: pathlib.Path = DATA_FOLDER.joinpath("buzz_letters.json")
logger.info(f"Letters data file: {DATA_LETTERS_FILE}")



#####################################
# Define global variables
#####################################

# Define some lists for generating buzz messages
ADJECTIVES: list = ["valiant", "dreadful", "chivalrous", "glorious", "cunning", "majestic", "grim", "enchanting", "fierce", "ancient"]
ACTIONS: list = ["clashed", "beheld", "discovered", "proclaimed", "vanquished", "forged", "bequeathed", "unearthed", "marveled at", "besieged"]
TOPICS: list = ["a dragon’s lair", "a knight’s tourney", "a baron’s betrayal", "a holy relic", "a siege tower", "a bard's ballad", "a witch’s curse", "a crusader’s vow", "a castle’s ruin", "a king’s decree"]

# Global letter distribution dictionary (a-z initialized to 0)
letter_counts = {letter: 0 for letter in string.ascii_lowercase}

#####################################
# Define a function to generate buzz messages
#####################################

def generate_messages():
    """
    Generate a stream of buzz messages in the JSON format.
    Example JSON message:
        {"message": "I love Python!", "author": "Eve"}

    Additionally, for each message generated, this function processes the 
    "message" field to remove punctuation, spaces, and special characters, 
    converts it to lowercase, updates a running cumulative letter distribution, 
    and writes the updated distribution as a new JSON line to buzz_letters.json.
    """
    while True:
        adjective = random.choice(ADJECTIVES)
        action = random.choice(ACTIONS)
        topic = random.choice(TOPICS)

        # Create a message string using f-string formatting
        message_string = f"I just {action} {topic}! It was {adjective}."

        # Add an author to the message
        author = random.choice(["Guinevere", "Lancelot", "Merlin", "Beowulf", "Eleanor", "Gawain", "Isolde", "Tristan", "Morgana", "Roland"])

        # Create a dictionary with the message and author
        json_message = {
            "message": message_string,
            "author": author
        }

        # Process the message: remove non-alphabetic characters and convert to lowercase
        processed_text = re.sub(r'[^a-zA-Z]', '', message_string).lower()
        # Update the global letter_counts for each letter in the processed message
        for char in processed_text:
            if char in letter_counts:
                letter_counts[char] += 1

        # Write the updated letter distribution to buzz_letters.json.
        # Each write is a new JSON message containing counts for every letter a-z.
        with DATA_LETTERS_FILE.open("a") as lf:
            lf.write(json.dumps(letter_counts) + "\n")

        # Yield the original buzz message for writing to buzz_live.json (if needed)
        yield json_message


#####################################
# Define main() function to run this producer.
#####################################

def main() -> None:
    """
    Main entry point for this producer.
    It continuously generates buzz messages and writes them to buzz_live.json.
    Additionally, each message triggers an update to buzz_letters.json.
    """

    logger.info("START producer...")
    logger.info("Hit CTRL c (or CMD c) to close.")
    
    # Call the function we defined above to get the message interval
    interval_secs: int = get_message_interval()

    try:
        for message in generate_messages():
            logger.info(message)
            with DATA_FILE.open("a") as f:
                f.write(json.dumps(message) + "\n")
            time.sleep(interval_secs)
    except KeyboardInterrupt:
        logger.warning("Producer interrupted by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        logger.info("Producer shutting down.")


#####################################
# Conditional Execution
#####################################

if __name__ == "__main__":
    main()
