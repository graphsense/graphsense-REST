from pathlib import Path

from sqlmodel import text
from tagpack.cli import exec_cli_command
from tagstore.db.database import get_db_engine, init_database, with_session

DATA_DIR_TP = Path(__file__).parent.resolve() / "data" / "packs"
DATA_DIR_A = Path(__file__).parent.resolve() / "data" / "actors"
DATA_SQL = Path(__file__).parent.resolve() / "data" / "data.sql"


def load_test_data(db_url: str):
    engine = get_db_engine(db_url)

    init_database(engine)

    exec_cli_command(
        ["actorpack", "insert", str(DATA_DIR_A), "-u", db_url, "--no_strict_check"]
    )

    tps = [
        (True, "tagpack_public.yaml"),
        (False, "tagpack_private.yaml"),
        (False, "tagpack_uriX.yaml"),
        (True, "tagpack_uriY.yaml"),
    ]
    for public, tpf in tps:
        exec_cli_command(
            [
                "tagpack",
                "insert",
                str(DATA_DIR_TP / tpf),
                "-u",
                db_url,
                "--no_strict_check",
                "--no_git",
            ]
            + (["--public"] if public else [])
        )

    with with_session(engine) as session:
        with open(DATA_SQL) as f:
            session.execute(text(f.read()))
            session.commit()

    exec_cli_command(["tagstore", "refresh_views", "-u", db_url])
