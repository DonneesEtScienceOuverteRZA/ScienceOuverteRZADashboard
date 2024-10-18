import json
import xmltodict

fichier="pages/data/ZAM-10-48579-PRO-WRKT4O.xml"

############# VERS JSON
with open(fichier) as xml_file:
    data_dict = xmltodict.parse(xml_file.read())
    xml_file.close()
    json_data = json.dumps(data_dict, indent=4)
    with open("data.json", "w") as json_file:
        json_file.write(json_data)
        json_file.close()

############# VERS XML
with open("data.json","r") as file:
    python_dict=json.load(file)

    with open("test_xml.xml","w") as xml_file:
        xmltodict.unparse(python_dict,output=xml_file)
        xml_file.close()
