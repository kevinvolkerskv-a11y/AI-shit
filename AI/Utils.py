import os
import sys


def wis_scherm():
    """Wis het scherm"""
    os.system('cls' if os.name == 'nt' else 'clear')


def toon_menu():
    """Toon het hoofdmenu"""
    print("=" * 50)
    print("     PROJECT & TASK MANAGEMENT SYSTEEM")
    print("=" * 50)
    print("\n=== PROJECTBEHEER ===")
    print("1. Nieuw project aanmaken")
    print("2. Projectoverzicht weergeven")
    print("3. Project sluiten")
    print("4. Project verwijderen")
    print("\n=== TAAKBEHEER ===")
    print("5. Taak aanmaken")
    print("6. Taakstatus wijzigen")
    print("7. Taken weergeven")
    print("8. Taakdetails weergeven")
    print("9. Taak verwijderen")
    print("\n0. Afsluiten")
    print("-" * 50)


def lees_invoer(prompt: str, verplicht: bool = False) -> str:
    """
    Lees invoer van de gebruiker.
    
    Args:
        prompt: De prompt die wordt getoond
        verplicht: Of de invoer verplicht is
    
    Returns:
        De ingevoerde tekst
    """
    while True:
        waarde = input(f"{prompt}: ").strip()
        
        if verplicht and not waarde:
            print(f"  > {prompt} is verplicht")
            continue
        
        return waarde


def lees_keuzecijfer(prompt: str, min_val: int, max_val: int) -> int:
    """
    Lees een keuzecijfer van de gebruiker.
    
    Args:
        prompt: De prompt die wordt getoond
        min_val: Minimale waarde
        max_val: Maximale waarde
    
    Returns:
        Het gekozen getal
    """
    while True:
        try:
            waarde = int(input(f"{prompt} ({min_val}-{max_val}): "))
            
            if min_val <= waarde <= max_val:
                return waarde
            
            print(f"  > Voer een getal in tussen {min_val} en {max_val}")
        except ValueError:
            print(f"  > Voer een geldig getal in")


def lees_ja_nee(prompt: str) -> bool:
    """
    Lees een ja/nee antwoord van de gebruiker.
    
    Args:
        prompt: De prompt die wordt getoond
    
    Returns:
        True voor ja, False voor nee
    """
    while True:
        antwoord = input(f"{prompt} (j/n): ").lower().strip()
        
        if antwoord in ['j', 'ja', 'y', 'yes']:
            return True
        elif antwoord in ['n', 'nee', 'no']:
            return False
        
        print("  > Voer 'j' voor ja of 'n' voor nee in")


def toon_bericht(bericht: str, soort: str = "info"):
    """
    Toon een bericht aan de gebruiker.
    
    Args:
        bericht: Het bericht dat getoond wordt
        soort: Het soort bericht (info, succes, fout, waarschuwing)
    """
    kleuren = {
        'info': '\033[94m',      # Blauw
        'succes': '\033[92m',    # Groen
        'fout': '\033[91m',      # Rood
        'waarschuwing': '\033[93m'  # Geel
    }
    einde = '\033[0m'  # Reset
    
    kleur = kleuren.get(soort, '')
    print(f"{kleur}{bericht}{einde}")


def wacht_op_enter():
    """Wacht tot de gebruiker op Enter drukt"""
    input("\nDruk op Enter om door te gaan...")
