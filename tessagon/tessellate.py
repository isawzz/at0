from tessagon.types.hex_tessagon import HexTessagon
from tessagon.adaptors.svg_adaptor import SvgAdaptor

def plane_function(u, v):
    return [u, v, 0]  # flat 2D plane

def generate_svg_tessellation(u_num=10, v_num=10):
    options = {
        'function': plane_function,
        'u_range': [0.0, 1.0],
        'v_range': [0.0, 1.0],
        'u_num': u_num,
        'v_num': v_num,
        'u_cyclic': False,
        'v_cyclic': False,
        'adaptor_class': SvgAdaptor
    }

    tessagon = HexTessagon(**options)
    svg = tessagon.create_mesh()
    return svg
