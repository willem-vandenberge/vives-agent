# Startpunt van de applicatie

from dotenv import load_dotenv
from src.workflow import Workflow

load_dotenv()

# app entry
def main():
    workflow = Workflow()
    print("Niewss samenvatter en fact-checker Agent")

    while True:
        query = input("\n🔍 Typ y om een nieuwsoverzicht te genereren: ").strip()
        if query.lower() in {"quit", "exit"}:
            break

        if query:
            result = workflow.run(query)
            print(f"\n📊 ----------- Nieuwsoverzicht:   ----------")




if __name__ == "__main__":
    main()