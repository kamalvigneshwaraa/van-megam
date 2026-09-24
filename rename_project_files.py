import os
import shutil

src_dir = r"C:\Users\dheeb\.gemini\antigravity\scratch\tdma_schedule_optimizer"

rename_map = {
    "tdma_brain.py": "1_TDMA_Network_Brain.py",
    "emane_bridge.py": "2_EMANE_Integration_Bridge.py",
    "generate_flowchart.py": "3_Generate_Flowchart_Diagram.py",
    "generate_visualizations.py": "3_Generate_Visual_Diagrams.py",
    "generate_pdf_report.py": "4_Generate_Documentation_PDF.py",
    "generate_pptx_presentation.py": "5_Generate_Presentation_PPTX.py",
    "nodes.json": "Node_Coordinates_Input.json",
    "emane_tdma_schedule.xml": "EMANE_TDMA_Schedule_Profile.xml"
}

for old_name, new_name in rename_map.items():
    old_path = os.path.join(src_dir, old_name)
    new_path = os.path.join(src_dir, new_name)
    if os.path.exists(old_path):
        shutil.copy2(old_path, new_path)
        print(f"[+] Copied {old_name} -> {new_name}")
