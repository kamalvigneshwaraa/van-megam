#!/usr/bin/env python3
"""
EMANE Integration Bridge Generator (Physical Emulator Setup)
Converts TDMA schedule matrix into native EMANE TDMA Radio Model XML profiles.
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
from tdma_brain import optimize_schedule, NODE_COORDINATES, RADIO_RANGE

# ---------------------------------------------------------
# CONFIGURATION INITIALIZATION
# ---------------------------------------------------------
OUTPUT_XML_FILE = "emane_tdma_schedule.xml"
SLOT_DURATION_MICROSECONDS = 1000  # 1 millisecond


def convert_schedule_to_emane_xml(schedule, slot_duration_us=SLOT_DURATION_MICROSECONDS):
    """Generates native EMANE XML schedule profile."""
    num_slots = max(schedule.values()) + 1 if schedule else 1

    root = ET.Element("emane-tdma-schedule", version="1.0")

    structure = ET.SubElement(
        root, "structure",
        frames="1",
        slots=str(num_slots),
        slotduration=str(slot_duration_us),
        bandwidth="1000000"
    )
    ET.SubElement(structure, "frequency", index="0", hz="2400000000")

    schedule_elem = ET.SubElement(root, "schedule")

    nodes_by_slot = {}
    for node, slot in schedule.items():
        nodes_by_slot.setdefault(slot, []).append(node)

    for slot_idx in range(num_slots):
        slot_elem = ET.SubElement(schedule_elem, "slot", index=str(slot_idx))
        assigned_nodes = nodes_by_slot.get(slot_idx, [])

        for node_id in sorted(assigned_nodes):
            nem_id = int("".join(filter(str.isdigit, node_id)))
            ET.SubElement(slot_elem, "tx", nem=str(nem_id), frequency="0", power="0.0")

    rough_string = ET.tostring(root, encoding="utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def run_emane_bridge(coords=NODE_COORDINATES, radio_range=RADIO_RANGE, output_file=OUTPUT_XML_FILE):
    """Executes schedule calculation and XML file generation."""
    _, _, schedule = optimize_schedule(coords, radio_range)
    
    xml_data = convert_schedule_to_emane_xml(schedule)
    with open(output_file, "w") as f:
        f.write(xml_data)
        
    print(f"[+] Successfully generated EMANE XML schedule: {output_file}")
    print(f"[+] Total Slots Configured: {max(schedule.values()) + 1}")
    return schedule


if __name__ == "__main__":
    run_emane_bridge()
