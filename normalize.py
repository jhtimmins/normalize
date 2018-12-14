import datetime
import numpy as np
import pandas as pd
import sys
from io import StringIO


def normalize(input_data):
    """Normalize source data and return as string or optionally save to file."""

    # df is the standard variable name for a DataFrame in Pandas.
    df = extract(input_data)
    df = transform_zip(df)
    df = transform_timestamp(df)
    df = transform_duration(df)

    return df.to_string()


def extract(input_data):
    """Extract data from source and return as DataFrame"""

    utf_8_data = input_data.decode("utf-8", "replace")
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


if __name__ == '__main__':
    input_data = sys.stdin.buffer.read()
    normalized = normalize(input_data)
    sys.stdout.write(normalized)
