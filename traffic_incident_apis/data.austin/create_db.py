from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
import warnings

USER = "root"
PASSWORD = "5Bvq6GoIhev1FnBG"
HOST = "127.0.0.1"
PORT = "3306"
DATABASE = "team_big_bend"

engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}")

try:
    engine.execute(f"CREATE DATABASE {DATABASE}")
except ProgrammingError:
    warnings.warn(
        f"Could not create database {DATABASE}. Database {DATABASE} may already exist."
    )
    pass