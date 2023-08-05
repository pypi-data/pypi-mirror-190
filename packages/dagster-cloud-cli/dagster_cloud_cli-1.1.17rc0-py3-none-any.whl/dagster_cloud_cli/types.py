from enum import Enum


class ServerlessEventSource(Enum):
    GITHUB = "github"
    GITLAB = "gitlab"
    CLI = "cli"
    UNKNOWN = "unknown"


class ServerlessEventState(Enum):
    START = "start"
    SUCCESS = "success"
    FAILURE = "failure"


class ServerlessEventType(Enum):
    DEPLOY = "deploy"


class ServerlessEventStrategy(Enum):
    DOCKER = "docker"
    PEX = "pex"
