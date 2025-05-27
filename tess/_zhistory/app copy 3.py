from flask import Flask, request, jsonify, Response
from tessellate import generate_svg_tessellation
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Tessagon API is running.'

@app.route('/tessellate', methods=['GET'])
def tessellate():
    try:
        u = int(request.args.get('u', 4))
        v = int(request.args.get('v', 4))
        shape = request.args.get('shape', 'Hexagon')
        # svg = generate_svg_tessellation(u, v, shape)
        # return Response(svg, mimetype='image/svg+xml')
        res = generate_svg_tessellation(u, v, shape)
        return jsonify(res) 
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
