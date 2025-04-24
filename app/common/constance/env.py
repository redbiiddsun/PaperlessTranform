from sqlmodel import Enum


class Environment(Enum):
    PRODUCTION = "prd"
    DEVELOPMENT = "dev"
