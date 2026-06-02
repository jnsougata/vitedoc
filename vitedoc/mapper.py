import pkgutil
import importlib
import inspect
import json


def safe_signature(obj):
    try:
        return str(inspect.signature(obj))
    except Exception:
        return None


def safe_source_info(obj):
    try:
        file = inspect.getsourcefile(obj)
        line = inspect.getsourcelines(obj)[1]

        return {
            "file": file,
            "line": line,
        }
    except Exception:
        return {
            "file": None,
            "line": None,
        }


def extract_function(func):
    return {
        "name": func.__name__,
        "signature": safe_signature(func),
        "docstring": inspect.getdoc(func),
        **safe_source_info(func),
    }


def extract_class(cls):
    methods = {}
    properties = {}

    for name, member in inspect.getmembers(cls):
        if name.startswith("_"):
            continue

        if isinstance(member, property):
            properties[name] = {
                "docstring": inspect.getdoc(member),
            }

        elif (
            inspect.isfunction(member)
            or inspect.ismethod(member)
            or inspect.ismethoddescriptor(member)
        ):
            methods[name] = {
                "signature": safe_signature(member),
                "docstring": inspect.getdoc(member),
                **safe_source_info(member),
            }

    return {
        "name": cls.__name__,
        "docstring": inspect.getdoc(cls),
        "bases": [
            f"{base.__module__}.{base.__name__}"
            for base in cls.__bases__
            if base is not object
        ],
        "properties": properties,
        "methods": methods,
        **safe_source_info(cls),
    }


def extract_module(module):
    classes = {}
    functions = {}

    for name, obj in inspect.getmembers(module):
        try:
            if inspect.isclass(obj) and obj.__module__ == module.__name__:
                classes[name] = extract_class(obj)

            elif inspect.isfunction(obj) and obj.__module__ == module.__name__:
                functions[name] = extract_function(obj)

        except Exception as e:
            print(f"Warning: failed to inspect {module.__name__}.{name}: {e}")

    return {
        "name": module.__name__,
        "docstring": inspect.getdoc(module),
        "file": inspect.getsourcefile(module),
        "classes": classes,
        "functions": functions,
    }


def build_package_map(package_name):
    package = importlib.import_module(package_name)

    api = {
        "package": package_name,
        "modules": {},
    }

    api["modules"][package.__name__] = extract_module(package)

    if hasattr(package, "__path__"):
        for _, module_name, _ in pkgutil.walk_packages(
            package.__path__,
            package.__name__ + "."
        ):
            try:
                module = importlib.import_module(module_name)
                api["modules"][module_name] = extract_module(module)

            except Exception as e:
                api["modules"][module_name] = {
                    "error": str(e)
                }

    return api


def generate_summary(api):
    module_count = len(api["modules"])

    class_count = 0
    function_count = 0
    method_count = 0

    for module in api["modules"].values():
        class_count += len(module.get("classes", {}))
        function_count += len(module.get("functions", {}))

        for cls in module.get("classes", {}).values():
            method_count += len(cls.get("methods", {}))

    return {
        "modules": module_count,
        "classes": class_count,
        "functions": function_count,
        "methods": method_count,
    }


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as fp:
        json.dump(data, fp, indent=2, ensure_ascii=False)


def generate_map(pkg_path: str, map_path: str):
    api = build_package_map(pkg_path)
    summary = generate_summary(api)
    api["summary"] = summary
    save_json(api, map_path)

