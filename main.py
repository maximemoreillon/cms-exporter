from db import driver
from os import path
from markdownify import markdownify as md

#
# output_folder = "./output"
output_folder = "/home/moreillon/dev/hugo/articles/content/articles"


def process_content(content):
    # Remove h1 (striped by md)
    content = "\n".join(content.splitlines()[2:])

    # Fix images query
    content = content.replace(
        "https://img.maximemoreillon.com/image?id=",
        "https://img.maximemoreillon.com/images/",
    )
    return content


with driver.session() as session:
    cypher = """
        MATCH (article:Article {published: true})
        WITH article
        OPTIONAL MATCH (tag:Tag)-[:APPLIED_TO]->(article)
        WITH article, COLLECT(properties(tag)) AS tags
        MATCH (article)-[authorship:WRITTEN_BY]->(author:User)

        WITH COUNT(DISTINCT(article)) AS article_count,
          COLLECT({
            article: properties(article),
            author: properties(author),
            authorship: properties(authorship),
            tags: tags
          }) AS articles

        RETURN articles
        """
    records = session.run(cypher)

    for record in records:
        items = record["articles"]
        for item in items:

            article = item["article"]

            file_name = f"{article["_id"]}.md"
            file_path = path.join(output_folder, file_name)

            content = md(article["content"], strip=["h1"])

            content = process_content(content)

            tags = []
            for tag in item["tags"]:
                tags.append(tag["name"])

            with open(file_path, "w") as file_object:
                file_object.write("+++\n")
                file_object.write(f'title = "{article["title"]}"\n')
                file_object.write(f"date = '{item["authorship"]["creation_date"]}'\n")
                file_object.write(f"lastmod = '{item["authorship"]["edition_date"]}'\n")
                file_object.write(f"tags = {tags}\n")
                # if "summary" in article:
                #     file_object.write(f'summary = "{article["summary"]}"\n')
                # file_object.write(f"draft = true\n")
                file_object.write("+++\n")
                file_object.write("\n")

                file_object.write(content)

            print(article["title"])
