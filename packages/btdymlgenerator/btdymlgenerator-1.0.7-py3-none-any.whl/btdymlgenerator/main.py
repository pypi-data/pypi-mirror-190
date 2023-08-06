import argparse
import json
import os
import yaml


def json_to_yaml(json_file, search_names=None):
    with open(json_file, 'r') as f:
        data = json.load(f)

    yaml_data = {}
    targets = data.get('targets')
    for target in targets:
        name = target.get('name')
        podspec = target.get('podspec')
        sub_data = {}
        for item in podspec:
            if not search_names or item.get('name') in search_names:
                sub_data[item.get('name')] = [
                    spec[len(item.get('name')) + 1:] for spec in item.get('subspecs')
                ]
        if sub_data:
            yaml_data[name] = sub_data

    yaml_file = 'output.yaml'
    with open(yaml_file, 'w') as f:
        yaml.dump(yaml_data, f)

    print(f'YAML file saved to: {os.path.abspath(yaml_file)}')


def main():
    parser = argparse.ArgumentParser(
        description='Convert JSON file to YAML file')
    parser.add_argument('json_file', type=str, help='input JSON file')
    parser.add_argument('-s', '--search_names', type=str,
                        nargs='+', help='list of search names')
    args = parser.parse_args()

    # 打印参数
    print(args)

    json_to_yaml(args.json_file, args.search_names)

    json_to_yaml("deps.json", "BDWebImageView")


if __name__ == '__main__':
    main()
