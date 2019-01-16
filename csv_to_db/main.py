from parser import pandas_frame_from_csv_path


def main():
    frame = pandas_frame_from_csv_path('../btw17_kerg.csv', lines_to_skip=2, sep=';')
    print(frame)


if __name__ == '__main__':
    main()
