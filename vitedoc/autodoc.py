import json
import re
from textwrap import dedent

def format_docstring(doc):
    if not doc:
        return ""

    lines = dedent(doc).splitlines()
    result = []

    section = None
    last_item = None

    SECTION_HEADERS = {
        "Args:": "### Arguments",
        "Arguments:": "### Arguments",
        "Parameters:": "### Arguments",
        "Returns:": "### Returns",
        "Yields:": "### Yields",
        "Raises:": "### Raises",
        "Examples:": "### Examples",
        "Notes:": "### Notes",
    }

    for line in lines:
        stripped = line.strip()

        if not stripped:
            result.append("")
            continue

        if stripped in SECTION_HEADERS:
            section = stripped[:-1].lower()
            result.append(SECTION_HEADERS[stripped])
            result.append("")
            last_item = None
            continue

        if section == "args":
            m = re.match(
                r"^\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]+)\):\s*(.*)$",
                line,
            )

            if m:
                name, typ, desc = m.groups()
                result.append(f"- **{name}** (`{typ}`): {desc}")
                last_item = len(result) - 1
                continue

            if last_item is not None and line.startswith(" " * 8):
                result[last_item] += f" {stripped}"
                continue

        elif section == "returns":
            m = re.match(r"^\s+([^:]+):\s*(.*)$", line)

            if m:
                typ, desc = m.groups()
                result.append(f"- **Type:** `{typ.strip()}`")
                if desc:
                    result.append(f"  - {desc}")
                last_item = len(result) - 1
                continue

            if last_item is not None and line.startswith(" " * 8):
                result[last_item] += f" {stripped}"
                continue

        elif section == "raises":
            m = re.match(r"^\s+([^:]+):\s*(.*)$", line)

            if m:
                exc, desc = m.groups()
                result.append(f"- **{exc.strip()}**: {desc}")
                last_item = len(result) - 1
                continue

        result.append(stripped)

    return "\n".join(result)


def code_block(text):
    return f"```python\n{text}\n```"


def make_anchor(name):
    return name.lower().replace("_", "-")


def render_function(name, data):
    md = []
    md.append(f"## `{name}`")
    md.append("")
    if data.get("signature"):
        md.append("### Signature")
        md.append("")
        md.append(code_block(f"{name}{data['signature']}"))
        md.append("")
    if data.get("docstring"):
        md.append(format_docstring(data["docstring"]))
        md.append("")
    return "\n".join(md)


def render_method(name, data):
    md = []
    md.append(f"#### `{name}`")
    md.append("")
    if data.get("signature"):
        md.append(code_block(f"{name}{data['signature']}"))
        md.append("")
    if data.get("docstring"):
        md.append(format_docstring(data["docstring"]))
        md.append("")
    return "\n".join(md)


def render_class(name, data):
    md = []
    md.append(f"## Class `{name}`")
    md.append("")
    if data.get("docstring"):
        md.append(format_docstring(data["docstring"]))
        md.append("")
    if data.get("bases"):
        md.append("### Inheritance")
        md.append("")
        for base in data["bases"]:
            md.append(f"- `{base}`")
        md.append("")
    methods = data.get("methods", {})
    if methods:
        md.append("### Methods")
        md.append("")
        for method_name in sorted(methods):
            md.append(render_method(method_name, methods[method_name]))
    return "\n".join(md)


def render_module(module_name, module_data):
    md = []
    md.append("---")
    md.append(f"title: {module_name}")
    md.append("---")
    md.append("")
    md.append(f"# `{module_name}`")
    md.append("")
    if module_data.get("docstring"):
        md.append(module_data["docstring"])
        md.append("")
    classes = module_data.get("classes", {})
    functions = module_data.get("functions", {})

    if classes:
        md.append("## Classes")
        md.append("")
        for cls_name in sorted(classes):
            md.append(f"- [{cls_name}](#{make_anchor(f'class-{cls_name}')})")
        md.append("")
        for cls_name in sorted(classes):
            md.append(render_class(cls_name, classes[cls_name]))
            md.append("")
    if functions:
        md.append("## Functions")
        md.append("")
        for fn_name in sorted(functions):
            md.append(f"- [{fn_name}](#{make_anchor(fn_name)})")
        md.append("")
        for fn_name in sorted(functions):
            md.append(render_function(fn_name, functions[fn_name]))
            md.append("")
    return "\n".join(md)

def autodoc(out_dir: str, input_json_path: str):
    with open(input_json_path, encoding="utf-8") as f:
        api = json.load(f)
    for module_name, module_data in api["modules"].items():
        if "error" in module_data:
            continue
        filename = module_name.split(".")[-1] + ".md"
        content = render_module(module_name, module_data)
        with open(f"{out_dir}/{filename}", "w", encoding="utf-8") as fp:
            fp.write(content)
        print("Generated:", filename)
