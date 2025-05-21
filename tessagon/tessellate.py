from tessagon.types.hex_tessagon import HexTessagon
from tessagon.types.octo_tessagon import OctoTessagon
from tessagon.types.square_tessagon import SquareTessagon
from tessagon.types.tri_tessagon import TriTessagon
from tessagon.types.floret_tessagon import FloretTessagon
from tessagon.types.dissected_triangle_tessagon import DissectedTriangleTessagon
from tessagon.types.dissected_hex_quad_tessagon import DissectedHexQuadTessagon
from tessagon.types.pythagorean_tessagon import PythagoreanTessagon
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

    tessagon = PythagoreanTessagon(**options)
    svg = tessagon.create_mesh()
    return svg
