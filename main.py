import os
import yaml

def retrieve_img(file):
    with open("/home/{}/Documents/Obsidian Vault/{}".format(os.getlogin(), file), "rb") as f:
        bytes = f.read()
    with open("Assets/Images/{}".format(file), "wb") as f:
        f.write(bytes)
    return f"/Assets/Images/{file}"

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
            elif "![[Pasted image " in line:
                filex = retrieve_img(line.split("![[")[1].split("]]")[0])
                img_tag = f"            <img src=\"{filex}\">"
                if img_tag not in file:
                    file.append(img_tag)
                matched = True
                break
        if not matched and line.strip():
            if in_list:
                file.append("            </ul>")
                in_list = False
            file.append(f"            <p>{line.strip()}</p>")
    if in_list:
        file.append("            </ul>")
    
    file.append("        </article>\n    </main>\n    <footer>\n        <a href=\"https://github.com/jwe0\">\n            <svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\"><path d=\"M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z\"/></svg>\n        </a>\n        <p>Made by Jwe0</p>\n    </footer>\n</body>")
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