from typing import List, Optional
from Models import Project, Task, TaskPriority


def valideer_projectnaam(naam: str, bestaande_projecten: List[Project]) -> tuple[bool, str]:
    """
    Valideer de projectnaam.
    
    Args:
        naam: De projectnaam die gevalideerd moet worden
        bestaande_projecten: Lijst van bestaande projecten
    
    Returns:
        Tuple van (is_geldig, foutbericht)
    """
    if not naam or not naam.strip():
        return False, "Projectnaam mag niet leeg zijn"
    
    # Controleer uniciteit
    bestaande_namen = [p.naam.lower() for p in bestaande_projecten]
    if naam.lower() in bestaande_namen:
        return False, f"Een project met de naam '{naam}' bestaat al"
    
    return True, ""


def valideer_taaktitel(titel: str, bestaande_taken: List[Task]) -> tuple[bool, str]:
    """
    Valideer de taaktitel.
    
    Args:
        titel: De taaktitel die gevalideerd moet worden
        bestaande_taken: Lijst van bestaande taken in het project
    
    Returns:
        Tuple van (is_geldig, foutbericht)
    """
    if not titel or not titel.strip():
        return False, "Taaktitel mag niet leeg zijn"
    
    # Controleer uniciteit binnen project
    bestaande_titels = [t.titel.lower() for t in bestaande_taken]
    if titel.lower() in bestaande_titels:
        return False, f"Een taak met titel '{titel}' bestaat al in dit project"
    
    return True, ""


def valideer_prioriteit(prioriteit: str) -> tuple[bool, str]:
    """
    Valideer de taakprioriteit.
    
    Args:
        prioriteit: De prioriteit als string (laag, normaal, hoog)
    
    Returns:
        Tuple van (is_geldig, prioriteit_enum of foutbericht)
    """
    geldige_prioriteiten = {
        'laag': TaskPriority.LAAG,
        'normaal': TaskPriority.NORMAAL,
        'hoog': TaskPriority.HOOG
    }
    
    prioriteit_lower = prioriteit.lower() if prioriteit else ""
    
    if prioriteit_lower not in geldige_prioriteiten:
        return False, "Prioriteit moet 'laag', 'normaal' of 'hoog' zijn"
    
    return True, geldige_prioriteiten[prioriteit_lower]


def valideer_projectsluitng(project: Project) -> tuple[bool, str]:
    """
    Valideer of een project gesloten kan worden.
    
    Args:
        project: Het project dat gesloten moet worden
    
    Returns:
        Tuple van (kan_gesloten_worden, bericht)
    """
    if project.is_gesloten():
        return False, "Het project is al gesloten"
    
    if not project.alle_taken_afgerond():
        return False, "Het project kan alleen gesloten worden als alle taken afgerond zijn"
    
    if not project.tasks:
        return False, "Kan een project zonder taken niet sluiten"
    
    return True, ""
