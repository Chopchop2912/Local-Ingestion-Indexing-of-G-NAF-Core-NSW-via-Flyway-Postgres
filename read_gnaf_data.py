from pathlib import Path
import pandas as pd 

gnaf_folder = Path("C:/Users/Justin.Lam/Desktop/GNAFAUGUST2026/Standard")


psv_files = psv_files = list(gnaf_folder.glob("**/*STREET_LOCALITY_ALIAS_psv.psv"))

if not psv_files:
    print(
        "❌ No matching STREET_LOCALITY_ALIAS_psv.psv files found."
    )
else:
    print(f"✅ Found {len(psv_files)} matching files:")


    for file_path in psv_files:
        print(f"  - {file_path.name}")



