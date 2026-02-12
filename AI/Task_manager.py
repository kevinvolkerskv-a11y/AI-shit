from typing import List, Optional, Tuple
from Models import Project, Task, TaskStatus, TaskPriority
from Validators import valideer_taaktitel, valideer_prioriteit


class TaskManager:
    """Manager voor taakbeheer"""
    
    def __init__(self, storage=None):
        self.storage = storage
    
    def maak_taak_aan(self, project: Project, titel: str, beschrijving: Optional[str] = None,
                     prioriteit_str: str = "normaal") -> Tuple[bool, str, Optional[Task]]:
        """
        Maak een nieuwe taak aan in een project.
        
        Args:
            project: Het project waarin de taak wordt aangemaakt
            titel: De titel van de taak
            beschrijving: Optionele beschrijving van de taak
            prioriteit_str: De prioriteit als string
        
        Returns:
            Tuple van (succes, bericht, taak)
        """
        if project.is_gesloten():
            return False, "Kan geen taken toevoegen aan een gesloten project", None
        
        # Valideer titel
        is_geldig, foutbericht = valideer_taaktitel(titel, project.tasks)
        if not is_geldig:
            return False, foutbericht, None
        
        # Valideer prioriteit
        is_geldig, prioriteit = valideer_prioriteit(prioriteit_str)
        if not is_geldig:
            return False, prioriteit, None
        
        # Maak de taak aan
        nieuwe_taak = Task(titel, beschrijving, prioriteit)
        
        # Voeg toe aan project
        if project.voeg_taak_toe(nieuwe_taak):
            # Sla op schijf op
            if self.storage and self.storage.sla_project_op(project):
                return True, f"Taak '{titel}' succesvol aangemaakt", nieuwe_taak
            elif not self.storage:
                return True, f"Taak '{titel}' succesvol aangemaakt", nieuwe_taak
            else:
                # Verwijder uit project als opslaan mislukt
                project.tasks.remove(nieuwe_taak)
                return False, f"Taak kon niet opgeslagen worden", None
        
        return False, "Kon taak niet toevoegen", None
    
    def zoek_taak(self, project: Project, titel: str) -> Optional[Task]:
        """
        Zoek een taak in een project op titel.
        
        Args:
            project: Het project waarin gezocht wordt
            titel: De titel van de taak
        
        Returns:
            De gevonden taak of None
        """
        return next(
            (t for t in project.tasks if t.titel.lower() == titel.lower()),
            None
        )
    
    def wijzig_taakstatus(self, project: Project, taaktitel: str, 
                         nieuwe_status_str: str) -> Tuple[bool, str]:
        """
        Wijzig de status van een taak.
        
        Args:
            project: Het project van de taak
            taaktitel: De titel van de taak
            nieuwe_status_str: De nieuwe status als string
        
        Returns:
            Tuple van (succes, bericht)
        """
        taak = self.zoek_taak(project, taaktitel)
        
        if not taak:
            return False, f"Taak '{taaktitel}' niet gevonden"
        
        # Controleer of taak mag worden aangepast
        if not taak.kan_aangepast_worden():
            return False, "Afgeronde taken kunnen niet meer worden aangepast"
        
        # Parse de nieuwe status
        status_mapping = {
            'nieuw': TaskStatus.NIEUW,
            'bezig': TaskStatus.BEZIG,
            'afgerond': TaskStatus.AFGEROND
        }
        
        nieuwe_status_str_lower = nieuwe_status_str.lower()
        
        if nieuwe_status_str_lower not in status_mapping:
            return False, "Ongeldige status. Geldige statussen zijn: nieuw, bezig, afgerond"
        
        nieuwe_status = status_mapping[nieuwe_status_str_lower]
        
        # Wijzig de status
        if taak.wijzig_status(nieuwe_status):
            bericht = f"Status van taak '{taaktitel}' gewijzigd naar {nieuwe_status.value}"
            if taak.is_afgerond():
                bericht += f" (Afgerond op: {taak.afrondmoment.strftime('%Y-%m-%d %H:%M:%S')})"
            
            # Sla op schijf op
            if self.storage:
                self.storage.sla_project_op(project)
            
            return True, bericht
        else:
            return False, f"Status kan niet gewijzigd worden van {taak.status.value} naar {nieuwe_status_str}"
    
    def verwijder_taak(self, project: Project, taaktitel: str) -> Tuple[bool, str]:
        """
        Verwijder een taak uit een project.
        
        Args:
            project: Het project van de taak
            taaktitel: De titel van de taak
        
        Returns:
            Tuple van (succes, bericht)
        """
        taak = self.zoek_taak(project, taaktitel)
        
        if not taak:
            return False, f"Taak '{taaktitel}' niet gevonden"
        
        if not taak.is_afgerond():
            return False, "Alleen afgeronde taken kunnen verwijderd worden"
        
        project.tasks.remove(taak)
        
        # Sla op schijf op
        if self.storage:
            self.storage.sla_project_op(project)
        
        return True, f"Taak '{taaktitel}' succesvol verwijderd"
    
    def toon_takenlijst(self, project: Project) -> str:
        """
        Toon een overzicht van alle taken in een project.
        
        Args:
            project: Het project
        
        Returns:
            Een geformateerde string met de takenlijst
        """
        if not project.tasks:
            return f"\n=== TAKEN IN PROJECT '{project.naam}' ===\nGeen taken gevonden"
        
        overzicht = f"\n=== TAKEN IN PROJECT '{project.naam}' ===\n"
        overzicht += f"{'Titel':<30} {'Status':<10} {'Prioriteit':<10}\n"
        overzicht += "-" * 50 + "\n"
        
        for taak in project.tasks:
            status_text = taak.status.value
            prioriteit_text = taak.prioriteit.value
            
            overzicht += f"{taak.titel:<30} {status_text:<10} {prioriteit_text:<10}\n"
        
        return overzicht
    
    def toon_taakdetails(self, project: Project, taaktitel: str) -> str:
        """
        Toon gedetailleerde informatie over een taak.
        
        Args:
            project: Het project van de taak
            taaktitel: De titel van de taak
        
        Returns:
            Een geformateerde string met taakdetails
        """
        taak = self.zoek_taak(project, taaktitel)
        
        if not taak:
            return f"Taak '{taaktitel}' niet gevonden"
        
        details = "\n=== TAAKDETAILS ===\n"
        details += f"Titel: {taak.titel}\n"
        details += f"Beschrijving: {taak.beschrijving or 'Geen beschrijving'}\n"
        details += f"Prioriteit: {taak.prioriteit.value}\n"
        details += f"Status: {taak.status.value}\n"
        details += f"Aangemaakt: {taak.aanmaakdatum.strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        if taak.afrondmoment:
            details += f"Afgerond: {taak.afrondmoment.strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        return details
