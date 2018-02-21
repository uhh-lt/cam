import argparse

def run_flask(parameter):
    print(parameter)


def main():
    parser = argparse.ArgumentParser(description='description of the job.')
    parser.add_argument('-host', help="host server. Default http localhost 99222", default="http localhost 99222")
    args = parser.parse_args()

    run_flask(args.host)

if __name__ == '__main__':
    main()