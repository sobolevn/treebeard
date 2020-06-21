def log(content: str, print_content: bool = True):
    """Manually log your custom content to a local file
    The file is saved at the end of the run and uploaded as an output
    then fetched by the notification function
    Logged content will be presented in the Treebeard admin page,
    and sent via Slack

    Params: content, custom string used in a command from a notebook
    """
    if print_content:
        print(content)
    with open("treebeard.log", "a+") as f:
        f.write("\n")
        f.write(content)
