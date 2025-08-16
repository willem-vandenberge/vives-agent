

from dotenv import load_dotenv
from src.workflow import Workflow

load_dotenv()

# app entry
def main():
    workflow = Workflow()
    print("Niewss samenvatter en fact-checker Agent")

    while True:
        query = input("\n🔍 Typ start om een nieuwsoverzicht te genereren: ").strip()
        if query.lower() in {"quit", "exit"}:
            break

        if query:
            print(f" ----------- Nieuwsoverzicht:   ----------")
            result = workflow.run()





if __name__ == "__main__":
    main()