import glob
import sys

def get_all_requirement_files_names():
    paths = [path for path in glob.iglob('./toolbox/*/requirements.txt')]
    return [(path, path.split('/')[2]) for path in paths]

def filter_requirement_files(path_and_name, filter_list):
    return [(path, library_type) for path, library_type in path_and_types
            if library_type in filter_list]

all_requirement_files = get_all_requirement_files_names()

all_libraries_to_export = sys.argv[1:]
if len(all_libraries_to_export) != 0:
    all_requirement_files = filter_requirement_files(all_requirement_files, sys.argv[1:])

already_seen = {}

for requirement_path, library_name in all_requirement_files:
    print('## {0}'.format(library_name))
    for line in open(requirement_path, 'rb'):
        requirement = line.strip()
        if requirement in already_seen:
            print('# {0} - Already included in {1}'.format(requirement, already_seen[requirement]))
        else:
            print(requirement)
            already_seen[requirement] = library_name