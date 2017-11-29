import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=(
        'Run anything'))

    # common settings
    parser.add_argument('-p', '--proj', default='',
                        dest='proj_name',
                        help='project name to execute')

    args = parser.parse_args()

    if args.proj_name == 'preprocess':
        # preprocess code
        from proj.preprocess import run
        run.run()
    elif args.proj_name == 'upload':
        # upload to firestore
        from proj.upload import run
        run.run()
    else:
        # preprocess and upload
        from proj.preprocess import run as preprocess
        from proj.upload import run as upload
        preprocess.run()
        upload.run()
