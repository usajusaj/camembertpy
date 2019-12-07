import bri


def create_index(args):
    b = bri.Bri(args.bam_file)
    b.create()


def get_read(args):
    b = bri.Bri(args.bam_file)
    b.load()
    for read in b.get(args.read_name):
        print(read.to_string())


def main():
    import argparse
    parser = argparse.ArgumentParser("Interface to bri")

    command_parsers = parser.add_subparsers(title='Available subcommands',
                                            dest='command',
                                            description='For detailed subcommand help run: <subcommand> -h.')

    index_parser = command_parsers.add_parser('index')
    index_parser.add_argument('bam_file')
    index_parser.set_defaults(func=create_index)

    get_parser = command_parsers.add_parser('get')
    get_parser.add_argument('bam_file')
    get_parser.add_argument('read_name')
    get_parser.set_defaults(func=get_read)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
