import sys
from app import models      # noqa: F401 - импорт ради регистрации моделей
from app.db import init_db

def main() -> None:
    print(f"Python {sys.version}")

init_db()
print("ok")

if __name__ == "__main__":
    main()