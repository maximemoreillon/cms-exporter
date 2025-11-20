from db import driver
from os import path
from markdownify import markdownify as md

output_folder = "./output"
limit = 3


def save_html(article):
    file_name = f"{article["_id"]}.html"
    file_path = path.join(output_folder, "html", file_name)
    file_content = article["content"]

    with open(file_path, "w") as file_object:
        file_object.write(file_content)


def save_md(article):

    # file_name = f"{article["title"]}.md"
    file_name = f"{article["_id"]}.md"
    file_path = path.join(output_folder, "md", file_name)
    # file_content = md(article["content"], strip=["h1"])
    file_content = md(article["content"])

    with open(file_path, "w") as file_object:
        file_object.write("+++\n")
        file_object.write(f"date = '2025-11-20T10:44:51+09:00'\n")
        file_object.write(f"draft = true\n")
        file_object.write(f"title = '{article["title"]}'\n")
        file_object.write("+++\n")
        file_object.write("\n")
        file_object.write(file_content)


with driver.session() as session:
    cypher = f"MATCH (a:Article) RETURN PROPERTIES(a) as article LIMIT {limit}"
    result = session.run(cypher)
    for record in result:
        article = record["article"]
        save_html(article)
        save_md(article)
