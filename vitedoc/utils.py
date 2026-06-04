from typing import Literal
from pathlib import Path


class Action:
    """
    Represents an action element.

    Args:
        theme (str): The name of the theme. Supported themes are `brand` and `alt`.
        text (str): The text to display on the action button.
        link (str): The URL to navigate to when the action button is clicked.
    """

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
    """
    Represents a feature element.

    Args:
        icon_emoji (str): The emoji icon to use. Defaults to None.
        icon_path (str): The path to the icon. Defaults to None.
        title (str): The title of the feature. Defaults to None.
        details (str): The details of the feature. Defaults to None.

    Notes:
        `icon_emoji` and `icon_path` mutually exclusive. If both are provided, `icon_emoji` will take precedence.
    """
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

def find_packages(path: str):
    return [
        d.name
        for d in Path(".").iterdir()
        if d.is_dir() and (d / "__init__.py").is_file()
    ]
