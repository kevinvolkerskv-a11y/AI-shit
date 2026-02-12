import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
from Models import Project, Task, TaskStatus, ProjectStatus, TaskPriority


class StorageManager:
    """Manager voor persistentie van projecten en taken op schijf"""
    
    def __init__(self, base_path: str = "projects"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
    
    def _project_folder(self, project_naam: str) -> Path:
        """Geef het mappad voor een project"""
        return self.base_path / self._saniteer_mapnaam(project_naam)
    
    def _saniteer_mapnaam(self, naam: str) -> str:
        """Zet projectnaam om naar een geldige mapnaam"""
        # Vervang ongeldige karakters
        invalid_chars = r'<>:"/\|?*'
        for char in invalid_chars:
            naam = naam.replace(char, '_')
        return naam.strip()
    
    def sla_project_op(self, project: Project) -> bool:
        """
        Sla een project op in de bestandssysteem.
        
        Args:
            project: Het project dat opgeslagen moet worden
        
        Returns:
            True als succesvol, False anders
        """
        try:
            project_folder = self._project_folder(project.naam)
            project_folder.mkdir(parents=True, exist_ok=True)
            
            # Sla projectgegevens op
            project_data = {
                'naam': project.naam,
                'beschrijving': project.beschrijving,
                'status': project.status.value,
                'aanmaakdatum': project.aanmaakdatum.isoformat(),
                'sluitdatum': project.sluitdatum.isoformat() if project.sluitdatum else None
            }
            
            with open(project_folder / 'project.json', 'w', encoding='utf-8') as f:
                json.dump(project_data, f, ensure_ascii=False, indent=2)
            
            # Sla taken op
            taken_data = []
            for taak in project.tasks:
                taken_data.append({
                    'titel': taak.titel,
                    'beschrijving': taak.beschrijving,
                    'prioriteit': taak.prioriteit.value,
                    'status': taak.status.value,
                    'aanmaakdatum': taak.aanmaakdatum.isoformat(),
                    'afrondmoment': taak.afrondmoment.isoformat() if taak.afrondmoment else None
                })
            
            with open(project_folder / 'tasks.json', 'w', encoding='utf-8') as f:
                json.dump(taken_data, f, ensure_ascii=False, indent=2)
            
            return True
        
        except Exception as e:
            print(f"Fout bij opslaan project: {e}")
            return False
    
    def laad_project(self, project_naam: str) -> Optional[Project]:
        """
        Laad een project van schijf.
        
        Args:
            project_naam: De naam van het project
        
        Returns:
            Het geladen Project object of None
        """
        try:
            project_folder = self._project_folder(project_naam)
            
            if not project_folder.exists():
                return None
            
            # Laad projectgegevens
            project_file = project_folder / 'project.json'
            if not project_file.exists():
                return None
            
            with open(project_file, 'r', encoding='utf-8') as f:
                project_data = json.load(f)
            
            # Recreïer project
            project = Project(
                project_data['naam'],
                project_data.get('beschrijving')
            )
            
            project.status = ProjectStatus(project_data['status'])
            project.aanmaakdatum = datetime.fromisoformat(project_data['aanmaakdatum'])
            
            if project_data.get('sluitdatum'):
                project.sluitdatum = datetime.fromisoformat(project_data['sluitdatum'])
            
            # Laad taken
            tasks_file = project_folder / 'tasks.json'
            if tasks_file.exists():
                with open(tasks_file, 'r', encoding='utf-8') as f:
                    taken_data = json.load(f)
                
                for taak_data in taken_data:
                    taak = Task(
                        taak_data['titel'],
                        taak_data.get('beschrijving'),
                        TaskPriority(taak_data['prioriteit'])
                    )
                    
                    taak.status = TaskStatus(taak_data['status'])
                    taak.aanmaakdatum = datetime.fromisoformat(taak_data['aanmaakdatum'])
                    
                    if taak_data.get('afrondmoment'):
                        taak.afrondmoment = datetime.fromisoformat(taak_data['afrondmoment'])
                    
                    project.tasks.append(taak)
            
            return project
        
        except Exception as e:
            print(f"Fout bij laden project: {e}")
            return None
    
    def laad_alle_projecten(self) -> List[Project]:
        """
        Laad alle projecten van schijf.
        
        Returns:
            Lijst van alle geladen projecten
        """
        projecten = []
        
        if not self.base_path.exists():
            return projecten
        
        # Itereer door alle mappen in projects/
        for project_folder in self.base_path.iterdir():
            if project_folder.is_dir():
                project_file = project_folder / 'project.json'
                if project_file.exists():
                    projeto = self.laad_project(project_folder.name)
                    if projeto:
                        projecten.append(projeto)
        
        return projecten
    
    def verwijder_project(self, project_naam: str) -> bool:
        """
        Verwijder een project inclusief alle bestanden.
        
        Args:
            project_naam: De naam van het project
        
        Returns:
            True als succesvol, False anders
        """
        try:
            project_folder = self._project_folder(project_naam)
            
            if project_folder.exists():
                import shutil
                shutil.rmtree(project_folder)
                return True
            
            return False
        
        except Exception as e:
            print(f"Fout bij verwijderen project: {e}")
            return False
    
    def project_bestaat(self, project_naam: str) -> bool:
        """
        Controleer of een project op schijf bestaat.
        
        Args:
            project_naam: De naam van het project
        
        Returns:
            True als het project bestaat, False anders
        """
        project_folder = self._project_folder(project_naam)
        return (project_folder / 'project.json').exists()
    
    def list_projectmappen(self) -> List[str]:
        """
        Geef een lijst van alle projectmappen.
        
        Returns:
            Lijst van projectnamen
        """
        projecten = []
        
        if not self.base_path.exists():
            return projecten
        
        for item in self.base_path.iterdir():
            if item.is_dir():
                project_file = item / 'project.json'
                if project_file.exists():
                    try:
                        with open(project_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            projecten.append(data['naam'])
                    except:
                        pass
        
        return projecten
