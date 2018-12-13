import datetime
import numpy as np
import pandas as pd
import sys
from io import StringIO


def normalize(source, dest=None):
    """Normalize source data and return as string or optionally save to file."""
    df = extract(source)
    df = transform_zip(df)
    df = transform_timestamp(df)
    df = transform_duration(df)
    load(df, dest)


def extract(source):
    """Extract data from source and return as DataFrame"""
    with open(source, "rb") as f:
        # Replace non-Unicode values with Unicode Replacement Character.
        utf_8_data = f.read().decode("utf-8", "replace")
    utf_8_rows = utf_8_data.split('\n')

    # Capitalize column headers.
    columns = utf_8_rows.pop(0).upper()

    valid_rows = [columns]
    for row in utf_8_rows:
        pieces = row.split(',')
        # Remove too-short trailing rows.
        if len(pieces) < 8:
            continue
        timestamp = pieces[0]
        replace = '�'
        if replace  in timestamp:
            # log # WARNING:
            sys.stderr.write("Warning: invalid timestamp: {}".format(row))
            continue
        valid_rows.append(row)

    reassembled_data = '\n'.join(valid_rows)
    return pd.read_csv(StringIO(reassembled_data), parse_dates=['TIMESTAMP'], encoding='utf-8')


def transform_zip(df):
    """Normalize ZIP length to 5 digits."""
    df['ZIP'] = df['ZIP'].apply('{:0>5}'.format)

    return df


def transform_timestamp(df):
    """Convert TIMESTAMP to East Coast time and format as ISO-8601"""
    df['TIMESTAMP'] = df['TIMESTAMP'].dt.tz_localize('America/Los_Angeles').dt.tz_convert('America/New_York')
    df['TIMESTAMP'] = df['TIMESTAMP'].dt.strftime('%Y-%m-%dT%H:%M:%S%z')

    return df


def duration_to_seconds(duration):
    """Convert a duration string to a seconds integer."""
    replace = '�'
    if replace in duration:
        sys.stderr.write("Warning: invalid duration: {}".format(duration))
        return 0
    pieces = duration.split(':')
    pieces.reverse()
    seconds = 0.0
    if len(pieces) > 0:
      seconds += float(pieces[0])
    if len(pieces) > 1:
      seconds += float(pieces[1]) * 60
    if len(pieces) > 2:
      seconds += float(pieces[2]) * 3600
    return seconds


def transform_duration(df):
    df['FOODURATION'] = df['FOODURATION'].apply(duration_to_seconds)
    df['BARDURATION'] = df['BARDURATION'].apply(duration_to_seconds)
    df['TOTALDURATION'] = df['FOODURATION'] + df['BARDURATION']

    return df


def load(df, dest):
    if dest:
        df.to_csv(dest)
        return
    print(df.to_string())


if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Please include a source file and an optional destination filename.")
        exit()

    source = sys.argv[1]

    if len(sys.argv) > 2:
        dest = sys.argv[2]
    else:
        dest = None

    normalize(source, dest)
