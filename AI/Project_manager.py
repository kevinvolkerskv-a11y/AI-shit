from typing import List, Optional, Tuple
from Models import Project, ProjectStatus
from Validators import valideer_projectnaam, valideer_projectsluitng
from Storage import StorageManager


class ProjectManager:
    """Manager voor projectbeheer"""
    
    def __init__(self, storage: Optional[StorageManager] = None):
        self.storage = storage or StorageManager()
        self.projecten: List[Project] = []
        self._laad_projecten_van_schijf()
    
    def _laad_projecten_van_schijf(self):
        """Laad alle projecten van schijf in het geheugen"""
        self.projecten = self.storage.laad_alle_projecten()
    
    def maak_project_aan(self, naam: str, beschrijving: Optional[str] = None) -> Tuple[bool, str, Optional[Project]]:
        """
        Maak een nieuw project aan.
        
        Args:
            naam: De naam van het project
            beschrijving: Optionele beschrijving van het project
        
        Returns:
            Tuple van (succes, bericht, project)
        """
        is_geldig, foutbericht = valideer_projectnaam(naam, self.projecten)
        
        if not is_geldig:
            return False, foutbericht, None
        
        nieuw_project = Project(naam, beschrijving)
        self.projecten.append(nieuw_project)
        
        # Sla op schijf op
        if self.storage.sla_project_op(nieuw_project):
            return True, f"Project '{naam}' succesvol aangemaakt", nieuw_project
        else:
            # Verwijder uit geheugen als opslaan mislukt
            self.projecten.remove(nieuw_project)
            return False, f"Project '{naam}' kon niet opgeslagen worden", None
    
    def zoek_project(self, naam: str) -> Optional[Project]:
        """
        Zoek een project op naam.
        
        Args:
            naam: De naam van het project
        
        Returns:
            Het gevonden project of None
        """
        return next(
            (p for p in self.projecten if p.naam.lower() == naam.lower()),
            None
        )
    
    def haal_alle_projecten_op(self) -> List[Project]:
        """Haal alle projecten op"""
        return self.projecten.copy()
    
    def sluit_project(self, projectnaam: str) -> Tuple[bool, str]:
        """
        Sluit een project.
        
        Args:
            projectnaam: De naam van het project
        
        Returns:
            Tuple van (succes, bericht)
        """
        project = self.zoek_project(projectnaam)
        
        if not project:
            return False, f"Project '{projectnaam}' niet gevonden"
        
        is_geldig, bericht = valideer_projectsluitng(project)
        
        if not is_geldig:
            return False, bericht
        
        if project.sluit_project():
            # Sla op schijf op
            if self.storage.sla_project_op(project):
                return True, f"Project '{projectnaam}' succesvol gesloten"
            else:
                return False, "Project kon niet opgeslagen worden"
        
        return False, "Kon project niet sluiten"
    
    def verwijder_project(self, projectnaam: str) -> Tuple[bool, str]:
        """
        Verwijder een project.
        
        Args:
            projectnaam: De naam van het project
        
        Returns:
            Tuple van (succes, bericht)
        """
        project = self.zoek_project(projectnaam)
        
        if not project:
            return False, f"Project '{projectnaam}' niet gevonden"
        
        if not project.is_gesloten():
            return False, "Alleen gesloten projecten kunnen verwijderd worden"
        
        self.projecten.remove(project)
        
        # Verwijder van schijf
        if self.storage.verwijder_project(projectnaam):
            return True, f"Project '{projectnaam}' succesvol verwijderd"
        else:
            return False, "Project kon niet verwijderd worden"
    
    def toon_projectoverzicht(self) -> str:
        """
        Toon een overzicht van alle projecten.
        
        Returns:
            Een geformateerde string met het projectoverzicht
        """
        if not self.projecten:
            return "Geen projecten gevonden"
        
        overzicht = "=== PROJECTOVERZICHT ===\n"
        overzicht += f"{'Naam':<30} {'Status':<10} {'Aantal taken':<12}\n"
        overzicht += "-" * 52 + "\n"
        
        for project in self.projecten:
            status_text = project.status.value
            aantal_taken = project.aantal_taken()
            
            overzicht += f"{project.naam:<30} {status_text:<10} {aantal_taken:<12}\n"
        
        return overzicht
