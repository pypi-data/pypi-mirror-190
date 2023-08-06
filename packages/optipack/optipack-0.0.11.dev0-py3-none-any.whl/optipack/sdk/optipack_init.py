import os
from rich.tree import Tree
from rich.text import Text


def _generate_folder_structure(parent_dir: str, folder_structure: list, tree: Tree):
    if not folder_structure:
        print('End of folder tree...')
        return

    fs = folder_structure.pop()
    folder = fs

    if isinstance(fs, dict):
        folder = str(list(fs.keys())[0])
        new_dir = os.path.join(parent_dir, folder)
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
        inner_tree = tree.add(Text(folder))
        _generate_folder_structure(new_dir, fs[folder], inner_tree)
    else:
        icon = "🌱"
        tree.add(Text(icon) + folder)
        new_dir = os.path.join(parent_dir, folder)
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
    _generate_folder_structure(parent_dir, folder_structure, tree)


def _generate_yaml_file():
    ...


def init(
    env: str = '',
    project_name: str = '',
    parent_dir: str = '',
    structure_dir: str = './config/project_structure.yaml'
):
    from optipack.util import load_yaml
    from rich import print

    assert env, 'Empty environment'
    assert project_name, 'Empty project name'

    # 0. print hello
    # 1. create parent_dir
    if not parent_dir:
        parent_dir = os.path.join('.', project_name)

    if not os.path.exists(parent_dir):
        os.mkdir(parent_dir)

    # 2. create folder structure
    structure_dict = load_yaml(structure_dir)
    fs = structure_dict.get('project_structure')
    tree = Tree(f'🌲 {project_name} folder structure')

    _generate_folder_structure(
        parent_dir=parent_dir,
        folder_structure=fs,
        tree=tree
    )
    print(tree)
