import csv
import os
import re

conceptScheme42 = ('@prefix skos:  <http://www.w3.org/2004/02/skos/core#> . \n'
                   '@prefix dct: <http://purl.org/dc/terms/> . \n'
                   '@prefix ldp:   <http://www.w3.org/ns/ldp#> .\n'
                   '@prefix reg:   <http://purl.org/linked-data/registry#> .\n'
                   '@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .\n\n'
                   '<4.2> a reg:Register , skos:ConceptScheme , ldp:Container  ;\n'
                   '\tldp:isMemberOfRelation skos:inScheme ;\n'
                   '\trdfs:label "Code table 4.2 - Parameter Number"@en ;\n'
                   '\tdct:description "Parameter number by product discipline and parameter category "@en .\n')

conceptScheme45 = ('@prefix skos:  <http://www.w3.org/2004/02/skos/core#> . \n'
                   '@prefix dct: <http://purl.org/dc/terms/> . \n'
                   '@prefix ldp:   <http://www.w3.org/ns/ldp#> .\n'
                   '@prefix reg:   <http://purl.org/linked-data/registry#> .\n'
                   '@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .\n\n'
                   '<4.5> a reg:Register , skos:ConceptScheme , ldp:Container  ;\n'
                   '\tldp:isMemberOfRelation skos:inScheme ;\n'
                   '\trdfs:label "Fixed surface types and units"@en ;\n'
                   '\tdct:description "Code table 4.5 - Fixed surface types and units."@en .\n')

conceptTemplate42 = ('@prefix skos:  <http://www.w3.org/2004/02/skos/core#> . \n'
                     '@prefix dct: <http://purl.org/dc/terms/> . \n'
                   '@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .\n\n'
                   '<{d}-{c}-{n}> a skos:Concept, <http://codes.wmo.int/def/grib2/Parameter> ;\n'
                   '\trdfs:label "{label}"@en ;\n'
                   '\tdct:description "{label}"@en ;'
                   '\tskos:prefLabel "{label}"@en ;'
                   '\t<http://metarelate.net/vocabulary/index.html#identifier> '
                   '\t<http://codes.wmo.int/def/common/edition> , '
                   '\t<http://codes.wmo.int/def/grib2/discipline> , '
                   '\t<http://codes.wmo.int/def/grib2/parameter> , '
                   '\t<http://codes.wmo.int/def/grib2/category> ;\n'
                   '\t<http://codes.wmo.int/def/common/edition> <http://codes.wmo.int/codeform/grib2> ;\n'
                   '{u}'
                   '\t<http://codes.wmo.int/def/grib2/category> <http://codes.wmo.int/grib2/codeflag/4.1/{d}-{c}> ;\n'
                   '\t<http://codes.wmo.int/def/grib2/discipline> <http://codes.wmo.int/grib2/codeflag/0.0/{d}> ;\n'
                   '\t<http://codes.wmo.int/def/grib2/parameter> {n} ;\n'
                   '\t.\n')

conceptTemplate45 = ('@prefix skos:  <http://www.w3.org/2004/02/skos/core#> . \n'
                     '@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .\n\n'
                     '<{cf}> a skos:Concept ;\n'
                     '\trdfs:label "{label}"@en ;\n'
                     '\tskos:notation "{cf}"@en ;\n'
                     '{u}'
                     '\t.\n')

slashunit = re.compile('^([a-zA-Z]*)/([a-zA-Z]*)')

def unit_of_measure(code):
    unit = code
    if unit == '-':
        unit = 'N_unit'
    elif unit == 'sigma value' or unit == 'Numeric' or unit == 'Proportion':
        unit = '1'
    elif unit == '%':
        unit = 'percent'
    unitmatch = slashunit.match(unit)

    if unitmatch:
        if len(unitmatch.groups()) != 2:
            raise ValueError('unit slash parsing failed with unit: {}'.format(unit))
        unit = '{} {}-1'.format(unitmatch.group(1), unitmatch.group(2))
    unit = unit.replace(' ', '_')
    return unit

def main():
    print('Make GRIB2 TTL contents')
    root_path = os.path.split(os.path.dirname(__file__))[0]

    if not os.path.exists(os.path.join(root_path, 'codeflag')):
        os.mkdir(os.path.join(root_path, 'codeflag'))

    with open(os.path.join(root_path, 'codeflag/4.2.ttl'), 'w') as csf:
        csf.write(conceptScheme42)

    with open(os.path.join(root_path, 'GRIB2_CodeFlag_4_2_CodeTable_en.csv'), encoding='utf-8') as cf:
        greader = csv.DictReader(cf)
        dcp = re.compile("Product discipline ([0-9]+) - [a-zA-Z ]+, parameter category ([0-9]+): [a-zA-Z ]+")
        ttlpath = os.path.join(root_path, 'codeflag', '4.2')
        if not os.path.exists(ttlpath):
            os.mkdir(ttlpath)
        for entity in greader:
            if dcp.match(entity['SubTitle_en']) is None:
                raise ValueError('discipline and category not defined')

            discipline, category = dcp.match(entity['SubTitle_en']).groups()

            fpath = os.path.join(ttlpath,
                                 '{d}-{c}-{n}.ttl'.format(d=discipline,
                                                          c=category,
                                                          n=entity['CodeFlag']))
            with open(fpath, 'w', encoding='utf-8') as fh:
                # unit is not fully populated yet
                ustr = ''

                if entity['UnitComments_en']:
                    ustr = '\t<http://codes.wmo.int/def/common/unit> <http://codes.wmo.int/common/unit/{}> ;\n'
                    #ustr = ustr.format(entity['UnitComments_en'].replace(' ', '_'))
                    ustr = ustr.format(unit_of_measure(entity['UnitComments_en']))
                fh.write(conceptTemplate42.format(d=discipline,
                                                c=category,
                                                n=entity['CodeFlag'],
                                                label=entity['MeaningParameterDescription_en'],
                                                u=ustr))

    # with open(os.path.join(root_path, 'codeflag/4.5.ttl'), 'w') as csf:
    #     csf.write(conceptScheme45)

    # with open(os.path.join(root_path, 'GRIB2SurfaceLocalTable.csv'), encoding='utf-8') as cf:
    #     greader = csv.DictReader(cf)
    #     ttlpath = os.path.join(root_path, 'codeflag', '4.5')
    #     if not os.path.exists(ttlpath):
    #         os.mkdir(ttlpath)
    #     for entity in greader:
    #         fpath = os.path.join(ttlpath, '{}.ttl'.format(entity['Code figure']))
    #         with open(fpath, 'w', encoding='utf-8') as fh:
    #             ustr = ''
    #             if entity['Unit']:
    #                 ustr = '\t<http://codes.wmo.int/def/common/unit> "{}" ;\n'
    #                 ustr = ustr.format(entity['Unit'])
    #             fh.write(conceptTemplate45.format(cf=entity['Code figure'],
    #                                             label=entity['Parameter'],
    #                                             u=ustr))


if __name__ == '__main__':
    main()
