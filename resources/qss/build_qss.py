import os
import jinja2

FILE_JINJA2 = "dark_orange.j2"
FILE_QSS = FILE_JINJA2.replace(".j2", ".qss")

if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__))))
    with open(FILE_QSS, "w") as f:
        template_loader = jinja2.FileSystemLoader(searchpath="./")
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(FILE_JINJA2)

        text = template.render(
            color_background="#727272",
            color_highlight="#FFAA00",
            color_viewport="#404040",
            color_text="lightgrey",
            color_highlight_text="black",
        )

        f.write(text)
        print(f"Stylesheet file '{ FILE_QSS }' generated")
