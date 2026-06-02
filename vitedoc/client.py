import os


from .config import build
from .package import create_package_json
from .home import create_index_md

from .mapper import generate_map
from .autodoc import generate
from .sidebar import generate_vitepress_sidebar


def create_dir_structure(base: str):
    if not os.path.exists(base):
        os.mkdir(base)
    subdir = ['.vitepress', 'content', 'public']
    for subdir in subdir:
        path = os.path.join(base, subdir)
        if not os.path.exists(path):
            os.mkdir(path)

def init():
    while True:
        base = input("Enter base path (default: 'docs'): ") or 'docs'
        if os.path.exists(base):
            print(f"Directory '{base}' already exists. Please choose a different name.")
            break
        else:
            create_dir_structure(base)
            base_ = input("Enter base path of the documentation (default: 'vitedoc'): ") or 'vitedoc'
            title = input("Enter title of the documentation (default: 'ViteDoc'): ") or 'ViteDoc'
            description = input("Enter description of the documentation (default: '...'): ") or '...'
            logo = input("Enter logo path (default: '/favicon.png'): ") or '/favicon.png'
            create_package_json(os.path.join(base, 'package.json'))
            api_map_path = os.path.join(base, '.vitepress', 'api_map.json')
            package_path = input("Enter path to the package to document (default: '.'): ") or '.'
            package_name = package_path.split('/')[-1]
            create_index_md(
                os.path.join(base, 'index.md'),
                name=title,
                tagline=description,
                image_src=logo,
                actions=[
                    {
                        "theme": "brand",
                        "text": "Get Started",
                        "link": f"/content/{package_name}",
                    },
                    {
                        "theme": "alt",
                        "text": "View on GitHub",
                        "link": "https://github.com/xyz/pqr",
                    },
                ],
                features=[]
            )
            generate_map(package_path, api_map_path)
            sidebar = generate_vitepress_sidebar(api_map_path)
            build(
                path=os.path.join(base, '.vitepress', 'config.mts'),
                base=f'/{base_}/',
                title=title,
                description= description,
                logo=logo,
                sidebar=sidebar,
            )
            generate(
                out_dir=os.path.join(base, 'content'),
                input_json_path=api_map_path,
            )
            print(f"Documentation structure created successfully in '{base}' directory.")
            break
