import yaml


def load(args, data):
    """
    Load an answers file
    Of note, answers could actually be stuff in the questions file
    """
    file = args.get("input_file")
    if not file:
        return data

    with open(file, encoding="UTF-8") as fd:
        answers = yaml.safe_load(fd)

    data["answers"] = answers.get("answers")
    return data
