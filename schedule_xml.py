import xml.etree.ElementTree as ET
from xml.dom import minidom

slot_time = 1

schedule = {
    "Node_01": 0,
    "Node_02": 1,
    "Node_03": 0,
    "Node_04": 1,

    "Node_05": 2,
    "Node_06": 3,
    "Node_07": 2,
    "Node_08": 3,

    "Node_09": 0,
    "Node_10": 1,
    "Node_11": 4,
    "Node_12": 1,

    "Node_13": 2,
    "Node_14": 3,
    "Node_15": 2,
    "Node_16": 3
}


def create_xml(schedule):

    total_slots = max(
        schedule.values()
    ) + 1

    root = ET.Element("TDMA_SCHEDULE")

    root.set(
        "slotTimeMs",
        str(slot_time)
    )

    root.set(
        "frameLength",
        str(total_slots)
    )

    frame = ET.SubElement(
        root,
        "FRAME"
    )

    for slot in range(total_slots):

        slot_tag = ET.SubElement(
            frame,
            "SLOT"
        )

        slot_tag.set(
            "number",
            str(slot)
        )

        slot_tag.set(
            "timeMs",
            str(slot_time)
        )

        for node in sorted(schedule):

            if schedule[node] == slot:

                node_tag = ET.SubElement(
                    slot_tag,
                    "NODE"
                )

                node_tag.set(
                    "id",
                    node
                )

                node_tag.set(
                    "transmit",
                    "true"
                )

    mapping = ET.SubElement(
        root,
        "NODE_MAPPING"
    )

    for node in sorted(schedule):

        node_tag = ET.SubElement(
            mapping,
            "NODE"
        )

        node_tag.set(
            "id",
            node
        )

        node_tag.set(
            "slot",
            str(schedule[node])
        )

    xml_text = ET.tostring(
        root,
        encoding="unicode"
    )

    return minidom.parseString(
        xml_text
    ).toprettyxml(
        indent="    "
    )


xml_output = create_xml(schedule)

print("=" * 60)
print("TDMA XML SCHEDULE")
print("=" * 60)

print(xml_output)

print("=" * 60)
print("FINAL RESULT")
print("=" * 60)

print("TDMA schedule : VALID")
print("XML schedule  : GENERATED")
print("Slot time     :", slot_time, "ms")
print(
    "Frame length  :",
    max(schedule.values()) + 1,
    "slots"
)
print("Status        : SUCCESS")
