from datetime import datetime
from typing import Optional, List
from enum import Enum


class TaskPriority(Enum):
    """Prioriteit levels voor taken"""
    LAAG = "laag"
    NORMAAL = "normaal"
    HOOG = "hoog"


class TaskStatus(Enum):
    """Status mogelijkheden voor taken"""
    NIEUW = "nieuw"
    BEZIG = "bezig"
    AFGEROND = "afgerond"


class ProjectStatus(Enum):
    """Status mogelijkheden voor projecten"""
    ACTIEF = "actief"
    GESLOTEN = "gesloten"


class Task:
    """Representatie van een taak"""
    
    def __init__(self, titel: str, beschrijving: Optional[str] = None, 
                 prioriteit: TaskPriority = TaskPriority.NORMAAL):
        self.titel = titel
        self.beschrijving = beschrijving
        self.prioriteit = prioriteit
        self.status = TaskStatus.NIEUW
        self.aanmaakdatum = datetime.now()
        self.afrondmoment: Optional[datetime] = None
    
    def wijzig_status(self, nieuwe_status: TaskStatus) -> bool:
        """
        Wijzig de status van de taak volgens de toegestane overgangen.
        Teruggeeft True als wijziging succesvol is, False anders.
        """
        toegestane_overgangen = {
            TaskStatus.NIEUW: [TaskStatus.BEZIG],
            TaskStatus.BEZIG: [TaskStatus.AFGEROND],
            TaskStatus.AFGEROND: []
        }
        
        if nieuwe_status not in toegestane_overgangen[self.status]:
            return False
        
        self.status = nieuwe_status
        
        if nieuwe_status == TaskStatus.AFGEROND:
            self.afrondmoment = datetime.now()
        
        return True
    
    def is_afgerond(self) -> bool:
        """Controleer of de taak afgerond is"""
        return self.status == TaskStatus.AFGEROND
    
    def kan_aangepast_worden(self) -> bool:
        """Controleer of de taak nog kan worden aangepast"""
        return not self.is_afgerond()
    
    def __str__(self) -> str:
        return (f"[{self.status.value.upper()}] {self.titel} "
                f"(Prioriteit: {self.prioriteit.value})")


class Project:
    """Representatie van een project"""
    
    def __init__(self, naam: str, beschrijving: Optional[str] = None):
        self.naam = naam
        self.beschrijving = beschrijving
        self.status = ProjectStatus.ACTIEF
        self.aanmaakdatum = datetime.now()
        self.tasks: List[Task] = []
        self.sluitdatum: Optional[datetime] = None
    
    def voeg_taak_toe(self, taak: Task) -> bool:
        """
        Voeg een taak toe aan het project.
        Teruggeeft True als succesvol, False als project gesloten is.
        """
        if self.status == ProjectStatus.GESLOTEN:
            return False
        
        self.tasks.append(taak)
        return True
    
    def alle_taken_afgerond(self) -> bool:
        """Controleer of alle taken afgerond zijn"""
        if not self.tasks:
            return False
        return all(task.is_afgerond() for task in self.tasks)
    
    def sluit_project(self) -> bool:
        """
        Sluit het project.
        Teruggeert True als succesvol, False als niet alle taken afgerond zijn.
        """
        if not self.alle_taken_afgerond():
            return False
        
        self.status = ProjectStatus.GESLOTEN
        self.sluitdatum = datetime.now()
        return True
    
    def is_gesloten(self) -> bool:
        """Controleer of het project gesloten is"""
        return self.status == ProjectStatus.GESLOTEN
    
    def aantal_taken(self) -> int:
        """Geef het aantal taken in het project terug"""
        return len(self.tasks)
    
    def __str__(self) -> str:
        return f"{self.naam} (Status: {self.status.value})"
