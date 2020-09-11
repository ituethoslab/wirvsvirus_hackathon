# Extract submission descriptions into a collection of text files.

import json
import os
from zipfile import ZipFile
from bs4 import BeautifulSoup
from tqdm import tqdm


def read_datafile(path):
    """Load the datafile of submissions."""
    with open(DATAFILE) as fd:
        data = json.load(fd)
        return data


def write_descriptions(submissions, directory, serve_soup=False):
    """Write the submission descriptions each into a separate text file."""
    for submission in tqdm(submissions):
        if serve_soup:
            text = submission['description']
            ext = '.html'
        else:
            soup = BeautifulSoup(submission['description'], 'html.parser')
            text = soup.get_text()
            text = '\n\n'.join([p.get_text() for p in soup.find_all('p')])
            ext = '.txt'

        # Prepare directory
        try:
            os.makedirs(directory)
        except OSError:
            pass

        # Write them out
        with open(f"{directory}/{submission['title'].replace('/', '_')}{ext}", 'w') as fd:
            fd.write(text)


def create_zip(directory):
    """Zip the descriptions for transmission."""
    parent_dir = os.path.dirname(directory)
    final_dir = os.path.basename(directory)
    os.chdir(parent_dir)

    with ZipFile(final_dir + '.zip', 'w') as zipfile:
        for desc_file in tqdm(os.listdir(final_dir)):
            zipfile.write(os.path.join(final_dir, desc_file))


if __name__ == '__main__':
    DATAFILE = 'data/submissionsWithDetail20200331_171116.json'
    DESC_DIRECTORY = 'tmp/submission_descriptions'

    submissions = read_datafile(DATAFILE)

    write_descriptions(submissions, DESC_DIRECTORY)
    create_zip(DESC_DIRECTORY)
