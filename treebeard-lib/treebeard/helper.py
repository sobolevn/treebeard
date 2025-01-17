import configparser
import datetime
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

import click
import requests
from pydantic import BaseModel
from sentry_sdk import capture_exception, capture_message  # type: ignore

from treebeard.conf import (
    api_url,
    config_path,
    treebeard_config,
    treebeard_env,
)
from treebeard.version import get_version

version = get_version()


def set_credentials(email: str, key: str, user_name: str):
    """Create user credentials"""
    config = configparser.RawConfigParser()
    config.add_section("credentials")
    config.set("credentials", "email", email)
    config.set("credentials", "user_name", user_name)
    config.set("credentials", "api_key", key)
    with open(config_path, "w") as configfile:
        config.write(configfile)
    click.echo(f"🔑  Config saved in {config_path}")
    return user_name


def check_for_updates():
    pypi_data = requests.get("https://pypi.org/pypi/treebeard/json")  # type: ignore
    latest_version = json.loads(pypi_data.text)["info"]["version"]

    if latest_version != version:
        click.echo(
            click.style(
                "🌲 Warning: you are not on the latest version of Treebeard, update with `pip install --upgrade treebeard`",
                fg="yellow",
            ),
            err=True,
        )


def get_service_status_message(service_status_url: str) -> Optional[str]:
    try:
        data = json.loads(requests.get(service_status_url).text)  # type: ignore
        if "message" in data:
            return data["message"]
    except:  # Non-200 status/timeout, etc.
        return None


class CliContext(BaseModel):
    debug: bool


def sanitise_repo_short_name(repo_short_name: str) -> str:
    out = repo_short_name
    out = out.replace(" ", "-")
    out = out.replace(".", "-")
    return out.lower()


def create_example_yaml():
    dirname = os.path.split(os.path.abspath(__file__))[0]
    with open(Path(f"{dirname}/example_treebeard.yaml"), "rb") as f:
        open("treebeard.yaml", "wb").write(f.read())
    return


def get_time():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def update(status: Optional[str] = None):
    data = {}
    if status:
        data["status"] = status

    # Available at repotime
    workflow = os.getenv("GITHUB_WORKFLOW")

    if workflow:
        data["workflow"] = (
            workflow.replace(".yml", "").replace(".yaml", "").split("/")[-1]
        )

    event_name = os.getenv("GITHUB_EVENT_NAME")
    event_path = os.getenv("GITHUB_EVENT_PATH")

    if event_name:
        data["event_name"] = event_name
        if event_name == "push" and event_path:
            with open(event_path, "r") as event:
                event_json = json.load(event)
                data["sender"] = event_json["sender"]
                data["head_commit"] = event_json["head_commit"]

    # Envs below should be available at repo/build/runtime
    sha = os.getenv("GITHUB_SHA")
    ref = os.getenv("GITHUB_REF")

    if sha and ref:
        branch = ref.split("/")[-1]
        data["sha"] = sha
        data["branch"] = branch

    data["start_time"] = os.getenv("TREEBEARD_START_TIME") or get_time()
    if status in ["SUCCESS", "FAILURE"]:
        data["end_time"] = get_time()

    update_url = f"{api_url}/{treebeard_env.user_name}/{treebeard_env.repo_short_name}/{treebeard_env.run_id}/update"
    resp = requests.post(  # type:ignore
        update_url, json=data, headers={"api_key": treebeard_env.api_key},
    )

    if treebeard_config.debug:
        print(f"Updating backend with data\n{data}")

    if resp.status_code != 200:
        capture_message(f"Failed to update tb {resp.status_code}\n{update_url}\n{data}")


def shell(command: str):
    with subprocess.Popen(
        ["bash", "-c", command],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,
        universal_newlines=True,
    ) as p:
        if p.stdout:
            for line in p.stdout:
                print(line, end="")  # process line here

        if p.stderr:
            for line in p.stderr:
                print(line, end="", file=sys.stderr)  # process line here

    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, p.args)
