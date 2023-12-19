"""
Gemini Dungeon API

Game logic, chat and image generation api for gemini-dungeon frontend
"""
from dndlibrary import DNDLibrary
import logging

def main():
    try:
        logging.info("Setting up DND library")
        dndlib = DNDLibrary()
        dndlib.run()
    except Exception as err:
        logging.error(err)
        raise

if __name__ == "__main__":
    logging.info("Starting Gemini's Maze...")
    main()