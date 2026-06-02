import json


def create_package_json(path: str):
    with open(path, 'w') as f:
        f.write(json.dumps(
            {
                "devDependencies": {
                    "vitepress": "^1.6.3"
                },
                "scripts": {
                    "docs:dev": "vitepress dev",
                    "docs:build": "vitepress build && echo app_type: static > ./.vitepress/dist/vitedoc.yaml",
                    "docs:preview": "vitepress preview"
                }
            }, indent=4
        ))
