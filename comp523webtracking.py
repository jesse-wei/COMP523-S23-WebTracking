import json
import pathlib
import subprocess

import toml
import requests

DATA_PATH = pathlib.Path("data")
POSTS_ENDPOINT = "{}/wp-json/wp/v2/posts"
PAGES_ENDPOINT = "{}/wp-json/wp/v2/pages"


def snapshot(config):
    for team, data in config["team-websites"]["team"].items():
        posts_url = POSTS_ENDPOINT.format(data["url"])
        pages_url = PAGES_ENDPOINT.format(data["url"])

        posts = requests.get(posts_url).json()
        pages = requests.get(pages_url).json()

        data["posts"] = posts
        data["pages"] = pages

    return config


def dump_teams(config):
    for team, data in config["team-websites"]["team"].items():
        with open(DATA_PATH / f"{team}_posts.json", "w") as f:
            json.dump(data["posts"], f, indent=4, ensure_ascii=False)
        with open(DATA_PATH / f"{team}_pages.json", "w") as f:
            json.dump(data["pages"], f, indent=4, ensure_ascii=False)


def separate_git_commits(config):
    for team in config["team-websites"]["team"]:
        try:
            subprocess.check_call(["git", "add", f"data/{team}*.json"])
            subprocess.check_call(["git", "commit", "-m", f"Update team {team} data"])
        except:
            pass


def main():
    config = toml.load("websites.toml")
    config = snapshot(config)

    dump_teams(config)
    separate_git_commits(config)


if __name__ == "__main__":
    main()
