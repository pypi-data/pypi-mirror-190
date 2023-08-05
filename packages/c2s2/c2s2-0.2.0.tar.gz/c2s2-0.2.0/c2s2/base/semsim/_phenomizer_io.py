import csv
import gzip
import io
import typing
from typing import Dict
from urllib.request import urlopen

from ._phenomizer import TermPair


def read_ic_mica_data(fpath: str, timeout=10) -> Dict[TermPair, float]:
    """Read a CSV table with information contents of most informative common ancestors from given `fpath`.

    The file is uncompressed on the fly if the file name ends with `.gz`.
    """
    with _open_file_handle(fpath, timeout) as fh:
        comments, header = _parse_header(fh, comment_char='#')
        fieldnames = header.split(",")
        reader = csv.DictReader(fh, fieldnames=fieldnames)

        # Read the lines
        mica = {}
        for row in reader:
            pair = TermPair.of(row['term_a'], row['term_b'])
            mica[pair] = float(row['ic_mica'])

        return mica


def _parse_header(fh, comment_char):
    """Parse header into a list of comments and a header line. As a side effect, the `fh` is set to the position where
    CSV parser can take over and read the records.

    :return: a tuple with a list of comment lines and the header line
    """
    comments = []
    header = None
    for line in fh:
        if line.startswith(comment_char):
            comments.append(line.strip())
        else:
            header = line.strip()
            break
    return comments, header


def _open_file_handle(fpath: str, timeout) -> typing.IO:
    looks_like_url = fpath.startswith('http://') or fpath.startswith('https://')
    looks_compressed = fpath.endswith('.gz')

    fh = urlopen(fpath, timeout=timeout) if looks_like_url else open(fpath, mode='rb')
    return gzip.open(fh, mode='rt', newline='') if looks_compressed else io.TextIOWrapper(fh, encoding='utf-8')
