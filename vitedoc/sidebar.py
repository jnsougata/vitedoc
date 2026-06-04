import json
from collections import defaultdict


def _sidebar(api_json_path, pkg_prefix, version):
    with open(api_json_path, encoding="utf-8") as f:
        api = json.load(f)

    groups = defaultdict(list)

    sidebar = [
        {
            "text": "Introduction",
            "items": [],
        },
        {
            "text": "Reference",
            "items": [],
        }
    ]

    for module_name, module_data in api["modules"].items():
        if "error" in module_data:
            continue

        parts = module_name.split(".")

        if len(parts) == 1:
            sidebar[0]["items"].append(
                {
                    "text": "Getting Started",
                    "link": f"/guide/{version}/introduction",
                }
            )
        else:
            groups[parts[1].replace("_", " ").title()].append(module_name)

    for group_name in sorted(groups):
        for module_name in sorted(groups[group_name]):
            parts = module_name.split(".")

            if len(parts) == 1:
                title = module_name
            else:
                title = parts[-1].replace("_", " ").title()
            sidebar[1]["items"].append(
                {
                    "text": title,
                    "link": f"/guide/{version}/{module_name.split('.')[-1]}",
                }
            )

    return sidebar


if __name__ == "__main__":
    sidebar = _sidebar("api_map.json")
    print(json.dumps(sidebar, indent=2))