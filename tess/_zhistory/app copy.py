from flask import Flask, request, jsonify, Response
from tessellate import generate_svg_tessellation

app = Flask(__name__)

@app.route('/')
def index():
    return 'Tessagon API is running.'

@app.route('/tessellate', methods=['GET'])
def tessellate():
    try:
        u = int(request.args.get('u', 10))
        v = int(request.args.get('v', 10))
        svg = generate_svg_tessellation(u, v)
        return Response(svg, mimetype='image/svg+xml')
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
