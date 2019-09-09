import sys

import sys, getopt
import os
from jinja2 import Template, Environment, PackageLoader, select_autoescape, FileSystemLoader
import json
from git import Git

env = Environment(
    loader=FileSystemLoader(os.path.normpath(os.path.join(os.getcwd(), "./templates"))),
    autoescape=select_autoescape(['html', 'xml'])
)


def main(argv):
    path = ''
    outputfile = ''
    tagFrom = 'HEAD'
    tagTo = ''
    try:
        opts, args = getopt.getopt(argv, "i:f:t:o:", ["path=", "from=", "to=", "output="])
    except getopt.GetoptError:
        print('main.py -i <path to repo> -from <tag> -to <tag> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <path to repo> -from <tag> -to <tag> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--path"):
            path = os.path.normpath(os.path.join(os.getcwd(), arg))
        elif opt in ("-f", "--from"):
            tagFrom = arg
        elif opt in ("-t", "--to"):
            tagTo = arg
        elif opt in ("-o", "--output"):
            outputfile = os.path.normpath(os.path.join(os.getcwd(), arg))

    print('Path of project is "', path)
    print('Output file is "', outputfile)
    isDir = os.path.isdir(path)
    if not isDir:
        print("Not a valid directory...")
        sys.exit(1)

    g = Git(path)
    logFormat = '{"hash":"%h","author":"%an","msg":"%s","pretty":"%h by %an : %s","time":"%ar"}'
    # git log --pretty=short --format="%h %s by %an , %ar%n" --no-abbrev-commit  --date-order v1.2.0...v1.0.0
    loginfo = g.log('--pretty=short', '--format=' + logFormat, "--no-abbrev-commit", "--date-order",
                    tagFrom + '...' + tagTo)
    separator = ","
    parts = loginfo.split('\n')

    commitsAsJson = "["+separator.join(parts)+"]"


    commits = json.loads(commitsAsJson)


    t = env.get_template("main.html")

    f = open(outputfile, "w+")
    f.write(t.render(title=tagFrom,commits=commits))
    f.close()


if __name__ == "__main__":
    main(sys.argv[1:])
