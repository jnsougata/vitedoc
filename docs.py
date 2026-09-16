import re
import vitedoc
from vitedoc import Action, Feature


version = ""
with open("vitedoc/__init__.py") as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)  # type: ignore

if __name__ == '__main__':
    vitedoc.init(
        base_dir="docs",
        title="vitedoc",
        description="An automatic documentation generator for vitepress.",
        actions=[
            Action(
                theme="brand",
                text="Get started",
                link=f"/guide/{version}/introduction",
            ),
            Action(
                theme="alt",
                text="GitHub",
                link="https://github.com/jnsougata/vitedoc"
            ),
        ],
        features=[
            Feature(
                icon_emoji="🚀",
                title="Fast",
                details="Vitedoc is designed to be fast and efficient, allowing you to generate documentation "
                        "quickly and easily without sacrificing quality."
            ),
            Feature(
                icon_emoji="🧩",
                title="Automatic",
                details="Vitedoc automatically generates documentation for your project, saving you time and effort "
                        "while ensuring that your documentation is always up-to-date."
            ),
            Feature(
                icon_emoji="📝",
                title="Easy",
                details="Vitedoc is easy to use and provides a simple interface for generating documentation, making it accessible to both beginners and experienced developers."
            )
        ]
    )
