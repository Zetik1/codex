import sys
from app import models      # noqa: F401 - импорт ради регистрации моделей
from app.db import init_db

def main() -> None:
    print(f"Python {sys.version}")

if __name__ == "__main__":
    init_db()
    main()
    print("ok")