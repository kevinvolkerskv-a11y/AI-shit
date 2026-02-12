#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Project_manager import ProjectManager
from Task_manager import TaskManager
from Storage import StorageManager
from Utils import (toon_menu, lees_invoer, lees_keuzecijfer, lees_ja_nee,
                  toon_bericht, wacht_op_enter, wis_scherm)


class TaskManagementApp:
    """Hoofd applicatie voor project & task management"""
    
    def __init__(self):
        self.storage_manager = StorageManager()
        self.project_manager = ProjectManager(self.storage_manager)
        self.task_manager = TaskManager(self.storage_manager)
    
    def menu_project_aanmaken(self):
        """Menu: Nieuw project aanmaken"""
        print("\n=== NIEUW PROJECT AANMAKEN ===")
        
        naam = lees_invoer("Projectnaam")
        if not naam:
            toon_bericht("Projectnaam is verplicht", "fout")
            return
        
        beschrijving = lees_invoer("Projectbeschrijving (optioneel)")
        
        succes, bericht, project = self.project_manager.maak_project_aan(naam, beschrijving)
        
        if succes:
            toon_bericht(bericht, "succes")
        else:
            toon_bericht(bericht, "fout")
        
        wacht_op_enter()
    
    def menu_projectoverzicht(self):
        """Menu: Projectoverzicht weergeven"""
        print(self.project_manager.toon_projectoverzicht())
        wacht_op_enter()
    
    def menu_project_sluiten(self):
        """Menu: Project sluiten"""
        print("\n=== PROJECT SLUITEN ===")
        
        projectnaam = lees_invoer("Projectnaam")
        
        project = self.project_manager.zoek_project(projectnaam)
        if not project:
            toon_bericht(f"Project '{projectnaam}' niet gevonden", "fout")
            wacht_op_enter()
            return
        
        print(self.task_manager.toon_takenlijst(project))
        
        if not lees_ja_nee("Weet u zeker dat u dit project wilt sluiten?"):
            toon_bericht("Annuleren", "info")
            wacht_op_enter()
            return
        
        succes, bericht = self.project_manager.sluit_project(projectnaam)
        
        if succes:
            toon_bericht(bericht, "succes")
        else:
            toon_bericht(bericht, "fout")
        
        wacht_op_enter()
    
    def menu_project_verwijderen(self):
        """Menu: Project verwijderen"""
        print("\n=== PROJECT VERWIJDEREN ===")
        
        projectnaam = lees_invoer("Projectnaam")
        
        if not lees_ja_nee(f"Weet u zeker dat u project '{projectnaam}' wilt verwijderen?"):
            toon_bericht("Annuleren", "info")
            wacht_op_enter()
            return
        
        succes, bericht = self.project_manager.verwijder_project(projectnaam)
        
        if succes:
            toon_bericht(bericht, "succes")
        else:
            toon_bericht(bericht, "fout")
        
        wacht_op_enter()
    
    def menu_taak_aanmaken(self):
        """Menu: Taak aanmaken"""
        print("\n=== TAAK AANMAKEN ===")
        
        projectnaam = lees_invoer("Projectnaam")
        project = self.project_manager.zoek_project(projectnaam)
        
        if not project:
            toon_bericht(f"Project '{projectnaam}' niet gevonden", "fout")
            wacht_op_enter()
            return
        
        titel = lees_invoer("Taaktitel")
        if not titel:
            toon_bericht("Taaktitel is verplicht", "fout")
            wacht_op_enter()
            return
        
        beschrijving = lees_invoer("Taakbeschrijving (optioneel)")
        
        print("\nPrioriteitniveaus: laag, normaal, hoog")
        prioriteit = lees_invoer("Prioriteit (standaard: normaal)")
        if not prioriteit:
            prioriteit = "normaal"
        
        succes, bericht, taak = self.task_manager.maak_taak_aan(
            project, titel, beschrijving, prioriteit
        )
        
        if succes:
            toon_bericht(bericht, "succes")
        else:
            toon_bericht(bericht, "fout")
        
        wacht_op_enter()
    
    def menu_taak_status_wijzigen(self):
        """Menu: Taakstatus wijzigen"""
        print("\n=== TAAK STATUS WIJZIGEN ===")
        
        projectnaam = lees_invoer("Projectnaam")
        project = self.project_manager.zoek_project(projectnaam)
        
        if not project:
            toon_bericht(f"Project '{projectnaam}' niet gevonden", "fout")
            wacht_op_enter()
            return
        
        print(self.task_manager.toon_takenlijst(project))
        
        taaktitel = lees_invoer("Taaktitel")
        
        print("\nGeldige statussen:")
        print("- nieuw")
        print("- bezig")
        print("- afgerond")
        
        nieuwe_status = lees_invoer("Nieuwe status")
        
        succes, bericht = self.task_manager.wijzig_taakstatus(project, taaktitel, nieuwe_status)
        
        if succes:
            toon_bericht(bericht, "succes")
        else:
            toon_bericht(bericht, "fout")
        
        wacht_op_enter()
    
    def menu_taken_weergeven(self):
        """Menu: Taken weergeven"""
        print("\n=== TAKEN WEERGEVEN ===")
        
        projectnaam = lees_invoer("Projectnaam")
        project = self.project_manager.zoek_project(projectnaam)
        
        if not project:
            toon_bericht(f"Project '{projectnaam}' niet gevonden", "fout")
            wacht_op_enter()
            return
        
        print(self.task_manager.toon_takenlijst(project))
        wacht_op_enter()
    
    def menu_taakdetails_weergeven(self):
        """Menu: Taakdetails weergeven"""
        print("\n=== TAAKDETAILS WEERGEVEN ===")
        
        projectnaam = lees_invoer("Projectnaam")
        project = self.project_manager.zoek_project(projectnaam)
        
        if not project:
            toon_bericht(f"Project '{projectnaam}' niet gevonden", "fout")
            wacht_op_enter()
            return
        
        taaktitel = lees_invoer("Taaktitel")
        
        print(self.task_manager.toon_taakdetails(project, taaktitel))
        wacht_op_enter()
    
    def menu_taak_verwijderen(self):
        """Menu: Taak verwijderen"""
        print("\n=== TAAK VERWIJDEREN ===")
        
        projectnaam = lees_invoer("Projectnaam")
        project = self.project_manager.zoek_project(projectnaam)
        
        if not project:
            toon_bericht(f"Project '{projectnaam}' niet gevonden", "fout")
            wacht_op_enter()
            return
        
        print(self.task_manager.toon_takenlijst(project))
        
        taaktitel = lees_invoer("Taaktitel")
        
        if not lees_ja_nee(f"Weet u zeker dat u taak '{taaktitel}' wilt verwijderen?"):
            toon_bericht("Annuleren", "info")
            wacht_op_enter()
            return
        
        succes, bericht = self.task_manager.verwijder_taak(project, taaktitel)
        
        if succes:
            toon_bericht(bericht, "succes")
        else:
            toon_bericht(bericht, "fout")
        
        wacht_op_enter()
    
    def run(self):
        """Hoofd applicatielus"""
        while True:
            wis_scherm()
            toon_menu()
            
            keuze = lees_keuzecijfer("Maak een keuze", 0, 9)
            
            if keuze == 0:
                toon_bericht("Tot ziens!", "succes")
                break
            elif keuze == 1:
                self.menu_project_aanmaken()
            elif keuze == 2:
                self.menu_projectoverzicht()
            elif keuze == 3:
                self.menu_project_sluiten()
            elif keuze == 4:
                self.menu_project_verwijderen()
            elif keuze == 5:
                self.menu_taak_aanmaken()
            elif keuze == 6:
                self.menu_taak_status_wijzigen()
            elif keuze == 7:
                self.menu_taken_weergeven()
            elif keuze == 8:
                self.menu_taakdetails_weergeven()
            elif keuze == 9:
                self.menu_taak_verwijderen()


def main():
    """Main entry point"""
    app = TaskManagementApp()
    app.run()


if __name__ == "__main__":
    main()
