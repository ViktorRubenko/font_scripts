from fontTools.ttLib import TTFont
import xml.etree.ElementTree as ET
import os
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--old', required=True)
    parser.add_argument('-n', '--new', required=True)
    parser.add_argument('-x', '--xml', required=True)

    args = parser.parse_args()
    old_path = args.old
    new_path = args.new
    vtt_path = args.xml
    
    old_glyph_order = {glyph_id: glyph_name for glyph_id, glyph_name
                       in enumerate(TTFont(old_path).getGlyphOrder())}
    new_glyph_order = {glyph_name: glyph_id for glyph_id, glyph_name
                       in enumerate(TTFont(new_path).getGlyphOrder())}

    tree = ET.parse(vtt_path)
    root = tree.getroot()
    for TTGlyph in root.find('glyf'):
        TTGlyph.set('ID', str(new_glyph_order[old_glyph_order[int(TTGlyph.attrib['ID'])]]))

        if TTGlyph.find('instructions//assembly').text:
            assembly = []
            for line in TTGlyph.find('instructions//assembly').text.splitlines():
                if line.startswith('OFFSET[R]'):
                    line = line.split(', ')
                    line[1] = str(new_glyph_order[old_glyph_order[int(line[1])]])
                    line = ', '.join(line)
                assembly.append(line)
                TTGlyph.find('instructions//assembly').text = '\n'.join(assembly) + '\n'
    xml_path = os.path.join(os.path.dirname(vtt_path),
                            os.path.basename(vtt_path)[:-4] + '_updated.xml')
    k = 1
    while True:
        if os.path.isfile(xml_path):
            xml_path = os.path.join(os.path.dirname(vtt_path),
                                    os.path.basename(vtt_path)[:-4] + '_updated#{}.xml'.format(k))
            k += 1
        else:
            tree.write(xml_path)
            print('New vtt xml generated to {}'.format(xml_path))
            return
    
            
if __name__ == '__main__':
    main()
