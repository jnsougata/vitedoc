import json
import re


def format_docstring(doc):
    if not doc:
        return ""

    lines = doc.splitlines()
    result = []

    i = 0
    while i < len(lines):
        line = lines[i]

        if (
            i + 1 < len(lines)
            and set(lines[i + 1].strip()) == {"-"}
            and len(lines[i + 1].strip()) >= 3
        ):
            result.append(f"### {line.strip()}")
            result.append("")
            i += 2
            continue

        m = re.match(r"^(\w+)\s*:\s*(.+)$", line)

        if m:
            name, typ = m.groups()
            result.append(f"- **{name}** (`{typ}`)")
        else:
            result.append(line)

        i += 1

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
    if data.get("file"):
        md.append("### Source")
        md.append("")
        md.append(f"- File: `{data['file']}`")
        md.append(f"- Line: `{data['line']}`")
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
    if data.get("file"):
        md.append("### Source")
        md.append("")
        md.append(f"- File: `{data['file']}`")
        md.append(f"- Line: `{data['line']}`")
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
    if module_data.get("file"):
        md.append("## Module Information")
        md.append("")
        md.append(f"- File: `{module_data['file']}`")
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


# def render_index(api):
#     md = []
#
#     md.append("---")
#     md.append("title: API Reference")
#     md.append("---")
#     md.append("")
#
#     md.append("# API Reference")
#     md.append("")
#
#     md.append("## Modules")
#     md.append("")
#
#     for module_name in sorted(api["modules"]):
#         filename = module_name.replace(".", "_") + ".md"
#         md.append(f"- [{module_name}](./{filename})")
#
#     md.append("")
#
#     return "\n".join(md)

def generate(out_dir: str, input_json_path: str):
    with open(input_json_path, encoding="utf-8") as f:
        api = json.load(f)
    for module_name, module_data in api["modules"].items():
        if "error" in module_data:
            continue
        filename = module_name.replace(".", "_") + ".md"
        content = render_module(module_name, module_data)
        with open(f"{out_dir}/{filename}", "w", encoding="utf-8") as fp:
            fp.write(content)
        print("Generated:", filename)
