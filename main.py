import os
import yaml

def format(content, properties=None):
    rules = {
        "######": "h6",
        "#####": "h5",
        "####": "h4",
        "###": "h3",
        "##": "h2",
        "#": "h1",
        ">": "blockquote",
        "[": "a",
        "-": "li",
    }
    file = [f"<!--tags:     {','.join(properties.get('tags', []))} -->\n<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <link rel=\"stylesheet\" href=\"/Assets/styles.css\">"]
    if properties:
        title = properties.get("title", "Untitled")
        file.append(f"    <title>{title}</title>")
    file.append("</head>")

    if "---" in content:
        parts = content.split("---")
        if len(parts) > 2:
            content = "---".join(parts[2:])
    file.append(f"<body>\n    <header>\n        <h1>{properties.get("title", "Untitled")}</h1>\n    </header>\n    <main>\n        <article>")

    in_list = False
    for line in content.splitlines():
        matched = False
        for rule in rules:
            if line.startswith(rule):
                if rule == "-":
                    if not in_list:
                        file.append("            <ul>")
                        in_list = True
                    file.append(f"                <li>{line[len(rule):].strip()}</li>")
                    matched = True
                    break
                elif rule == "[":
                    file.append(f"            <{rules[rule]} href=\"{line[len(rule):].split(']')[1].strip().replace('(', '').replace(')', '')}\">{line[len(rule):].split(']')[0].strip()}</{rules[rule]}>")
                    matched = True
                    break
                if in_list:
                    file.append("            </ul>")
                    in_list = False
                file.append(f"            <{rules[rule]}>{line[len(rule):].strip()}</{rules[rule]}>")
                matched = True
                break
        if not matched and line.strip():
            if in_list:
                file.append("            </ul>")
                in_list = False
            file.append(f"            <p>{line.strip()}</p>")
    if in_list:
        file.append("            </ul>")
    
    file.append("        </article>\n    </main>\n    <footer>\n        <p>Made by Jwe0</p>\n    </footer>\n</body>")
    return file


def retrieve_properties(content):
    if "---" in content:
        parts = content.split("---")
        if len(parts) > 2:
            front = parts[1]
            try:
                return yaml.safe_load(front)
            except yaml.YAMLError:
                return None
    return None

def load_files():
    files = []
    base_path = f"/home/{os.getlogin()}/Documents/Obsidian Vault/Posts/"
    for file in os.listdir(base_path):
        if file.endswith(".md"):
            with open(os.path.join(base_path, file), "r") as f:
                files.append((file, f.read()))
    return files

def fix_index():
    with open("format.html", "r") as f:
        posts = ["<ul>"]
        for file in os.listdir("Pages"):
            if file.endswith(".html"):
                with open(f"Pages/{file}", "r") as j:
                    tags = j.read().split("\n")[0].split("tags:     ")[1].split(" -->")[0]
                    print(tags)
                posts.append(f"                <li><a href=\"Pages/{file}\">{file.split('.')[0]}</a> <p>{'| '.join(tags.split(', ')) if len(tags) >= 1 else tags[0] if tags else ''}</p></li>")
        posts.append("            </ul>")
        content = f.read().replace("LINKS", "\n".join(posts))
        with open("index.html", "w") as f:
            f.write(content)

files = load_files()
for file in files:
    properties = retrieve_properties(file[1])
    formatted = format(file[1], properties)
    output_name = os.path.splitext(file[0])[0] + ".html"
    with open("Pages/" + output_name, "w") as f:
        f.write("\n".join(formatted))
fix_index()