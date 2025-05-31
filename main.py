import json
import sys
import xml.etree.ElementTree as ET


def xml_to_json(xml_string):
    def elem_to_dict(elem):
        d = {elem.tag: {}}
        children = list(elem)
        if children:
            dd = {}
            for dc in map(elem_to_dict, children):
                for k, v in dc.items():
                    if k in dd:
                        if not isinstance(dd[k], list):
                            dd[k] = [dd[k]]
                        dd[k].append(v)
                    else:
                        dd[k] = v
            d = {elem.tag: dd}
        if elem.attrib:
            d[elem.tag].update((k, v) for k, v in elem.attrib.items())
        text = elem.text.strip() if elem.text else ""
        if text:
            if children or elem.attrib:
                d[elem.tag]["#text"] = text
            else:
                d[elem.tag] = text
        return d

    root = ET.fromstring(xml_string)
    return json.dumps(elem_to_dict(root), indent=2)


def read_xml_and_convert(filename=None):
    xml_data = ""
    if filename is not None:
        print(filename)
        try:
            with open(filename, "r", encoding="utf-8") as f:
                xml_data = f.read()
        except FileNotFoundError:
            print(f"File not found: {filename}")
            return
    else:
        xml_data = sys.stdin.read()
    print(xml_to_json(xml_data), flush=True)


read_xml_and_convert(filename=sys.argv[1] if len(sys.argv) > 1 else None)
