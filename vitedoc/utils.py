from typing import Literal


class Action:

    def __init__(
        self,
        *,
        theme: Literal["brand", "alt"],
        text: str,
        link: str,
    ):
        self.theme = theme
        self.text = text
        self.link = link

    def to_dict(self):
        return {"theme": self.theme, "text": self.text, "link": self.link}


class Feature:
    def __init__(
        self,
        *,
        icon_emoji: str = '',
        icon_path: str = '',
        title: str,
        details: str,
    ):
        if icon_emoji:
            self.icon = icon_emoji
        elif icon_path:
            self.icon = {"src": icon_path}
        self.title = title
        self.details = details

    def to_dict(self):
        return {"icon": self.icon, "title": self.title, "details": self.details}

from pathlib import Path

def find_packages(path: str):
    return [
        d.name
        for d in Path(".").iterdir()
        if d.is_dir() and (d / "__init__.py").is_file()
    ]
