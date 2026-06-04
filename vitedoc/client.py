import os
import re
from typing import Optional

from .config import generate_config
from .package import create_package_json
from .home import homepage

from .mapper import _map
from .autodoc import autodoc
from .sidebar import _sidebar
from .utils import Feature, Action, find_packages


def create_dir_structure(base: str):
    if not os.path.exists(base):
        os.mkdir(base)
    subdir = ['.vitepress', 'public', "guide"]
    for subdir in subdir:
        path = os.path.join(base, subdir)
        if not os.path.exists(path):
            os.mkdir(path)

def init(
    base_dir: str = "docs",
    *,
    title: str = "ViteDoc",
    description: str = "Hello there!",
    logo_path: str = "/logo.png",
    actions: Optional[list[Action]] = None,
    features: Optional[list[Feature]] = None,
    package_path: str = ".",
):
    create_dir_structure(base_dir)
    create_package_json(os.path.join(base_dir, 'package.json'))
    api_map_path = os.path.join(base_dir, '.vitepress', 'api.json')
    package_paths = find_packages(package_path)
    assert len(package_paths) > 0, f"No package found in path: {package_path}"
    assert len(package_paths) == 1, f"Multiple packages found in path: {package_path}"
    package_path = package_paths[0]
    version = ""
    with open(f"{package_path}/__init__.py") as f:
        version = re.search(
            r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
        ).group(1)
    _map(package_path, api_map_path)
    package_name = package_path.split('/')[-1]
    generate_config(
        path=os.path.join(base_dir, '.vitepress', 'config.mts'),
        base=f'/{package_name}/',
        title=title,
        description=description,
        logo=logo_path,
        sidebar=_sidebar(api_map_path, package_name, version),
    )
    autodoc(
        out_dir=os.path.join(base_dir, "guide", version),
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
