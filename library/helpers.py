import os.path

import markdown


def openfile(filename):
    filepath = os.path.join("shortener_app/pages/", filename)
    with open(filepath, "r", encoding="utf-8") as input_file:
        text = input_file.read()
    html = markdown.markdown(text)
    return {"text": html}

if __name__ == "__main__":
    print(openfile("about.md"))