import xml.etree.cElementTree as ET
import tarfile
from find_silence import *

files = os.listdir(output_dir)

ET.Element("?xml version=\"1.0\" encoding=\"UTF-8\"?")
root = ET.Element("drumkit_info")
instrument_list = ET.SubElement(root, "instrument_list")

for file in files:

    instrument = ET.SubElement(instrument_list, "instrument")

    ET.SubElement(instrument, "id").text = "0"
    ET.SubElement(instrument, "name").text = "sample"
    ET.SubElement(instrument, "volume").text = "1"
    ET.SubElement(instrument, "isLocked").text = "false"
    ET.SubElement(instrument, "pan_L").text = "1"
    ET.SubElement(instrument, "pan_R").text = "1"

    ET.SubElement(instrument, "randomPitchFactor").text = "0"
    ET.SubElement(instrument, "gain").text = "1"
    ET.SubElement(instrument, "filterActive").text = "false"
    ET.SubElement(instrument, "filterCutoff").text = "1"
    ET.SubElement(instrument, "filterResonance").text = "0"

    ET.SubElement(instrument, "Attack").text = "0"
    ET.SubElement(instrument, "Decay").text = "0"
    ET.SubElement(instrument, "Sustain").text = "1"
    ET.SubElement(instrument, "Release").text = "1000"
    ET.SubElement(instrument, "muteGroup").text = "-1"

    layer = ET.SubElement(instrument, "layer")

    ET.SubElement(layer, "filename").text = file
    ET.SubElement(layer, "min").text = "0"
    ET.SubElement(layer, "max").text = "1"
    ET.SubElement(layer, "gain").text = "1"
    ET.SubElement(layer, "pitch").text = "0"


tree = ET.ElementTree(root)
tree.write(output_dir+"/filename.xml")

with tarfile.open('kit.h2drumkit', "w:gz") as tar:
    tar.add(output_dir, arcname = os.path.basename(output_dir))
