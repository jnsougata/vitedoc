import json
import os
import re
from textwrap import dedent


def render_docstring(doc):
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
        "Attributes:": "### Attributes",
        "Members:": "### Attributes",
        "Returns:": "### Returns",
        "Yields:": "### Yields",
        "Raises:": "### Raises",
        "Examples:": "### Examples",
        "Notes:": "### Notes",
        "Warning:": "### Warning",
        "Warnings:": "### Warnings",
    }

    SECTION_NAMES = {
        "args": "args",
        "arguments": "args",
        "parameters": "args",
        "attributes": "attributes",
        "members": "attributes",
        "returns": "returns",
        "yields": "yields",
        "raises": "raises",
        "examples": "examples",
        "notes": "notes",
        "warning": "warning",
        "warnings": "warning",
    }

    for line in lines:
        stripped = line.strip()

        if not stripped:
            result.append("")
            continue

        if stripped in SECTION_HEADERS:
            section = SECTION_NAMES[stripped[:-1].lower()]

            result.append(SECTION_HEADERS[stripped])
            result.append("")

            last_item = None
            continue

        if section in {"args", "attributes"}:
            m = re.match(
                r"^\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]+)\):\s*(.*)$",
                line,
            )

            if m:
                name, typ, desc = m.groups()

                result.append(
                    f"- **{name}** (`{typ}`): {desc}"
                )

                last_item = len(result) - 1
                continue

            m = re.match(
                r"^\s+([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$",
                line,
            )

            if m:
                name, desc = m.groups()

                result.append(
                    f"- **{name}**: {desc}"
                )

                last_item = len(result) - 1
                continue

            if (
                last_item is not None
                and line.startswith((" " * 8, "\t"))
            ):
                result[last_item] += f" {stripped}"
                continue

        elif section in {"returns", "yields"}:
            m = re.match(
                r"^\s+([^:]+):\s*(.*)$",
                line,
            )

            if m:
                typ, desc = m.groups()

                result.append(
                    f"- **Type:** `{typ.strip()}`"
                )

                if desc:
                    result.append(f"  - {desc}")
                    last_item = len(result) - 1
                else:
                    last_item = len(result) - 1

                continue

            if (
                last_item is not None
                and line.startswith((" " * 8, "\t"))
            ):
                result[last_item] += f" {stripped}"
                continue

        elif section == "raises":
            m = re.match(
                r"^\s+([^:]+):\s*(.*)$",
                line,
            )

            if m:
                exc, desc = m.groups()

                result.append(
                    f"- **{exc.strip()}**: {desc}"
                )

                last_item = len(result) - 1
                continue

            if (
                last_item is not None
                and line.startswith((" " * 8, "\t"))
            ):
                result[last_item] += f" {stripped}"
                continue

        elif section == "examples":
            result.append(code_block(stripped))
            continue

        else:
            result.append(stripped)

    while result and not result[-1].strip():
        result.pop()

    return "\n".join(result)


def code_block(text):
    return f"```python\n{text}\n```"


def make_anchor(name):
    return re.sub(
        r"[^a-z0-9-]",
        "",
        name.lower().replace("_", "-"),
    )


def render_function(name, data):
    md = []

    md.append(f'<a id="{make_anchor(name)}"></a>')
    md.append(f"## `{name}`")
    md.append("")

    if data.get("qualified_name"):
        md.append(
            f"**Qualified Name:** `{data['qualified_name']}`"
        )
        md.append("")

    if data.get("signature"):
        prefix = "async " if data.get("async") else ""

        md.append("### Signature")
        md.append("")
        md.append(
            code_block(
                f"{prefix}{name}{data['signature']}"
            )
        )
        md.append("")

    if data.get("docstring"):
        md.append(render_docstring(data["docstring"]))
        md.append("")

    return "\n".join(md)


