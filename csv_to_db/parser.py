import os

import pandas as pd


def main():
    frame = pandas_frame_from_csv_path('../btw17_kerg.csv', lines_to_skip=2, sep=';')

    print(get_constituency_of(frame, 1))


def pandas_frame_from_csv_path(path, lines_to_skip=0, sep=','):
    """
    Reads a given file path and returns the pandas frame.
    See pandas_frame_from_csv_file().
    """

    with open(os.path.expanduser(path), 'r') as f:
        return pandas_frame_from_csv_file(f, lines_to_skip, sep)


def pandas_frame_from_csv_file(file, lines_to_skip=0, sep=','):
    """
    Reads a given file path and returns the pandas frame.

    :param file: a csv file object
    :param lines_to_skip: The number of lines at the beginning of the csv file to skip
    :param sep: The separator in the csv file
    :return: A pandas data frame, containing the data in the given file
    """

    for i in range(lines_to_skip):
        file.readline()

    return pd.read_csv(file, sep=sep)


def get_constituency_of(frame, state_id):
    """
    Returns a subset of the given frame, containing the constituencies which belong to the given state.

    :param frame: The pandas frame from where to extract the constituencies.
    :param state_id: The state id, whose subconstituencies are returned.
    :return: A pandas frame containing only the constituencies of the given state.
    """

    return frame[frame['gehört zu'] == state_id]


def get_states(frame):
    """
    Returns a subset of the given frame, containing only states.

    :param frame: The frame from which to extract the states.
    :return: A new pandas frame containing states.
    """

    return get_constituency_of(frame, 99)


if __name__ == '__main__':
    main()
