import yaml

def create_index_md(
    path: str,
    *,
    name: str,
    tagline: str,
    image_src: str,
    actions: list[dict],
    features: list[dict],
) -> None:
    data = {
        "layout": "home",
        "hero": {
            "name": name,
            "tagline": tagline,
            "image": {
                "src": image_src,
                "alt": f"{name} logo",
            },
            "actions": actions,
        },
        "features": features,
    }

    with open(path, "w", encoding="utf-8") as f:
        f.write("---\n")
        yaml.safe_dump(
            data,
            f,
            sort_keys=False,
            allow_unicode=True,
        )
        f.write("---\n")