def render_method(class_name, method_name, data):
    md = []

    anchor = make_anchor(
        f"{class_name}-{method_name}"
    )

    md.append(f'<a id="{anchor}"></a>')
    md.append(f"#### `{method_name}`")
    md.append("")

    if data.get("signature"):
        prefix = "async " if data.get("async") else ""

        md.append(
            code_block(
                f"{prefix}{method_name}"
                f"{data['signature']}"
            )
        )
        md.append("")

    if data.get("docstring"):
        md.append(render_docstring(data["docstring"]))
        md.append("")

    return "\n".join(md)


def render_property(class_name, prop_name, data):
    md = []

    anchor = make_anchor(
        f"{class_name}-{prop_name}"
    )

    md.append(f'<a id="{anchor}"></a>')
    md.append(f"#### `{prop_name}`")
    md.append("")

    if data.get("docstring"):
        md.append(render_docstring(data["docstring"]))
        md.append("")

    return "\n".join(md)


def render_class(name, data):
    md = []

    md.append(
        f'<a id="{make_anchor(f"class-{name}")}"></a>'
    )
    md.append(f"## Class `{name}`")
    md.append("")

    if data.get("qualified_name"):
        md.append(
            f"**Qualified Name:** "
            f"`{data['qualified_name']}`"
        )
        md.append("")

    if data.get("docstring"):
        md.append(render_docstring(data["docstring"]))
        md.append("")

    if data.get("bases"):
        md.append("### Inheritance")
        md.append("")

        for base in data["bases"]:
            md.append(f"- `{base}`")

        md.append("")

    properties = data.get("properties", {})
    methods = data.get("methods", {})

    if properties:
        md.append("### Property Index")
        md.append("")

        for prop_name in sorted(properties):
            anchor = make_anchor(
                f"{name}-{prop_name}"
            )

            md.append(
                f"- [{prop_name}](#{anchor})"
            )

        md.append("")

    if methods:
        md.append("### Method Index")
        md.append("")

        for method_name in sorted(methods):
            anchor = make_anchor(
                f"{name}-{method_name}"
            )

            md.append(
                f"- [{method_name}](#{anchor})"
            )

        md.append("")

    if properties:
        md.append("### Properties")
        md.append("")

        for prop_name in sorted(properties):
            md.append(
                render_property(
                    name,
                    prop_name,
                    properties[prop_name],
                )
            )

    if methods:
        md.append("### Methods")
        md.append("")

        for method_name in sorted(methods):
            md.append(
                render_method(
                    name,
                    method_name,
                    methods[method_name],
                )
            )

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
        md.append(render_docstring(module_data["docstring"]))
        md.append("")

    classes = module_data.get("classes", {})
    functions = module_data.get("functions", {})

    if classes:
        md.append("## Classes")
        md.append("")

        for cls_name in sorted(classes):
            md.append(
                f"- [{cls_name}]"
                f"(#{make_anchor(f'class-{cls_name}')})"
            )

        md.append("")

    if functions:
        md.append("## Functions")
        md.append("")

        for fn_name in sorted(functions):
            md.append(
                f"- [{fn_name}]"
                f"(#{make_anchor(fn_name)})"
            )

        md.append("")

    for cls_name in sorted(classes):
        md.append(
            render_class(
                cls_name,
                classes[cls_name],
            )
        )
        md.append("")

    for fn_name in sorted(functions):
        md.append(
            render_function(
                fn_name,
                functions[fn_name],
            )
        )
        md.append("")

    return "\n".join(md)

def autodoc(out_dir: str, input_json_path: str):
    with open(input_json_path, encoding="utf-8") as f:
        api = json.load(f)

    os.makedirs(out_dir, exist_ok=True)

    for module_name, module_data in api["modules"].items():
        if "error" in module_data:
            continue

        full_path = os.path.join(
            out_dir,
            module_name.split(".")[-1] + ".md",
        )

        os.makedirs(
            os.path.dirname(full_path),
            exist_ok=True,
        )

        content = render_module(
            module_name,
            module_data,
        )

        with open(
            full_path,
            "w",
            encoding="utf-8",
        ) as fp:
            fp.write(content)

        print("Generated:", full_path)