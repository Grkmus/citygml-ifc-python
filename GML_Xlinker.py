import os
import xml.etree.ElementTree as et


"""This program coded for establish xlink mechanism on FME exported GML files."""

base_path = os.path.dirname(os.path.realpath(__file__))

xml_file = os.path.join(base_path, "lod3_3.gml")

tree = et.parse(xml_file)

root = tree.getroot()
# ------------------------ Namespace declaration for xml --------------------##
ns = {"bldg":"http://www.opengis.net/citygml/building/1.0",             
      'use':"http://www.opengis.net/citygml/landuse/1.0",               
      'app':"http://www.opengis.net/citygml/appearance/1.0",
      'xAL':"urn:oasis:names:tc:ciq:xsdschema:xAL:2.0",
      'base':"http://www.citygml.org/citygml/profiles/base/1.0",
      'frn':"http://www.opengis.net/citygml/cityfurniture/1.0",
      'smil20lang':"http://www.w3.org/2001/SMIL20/Language",
      'xsi':"http://www.w3.org/2001/XMLSchema-instance",
      'xlink':"http://www.w3.org/1999/xlink",
      'tex':"http://www.opengis.net/citygml/texturedsurface/1.0",
      'wtr':"http://www.opengis.net/citygml/waterbody/1.0",
      'smil20':"http://www.w3.org/2001/SMIL20/",
      'grp':"http://www.opengis.net/citygml/cityobjectgroup/1.0",
      'core':"http://www.opengis.net/citygml/1.0",
      'veg':"http://www.opengis.net/citygml/vegetation/1.0",
      'sch':"http://www.ascc.net/xml/schematron",
      'gen':"http://www.opengis.net/citygml/generics/1.0",
      'dem':"http://www.opengis.net/citygml/relief/1.0",
      'gml':"http://www.opengis.net/gml",
      'tran':"http://www.opengis.net/citygml/transportation/1.0"}

for key, value in ns.iteritems():
    et.register_namespace(key,value)
    
# ----------------------- Looping through the gml file--------------------##
for cityObjectMember in root.findall('core:cityObjectMember', ns):
    buildings = cityObjectMember.findall('bldg:Building', ns)
    for building in buildings:
        for element in building:
            if 'Solid' in element.tag:
                lod_level = element.tag
                break
        boundedBy = building.findall('bldg:boundedBy', ns)
        id_list = []
        #selecting all surface member defined in building tag 
        surfaceMembers = building.findall(".//%s//{http://www.opengis.net/gml}surfaceMember" % lod_level)
        #getting surface gml_id and adding it to polygon
        for element in boundedBy:
            surface = element[0]
            gml_id = surface.get('{http://www.opengis.net/gml}id')
            id_list.append(gml_id)
            surface.attrib.pop('{http://www.opengis.net/gml}id')
            polygon = surface.find('.//{http://www.opengis.net/gml}Polygon')
            polygon.set('{http://www.opengis.net/gml}id', gml_id)

        for i in range(len(surfaceMembers)):
            surfaceMembers[i].clear()
            surfaceMembers[i].set('{http://www.w3.org/1999/xlink}href', id_list[i])
 

tree.write('lod3-3_PYTHON.gml',  encoding="UTF-8", xml_declaration=True, method="xml")
