# region tessagon_classes
# from imports import tessagon_class_dict
from tessagon.types.big_hex_tri_tessagon import BigHexTriTessagon
from tessagon.types.brick_tessagon import BrickTessagon
from tessagon.types.cloverdale_tessagon import CloverdaleTessagon
from tessagon.types.dissected_hex_quad_tessagon import DissectedHexQuadTessagon
from tessagon.types.dissected_hex_tri_tessagon import DissectedHexTriTessagon
from tessagon.types.dissected_square_tessagon import DissectedSquareTessagon
from tessagon.types.dissected_triangle_tessagon import DissectedTriangleTessagon
from tessagon.types.dodeca_tessagon import DodecaTessagon
from tessagon.types.dodeca_tri_tessagon import DodecaTriTessagon
from tessagon.types.floret_tessagon import FloretTessagon
from tessagon.types.hex_big_tri_tessagon import HexBigTriTessagon
from tessagon.types.hex_square_tri_tessagon import HexSquareTriTessagon
from tessagon.types.hex_tessagon import HexTessagon
from tessagon.types.hex_tri_tessagon import HexTriTessagon
from tessagon.types.islamic_hex_stars_tessagon import IslamicHexStarsTessagon
from tessagon.types.islamic_stars_crosses_tessagon import IslamicStarsCrossesTessagon
from tessagon.types.octo_tessagon import OctoTessagon
from tessagon.types.penta_tessagon import PentaTessagon
from tessagon.types.penta2_tessagon import Penta2Tessagon
from tessagon.types.pythagorean_tessagon import PythagoreanTessagon
from tessagon.types.rhombus_tessagon import RhombusTessagon
from tessagon.types.square_tessagon import SquareTessagon
from tessagon.types.square_tri_tessagon import SquareTriTessagon
from tessagon.types.square_tri2_tessagon import SquareTri2Tessagon
from tessagon.types.stanley_park_tessagon import StanleyParkTessagon
from tessagon.types.tri_tessagon import TriTessagon
from tessagon.types.valemount_tessagon import ValemountTessagon
from tessagon.types.weave_tessagon import WeaveTessagon
from tessagon.types.zig_zag_tessagon import ZigZagTessagon

tessagon_class_dict = {
    "BigHexTriTessagon": BigHexTriTessagon,
    "BrickTessagon": BrickTessagon,
    "CloverdaleTessagon": CloverdaleTessagon,
    "DissectedHexQuadTessagon": DissectedHexQuadTessagon,
    "DissectedHexTriTessagon": DissectedHexTriTessagon,
    "DissectedSquareTessagon": DissectedSquareTessagon,
    "DissectedTriangleTessagon": DissectedTriangleTessagon,
    "DodecaTessagon": DodecaTessagon,
    "DodecaTriTessagon": DodecaTriTessagon,
    "FloretTessagon": FloretTessagon,
    "HexBigTriTessagon": HexBigTriTessagon,
    "HexSquareTriTessagon": HexSquareTriTessagon,
    "HexTessagon": HexTessagon,
    "HexTriTessagon": HexTriTessagon,
    "IslamicHexStarsTessagon": IslamicHexStarsTessagon,
    "IslamicStarsCrossesTessagon": IslamicStarsCrossesTessagon,
    "OctoTessagon": OctoTessagon,
    "PentaTessagon": PentaTessagon,
    "Penta2Tessagon": Penta2Tessagon,
    "PythagoreanTessagon": PythagoreanTessagon,
    "RhombusTessagon": RhombusTessagon,
    "SquareTessagon": SquareTessagon,
    "SquareTriTessagon": SquareTriTessagon,
    "SquareTri2Tessagon": SquareTri2Tessagon,
    "StanleyParkTessagon": StanleyParkTessagon,
    "TriTessagon": TriTessagon,
    "ValemountTessagon": ValemountTessagon,
    "WeaveTessagon": WeaveTessagon,
    "ZigZagTessagon": ZigZagTessagon,
}


# endregion
from tessagon.adaptors.svg_adaptor import SvgAdaptor
from tessagon.adaptors.list_adaptor import ListAdaptor
from flask import Flask, request, jsonify, Response
from tessellate import generate_svg_tessellation
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# region functions
def plane_function(u, v):
    return [u, v, 0]  # flat 2D plane


def clean_object(obj):
    return {k: str(v) for k, v in obj.items()}

from tessagon.types.hex_tessagon import HexTessagon
from tessagon.adaptors.svg_adaptor import SvgAdaptor

def generate_svg_tessellation(u_num=10, v_num=10, shape_func=HexTessagon):
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

    tessagon = shape_func(**options)
    svg = tessagon.create_mesh()
    return svg

def generate_list_tessellation(u_num=10, v_num=10, shape_func=HexTessagon):
    options = {
        'function': plane_function,
        'u_range': [0.0, 1.0],
        'v_range': [0.0, 1.0],
        'u_num': u_num,
        'v_num': v_num,
        'u_cyclic': False,
        'v_cyclic': False,
        'adaptor_class': ListAdaptor  # Use ListAdaptor here
    }

    tessagon = shape_func(**options)
    faces = tessagon.create_mesh()
    return faces

# endregion


@app.route("/")
def index():
    return "Tessagon API is running."


@app.route("/tessellate", methods=["GET"])
def tessellate():
    u = int(request.args.get("u", 5))
    v = int(request.args.get("v", 5))
    shape_name = request.args.get("shape", "HexTessagon")
    options = {
        "function": plane_function,
        "u_range": [0.0, 1.0],
        "v_range": [0.0, 1.0],
        "u_num": u,
        "v_num": v,
        "u_cyclic": False,
        "v_cyclic": False,
        "adaptor_class": SvgAdaptor,
    }
    # tessagon = globals()[shape_name](**options)  #
    tess_class = tessagon_class_dict.get(shape_name)
    tessagon = tess_class(**options)
    faces = tessagon.create_mesh()
    return jsonify(faces)

@app.route('/tesvg', methods=['GET'])
def tesvg():
    try:
        u = int(request.args.get('u', 3))
        v = int(request.args.get('v', 3))
        shape_name = request.args.get('shape', 'HexTessagon')
        func = tessagon_class_dict.get(shape_name)
        svg = generate_svg_tessellation(u, v, func)
        return Response(svg, mimetype='image/svg+xml')
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/teslist', methods=['GET'])
def teslist():
    try:
        u = int(request.args.get('u', 2))
        v = int(request.args.get('v', 2))
        shape_name = request.args.get('shape', 'HexTessagon')
        func = tessagon_class_dict.get(shape_name)
        faces = generate_list_tessellation(u,v,func)
        return jsonify(faces)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
