from flask import Flask, request, jsonify, send_from_directory, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'placenta_database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class PlacentaStudy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    geo_accession = db.Column(db.String(20))
    title = db.Column(db.String(500))
    organism = db.Column(db.String(100))
    data_type = db.Column(db.String(100))
    extracted_molecule = db.Column(db.String(50))
    superseries = db.Column(db.String(10))
    summary = db.Column(db.Text)
    publication_date = db.Column(db.String(20))
    
    def to_dict(self):
        return {
            'id': self.id,
            'geo_accession': self.geo_accession,
            'title': self.title,
            'organism': self.organism,
            'data_type': self.data_type,
            'extracted_molecule': self.extracted_molecule,
            'superseries': self.superseries,
            'summary': self.summary,
            'publication_date': self.publication_date
        }

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if path.endswith('.db') or path.endswith('.py'):
        abort(403)
    
    allowed_extensions = ['.html', '.css', '.js', '.svg', '.png', '.jpg', '.jpeg', '.gif', '.ico']
    if not any(path.endswith(ext) for ext in allowed_extensions):
        abort(403)
    
    return send_from_directory('.', path)

@app.route('/api/studies', methods=['GET'])
def get_studies():
    organism = request.args.get('organism', '')
    data_type = request.args.get('data_type', '')
    molecule = request.args.get('molecule', '')
    superseries = request.args.get('superseries', '')
    
    query = PlacentaStudy.query
    
    if organism:
        query = query.filter(PlacentaStudy.organism.ilike(f'%{organism}%'))
    if data_type:
        query = query.filter(PlacentaStudy.data_type.ilike(f'%{data_type}%'))
    if molecule:
        molecules = [m.strip() for m in molecule.split(',')]
        molecule_filters = [PlacentaStudy.extracted_molecule.ilike(f'%{m}%') for m in molecules]
        query = query.filter(db.or_(*molecule_filters))
    if superseries:
        query = query.filter(PlacentaStudy.superseries == superseries)
    
    studies = query.all()
    return jsonify([study.to_dict() for study in studies])

@app.route('/api/studies/<int:id>', methods=['GET'])
def get_study(id):
    study = PlacentaStudy.query.get_or_404(id)
    return jsonify(study.to_dict())

@app.route('/api/stats', methods=['GET'])
def get_stats():
    total_studies = PlacentaStudy.query.count()
    organisms = db.session.query(PlacentaStudy.organism, db.func.count(PlacentaStudy.id)).group_by(PlacentaStudy.organism).all()
    data_types = db.session.query(PlacentaStudy.data_type, db.func.count(PlacentaStudy.id)).group_by(PlacentaStudy.data_type).all()
    
    return jsonify({
        'total_studies': total_studies,
        'by_organism': [{'organism': org, 'count': count} for org, count in organisms],
        'by_data_type': [{'data_type': dt, 'count': count} for dt, count in data_types]
    })

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
