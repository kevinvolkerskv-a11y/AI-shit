#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, r"c:\Users\tyron\OneDrive - Vonk\Documents\GitHub\Project-Task-management")

from Storage import StorageManager
from Project_manager import ProjectManager
from Task_manager import TaskManager
from Models import TaskPriority

# Test de persistentie
print("=== PERSISTENTIE TEST ===\n")

# Maak managers aan
storage = StorageManager()
pm = ProjectManager(storage)
tm = TaskManager(storage)

# Test 1: Maak project aan
print("Test 1: Project aanmaken...")
succes, bericht, project = pm.maak_project_aan("WebApp", "Een web applicatie project")
print(f"  {bericht}")
print(f"  Project in geheugen: {len(pm.projecten)} projecten\n")

# Test 2: Maak taak aan
if project:
    print("Test 2: Taak aanmaken...")
    succes, bericht, taak = tm.maak_taak_aan(project, "Homepage maken", "Maak de homepage", "hoog")
    print(f"  {bericht}")
    print(f"  Taken in project: {project.aantal_taken()}\n")
    
    # Test 3: Check mapstructuur
    print("Test 3: Mapstructuur controleren...")
    import os
    project_folder = storage._project_folder("WebApp")
    if project_folder.exists():
        print(f"  ✓ Map bestaat: {project_folder}")
        print(f"  Inhoud:")
        for item in os.listdir(project_folder):
            print(f"    - {item}")
    print()

# Test 4: Herlaad projecten van schijf
print("Test 4: Projecten herladen van schijf...")
pm2 = ProjectManager(storage)
print(f"  Geladen projecten: {len(pm2.projecten)}")
for p in pm2.projecten:
    print(f"    - {p.naam} ({p.aantal_taken()} taken)")
    for t in p.tasks:
        print(f"      - {t.titel} ({t.prioriteit.value})")

print("\n✓ Persistentie test voltooid!")
