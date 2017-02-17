import code
import config
import svgwrite
import util
from itertools import groupby
from optparse import OptionParser


def create(input_image, output_path):
    """Create an SVG from the input image."""
    conf = config.get()
    im = util.get_image(input_image)
    (width, height) = im.size
    pix = im.load()

    dwg = svgwrite.Drawing(output_path,
                           profile='full',
                           width=width,
                           height=height,
                           viewBox='0 0 {0} {1}'.format(width * conf['svg']['ratio'], height),
                           style='font-family:\'Source Code Pro\';font-weight:900;font-size:{0}'.format(conf['svg']['font_size']))
    dwg.attribs['xml:space'] = 'preserve'

    for h in range(0, height):
        colors = []
        for w in range(0, width):
            try:
                colors.append(util.to_hex(pix[w, h]))
            except:
                colors.append('#FFFFFF')
                pass
        colors = [(len(list(g)), k) for k, g in groupby(colors)]
        x = 0
        for c in colors:
            t = ''
            for l in range(0, c[0]):
                t = t + code.get_char()
            text = dwg.text(t, fill='{0}'.format(c[1]))
            text.attribs['y'] = str(h)
            text.attribs['x'] = x * conf['svg']['ratio']
            dwg.add(text)
            x = x + len(t)
    dwg.save()


if __name__ == '__main__':
    parser = OptionParser(usage='usage: %prog -i <PATH TO INPUT FILE> -o <PATH TO OUTPUT FILE>')
    parser.add_option('-i', '--input',
                      help='The path to the input image file',)
    parser.add_option('-o', '--output',
                      help='The path to save the svg output file')

    (options, args) = parser.parse_args()
    if not options.input or not options.output:
        parser.error('Please provide both input and output parameters. ')
    
    create(options.input, options.output)
