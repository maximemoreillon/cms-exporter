from db import driver
from os import path

output_folder = "./output"

with driver.session() as session:
    result = session.run("MATCH (a:Article) RETURN PROPERTIES(a) as article LIMIT 2")
    for record in result:
        article = record["article"]

        file_name = f"{article["title"]}.html"
        file_path = path.join(output_folder, file_name)
        file_content = article["content"]

        with open(file_path, "w") as file_object:
            file_object.write(file_content)
