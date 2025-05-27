from imports import tessagon_class_dict
from tessagon.adaptors.svg_adaptor import ListAdaptor
from flask import Flask, request, jsonify, Response
from tessellate import generate_svg_tessellation
from flask_cors import CORS

app = Flask(__name__)
#CORS(app)
CORS(app) #, resources={r"/tessellate*": {"origins": "*"}})

@app.route('/')
def index():
    return 'Tessagon API is running.'

def plane_function(u, v):
    return [u, v, 0]  # flat 2D plane

@app.route('/tessellate', methods=['GET'])
def tessellate():
    u = int(request.args.get('u', 5))
    v = int(request.args.get('v', 5))
    shape_name = request.args.get('shape', 'HexTessagon')
    options = {
        'function': plane_function,
        'u_range': [0.0, 1.0],
        'v_range': [0.0, 1.0],
        'u_num': u,
        'v_num': v,
        'u_cyclic': False,
        'v_cyclic': False,
        'adaptor_class': ListAdaptor
    }
    tessagon = globals()[shape_name](**options)  #
    #tess_class = tessagon_class_dict.get(shape_name)
    #tessagon = tess_class(**options)


    clean_options = {k: str(v) for k, v in options.items()}
    return jsonify({'opts':clean_options})
    return jsonify(options)

    tess_class = tessagon_class_dict.get(shape_name)
    print('class',tess_class)
    if tess_class is None:
        return jsonify({'error': f'Unknown tessagon shape: {shape_name}'}), 400

    options = {
        'u_num': u,
        'v_num': v,
        'adapter': ListAdaptor
    }

    tessagon = tess_class(**options)
    faces = tessagon.create_mesh()
    return jsonify(faces)

if __name__ == '__main__':
    app.run(debug=True)
