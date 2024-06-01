import mistune


markdown = mistune.create_markdown(renderer=None)


def iterate_code_chunks(markdown_text):
    for node in markdown(markdown_text):
        if node["type"] == "block_code":
            yield dict(code=node["raw"].strip(), language=node["attrs"]["info"])
