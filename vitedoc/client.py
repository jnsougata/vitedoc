import os
from typing import Optional

from .config import build
from .package import create_package_json
from .home import homepage

from .mapper import _map
from .autodoc import autodoc
from .sidebar import _sidebar
from .utils import Feature, Action, find_packages


def create_dir_structure(base: str):
    if not os.path.exists(base):
        os.mkdir(base)
    subdir = ['.vitepress', 'content', 'public']
    for subdir in subdir:
        path = os.path.join(base, subdir)
        if not os.path.exists(path):
            os.mkdir(path)

def init(
    base_dir: str = "docs",
    *,
    title: str = "ViteDoc",
    description: str = "Hello there!",
    logo_path: str = "/favicon.png",
    actions: Optional[list[Action]] = None,
    features: Optional[list[Feature]] = None,
    package_path: str = ".",
):
    # if os.path.exists(base_dir):
    #     print(f"Directory '{base_dir}' already exists. Please choose a different name.")
    #     return
    create_dir_structure(base_dir)
    create_package_json(os.path.join(base_dir, 'package.json'))
    api_map_path = os.path.join(base_dir, '.vitepress', 'api_map.json')
    package_path = find_packages(package_path)
    if len(package_path) >= 1:
        package_path = package_path[0]
    _map(package_path, api_map_path)
    package_name = package_path.split('/')[-1]
    build(
        path=os.path.join(base_dir, '.vitepress', 'config.mts'),
        base=f'/{package_name}/',
        title=title,
        description=description,
        logo=logo_path,
        sidebar=_sidebar(api_map_path),
    )
    autodoc(
        out_dir=os.path.join(base_dir, 'content'),
        input_json_path=api_map_path,
    )
    actions = [action.to_dict() for action in actions] if actions else []
    features = [feature.to_dict() for feature in features] if features else []
    homepage(
        os.path.join(base_dir, 'index.md'),
        name=title,
        tagline=description,
        image_src=logo_path,
        actions=actions,
        features=features
    )
    print(f"Documentation structure created successfully in '{base_dir}' directory.")
