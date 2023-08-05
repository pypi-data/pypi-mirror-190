import typer
from typing import Optional


app = typer.Typer()


# python3 main.py hello justin
@app.command()
def hello(name: str):
    print(f"Hello {name}")


# python3 main.py goodbye justin --formal
@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")

# demo main --name justin --lastname bieber
#  python3 main.py main --name justin --lastname bieber
# poetry run python3 demo_01/main.py main --name justin --lastname bieber
# demo main --name justin --lastname bieber
# cl

@app.command()
def main(name: Optional[str] = typer.Option(...) , lastname: Optional[str] = typer.Option(...) ):
    print(f"Hello {name} {lastname}")

# poetry publish --repository-url http://192.168.114.40:8069 --username root --password rahasia2022 --directory dist/*

#  /etc/poetry/bin/poetry --version

# poetry config pypi-token.pypi pypi-AgEIcHlwaS5vcmcCJDg0YTc0ZTNjLWEyMzQtNDhlMi05MGUxLTY2MTQzZWJmZDZlZQACKlszLCJhMDVmZDE2Mi0xMjg2LTRiYWUtYTE3Zi1mMjZjMDk0NmYyZjkiXQAABiClYUvbTo2BAWNsINMvW_S6qmY3kP0Zklda0Oo3mW0hFQ
# poetry publish --build

if __name__ == "__main__":
    app()