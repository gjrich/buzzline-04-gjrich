"""
basic_json_consumer_case.py

Read a JSON-formatted file as it is being written.

Example JSON message from buzz_letters.json:
{"a": 44, "b": 10, ..., "z": 0}
"""

#####################################
# Import Modules
#####################################

# Import packages from Python Standard Library
import json
import os  # for file operations
import sys  # to exit early
import time
import pathlib
from collections import defaultdict  # no longer needed for aggregation but kept for consistency

# IMPORTANT
# Import Matplotlib.pyplot for live plotting
import matplotlib.pyplot as plt

# Import functions from local modules
from utils.utils_logger import logger


#####################################
# Set up Paths - read from the file the producer writes
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

# Purge existing content in buzz_live.json and buzz_letters.json so the producer starts fresh.
DATA_FILE.write_text("")
DATA_LETTERS_FILE.write_text("")
logger.info("Cleared previous data in buzz_live.json and buzz_letters.json")


#####################################
# Set up data structures
#####################################

# Global letter distribution; will be replaced by each incoming message.
letter_counts = {}

#####################################
# Set up live visuals
#####################################

fig, ax = plt.subplots()
plt.ion()  # Turn on interactive mode for live updates

#####################################
# Define an update chart function for live plotting
# This will get called every time a new message is processed
#####################################

def update_chart():
    """Update the live chart with the latest letter counts."""
    ax.clear()

    # Sort the letters to ensure they are in alphabetical order
    letters = sorted(letter_counts.keys())
    counts = [letter_counts[letter] for letter in letters]

    # Create a bar chart using the sorted letters and their counts
    ax.bar(letters, counts, color="green")

    # Set the labels and title for the chart
    ax.set_xlabel("Letters")
    ax.set_ylabel("Frequency")
    ax.set_title("Letter Distribution Histogram")

    # Rotate the x-axis labels for better readability
    ax.set_xticklabels(letters, rotation=45, ha="right")

    plt.tight_layout()
    plt.draw()
    plt.pause(0.01)


#####################################
# Process Message Function
#####################################

def process_message(message: str) -> None:
    """
    Process a single JSON message (letter distribution) and update the chart.

    Args:
        message (str): The JSON message as a string.
    """
    try:
        logger.debug(f"Raw message: {message}")
        message_dict: dict = json.loads(message)
        logger.info(f"Processed JSON message: {message_dict}")

        # Update the global letter_counts with the newly received distribution
        global letter_counts
        letter_counts = message_dict
        logger.info(f"Updated letter distribution: {letter_counts}")

        update_chart()
        logger.info(f"Chart updated successfully for message: {message}")

    except json.JSONDecodeError:
        logger.error(f"Invalid JSON message: {message}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")


#####################################
# Main Function
#####################################

def main() -> None:
    """
    Main entry point for the consumer.
    - Monitors buzz_letters.json for new messages and updates a live chart
      displaying the cumulative letter frequency histogram.
    """

    logger.info("START consumer.")

    # Verify the file we're monitoring exists; if not, exit early.
    if not DATA_LETTERS_FILE.exists():
        logger.error(f"Data file {DATA_LETTERS_FILE} does not exist. Exiting.")
        sys.exit(1)

    try:
        with open(DATA_LETTERS_FILE, "r") as file:
            # Move the cursor to the end of the file
            file.seek(0, os.SEEK_END)
            print("Consumer is ready and waiting for new JSON messages...")

            while True:
                line = file.readline()
                if line.strip():
                    process_message(line)
                else:
                    logger.debug("No new messages. Waiting...")
                    time.sleep(0.5)
                    continue

    except KeyboardInterrupt:
        logger.info("Consumer interrupted by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        plt.ioff()
        plt.show()
        logger.info("Consumer closed.")


#####################################
# Conditional Execution
#####################################

if __name__ == "__main__":
    main()
