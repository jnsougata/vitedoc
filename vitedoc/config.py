import json
from pathlib import Path


def generate_config(
    path: str,
    *,
    base: str,
    title: str,
    description: str,
    logo: str,
    nav: list[dict[str, str]] | None = None,
    edit_link_pattern: str = "",
    sidebar: list[dict[str, list[dict[str, str]]]] | None = None,
    social_links: list[dict[str, str]] | None = None,
):
    nav = nav or []
    sidebar = sidebar or []
    social_links = social_links or []

    head = [["link", {"rel": "icon", "href": logo}]]

    nav_json = json.dumps(nav, indent=4)
    sidebar_json = json.dumps(sidebar, indent=4)
    social_links_json = json.dumps(social_links, indent=4)
    head_json = json.dumps(head, indent=4)

    config = f"""import {{ defineConfig }} from "vitepress";

export default defineConfig({{
    base: {json.dumps(base)},
    title: {json.dumps(title)},
    description: {json.dumps(description)},
    cleanUrls: true,

    head: {head_json},

    themeConfig: {{
        logo: {json.dumps(logo)},

        nav: {nav_json},

        editLink: {{
            pattern: {json.dumps(edit_link_pattern)},
        }},

        sidebar: {sidebar_json},

        search: {{
            provider: "local",
            options: {{
                _render: (src, env, md) => {{
                    if (env.relativePath.startsWith("docs")) {{
                        return "";
                    }}
                    return md.render(src, env);
                }},
            }},
        }},

        socialLinks: {social_links_json},
    }},
}});
"""

    Path(path).write_text(config, encoding="utf-8")