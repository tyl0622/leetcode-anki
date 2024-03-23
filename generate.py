#!/usr/bin/env python3
"""
This script generates an Anki deck with all the leetcode problems currently
known.
"""

import argparse
import asyncio
import logging
from pathlib import Path
from typing import Any, Awaitable, Callable, Coroutine, List

# https://github.com/kerrickstaley/genanki
import genanki  # type: ignore
from tqdm import tqdm  # type: ignore

LEETCODE_ANKI_MODEL_ID = 4567610856
LEETCODE_ANKI_DECK_ID = 8589798175
OUTPUT_FILE = "leetcode.apkg"
ALLOWED_EXTENSIONS = {".py", ".go"}


logging.getLogger().setLevel(logging.INFO)


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments for the script
    """
    parser = argparse.ArgumentParser(description="Generate Anki cards for leetcode")
    parser.add_argument(
        "--start", type=int, help="Start generation from this problem", default=0
    )
    parser.add_argument(
        "--stop", type=int, help="Stop generation on this problem", default=2**64
    )
    parser.add_argument(
        "--page-size",
        type=int,
        help="Get at most this many problems (decrease if leetcode API times out)",
        default=500,
    )
    parser.add_argument(
        "--list-id",
        type=str,
        help="Get all questions from a specific list id (https://leetcode.com/list?selectedList=<list_id>",
        default="",
    )
    parser.add_argument(
        "--output-file", type=str, help="Output filename", default=OUTPUT_FILE
    )

    args = parser.parse_args()

    return args


class LeetcodeNote(genanki.Note):
    """
    Extended base class for the Anki note, that correctly sets the unique
    identifier of the note.
    """

    @property
    def guid(self) -> str:
        # Hash by leetcode task handle
        return genanki.guid_for(self.fields[0])


async def generate_anki_note(
    leetcode_data,
    leetcode_model: genanki.Model,
    leetcode_task_handle: str,
) -> LeetcodeNote:
    """
    Generate a single Anki flashcard
    """
    return LeetcodeNote(

        model=leetcode_model,
        fields=[
            leetcode_task_handle,
            str(leetcode_data[leetcode_task_handle]),
        ],
    )


async def generate(
    start: int, stop: int, page_size: int, list_id: str, input_file, output_file: str
) -> None:
    """
    Generate an Anki deck
    """
    leetcode_model = genanki.Model(
        LEETCODE_ANKI_MODEL_ID,
        "Leetcode model",
        fields=[
            {"name": "Slug"},
            {"name": "Title"},
            # {"name": "Topic"},
            # {"name": "Content"},
            # {"name": "Difficulty"},
            # {"name": "Paid"},
            # {"name": "Likes"},
            # {"name": "Dislikes"},
            # {"name": "SubmissionsTotal"},
            # {"name": "SubmissionsAccepted"},
            # {"name": "SumissionAcceptRate"},
            # {"name": "Frequency"},
            # TODO: add hints
        ],
        templates=[
            {
                "name": "Leetcode",
                "qfmt": """
                <h2>{{Title}}</h2>
                <b>URL:</b>
                <a href='{{Slug}}'>
                    {{Slug}}
                </a>
                <br/>
                """,
                "afmt": """
                {{FrontSide}}
                """,
            }
        ],
    )
    leetcode_deck = genanki.Deck(LEETCODE_ANKI_DECK_ID, Path(output_file).stem)

    note_generators: List[Awaitable[LeetcodeNote]] = []

    logging.info("Generating flashcards")
    for leetcode_task_handle in input_file.keys():
        note_generators.append(
            generate_anki_note(input_file, leetcode_model, leetcode_task_handle)
        )

    for leetcode_note in tqdm(note_generators, unit="flashcard"):
        leetcode_deck.add_note(await leetcode_note)

    genanki.Package(leetcode_deck).write_to_file(output_file)

def format_text_to_dict(file_path):
    formatted_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if ', ' in line:
                url, file_name = line.strip().split(', ', 1)
                formatted_dict[url] = file_name
    return formatted_dict

async def main() -> None:
    """
    The main script logic
    """
    args = parse_args()
    file_path = "files.txt"
    input_file = format_text_to_dict(file_path)
    
    start, stop, page_size, list_id, output_file = (
        args.start,
        args.stop,
        args.page_size,
        args.list_id,
        args.output_file,
    )
    await generate(start, stop, page_size, list_id, input_file, output_file)


if __name__ == "__main__":
    loop: asyncio.events.AbstractEventLoop = asyncio.get_event_loop()
    loop.run_until_complete(main())