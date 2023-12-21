import re


def clean_corpus(chat_export_file):
    cleaned_corpus = remove_chat_metadata(chat_export_file)
    return cleaned_corpus


def remove_chat_metadata(chat_export_file):
    username = r"([\w\s]+)"  # e.g. "Jane Doe"
    metadata_end = r":\s"  # ": "
    pattern = username + metadata_end

    with open(chat_export_file, "r") as corpus_file:
        content = corpus_file.read()
    cleaned_corpus = re.sub(pattern, "", content)
    return tuple(cleaned_corpus.split("\n"))
