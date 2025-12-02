from database.db_manager import init_db
from gui.tk_gui import run_app


def main():
    init_db()
    run_app()


if __name__ == "__main__":
    main()
