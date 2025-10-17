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
    geo_accession = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    organism = db.Column(db.String(100), nullable=False)
    data_type = db.Column(db.String(100), nullable=False)
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

def init_db():
    with app.app_context():
        db.create_all()
        
        if PlacentaStudy.query.count() == 0:
            test_data = [
                PlacentaStudy(
                    geo_accession='GSE12345',
                    title='Transcriptional profiling of human placenta at different gestational stages',
                    organism='homo sapiens',
                    data_type='bulk rna sequencing',
                    extracted_molecule='total RNA',
                    superseries='no',
                    summary='This study examines gene expression patterns in human placental tissue across first, second, and third trimesters.',
                    publication_date='2024-03-15'
                ),
                PlacentaStudy(
                    geo_accession='GSE23456',
                    title='Single-cell RNA sequencing reveals placental cell heterogeneity',
                    organism='homo sapiens',
                    data_type='single cell rna sequencing',
                    extracted_molecule='mRNA',
                    superseries='yes',
                    summary='Single-cell analysis of human placenta identifying distinct trophoblast populations and their developmental trajectories.',
                    publication_date='2024-05-20'
                ),
                PlacentaStudy(
                    geo_accession='GSE34567',
                    title='DNA methylation patterns in mouse placental development',
                    organism='mus musculus',
                    data_type='methylation sequencing',
                    extracted_molecule='DNA',
                    superseries='no',
                    summary='Genome-wide methylation analysis of mouse placenta during mid-to-late gestation.',
                    publication_date='2024-01-10'
                ),
                PlacentaStudy(
                    geo_accession='GSE45678',
                    title='Spatial transcriptomics of term human placenta',
                    organism='homo sapiens',
                    data_type='spatial transcriptomics',
                    extracted_molecule='total RNA',
                    superseries='no',
                    summary='Spatial mapping of gene expression in term human placental villi using Visium technology.',
                    publication_date='2024-06-30'
                ),
                PlacentaStudy(
                    geo_accession='GSE56789',
                    title='Expression microarray analysis of placental insufficiency in rhesus macaque',
                    organism='macaca mulatta',
                    data_type='expression microarray',
                    extracted_molecule='cDNA',
                    superseries='no',
                    summary='Microarray study identifying differentially expressed genes in placental insufficiency model.',
                    publication_date='2023-11-22'
                ),
                PlacentaStudy(
                    geo_accession='GSE67890',
                    title='Proteomics of bovine placenta during pregnancy',
                    organism='bos taurus',
                    data_type='proteomics',
                    extracted_molecule='protein',
                    superseries='yes',
                    summary='Comprehensive proteomic analysis of bovine placental tissue at multiple pregnancy time points.',
                    publication_date='2024-02-14'
                ),
                PlacentaStudy(
                    geo_accession='GSE78901',
                    title='Whole genome sequencing of placental samples with chromosomal abnormalities',
                    organism='homo sapiens',
                    data_type='whole genome sequencing',
                    extracted_molecule='DNA',
                    superseries='no',
                    summary='WGS analysis of placental tissue from pregnancies with confirmed chromosomal anomalies.',
                    publication_date='2024-04-05'
                ),
                PlacentaStudy(
                    geo_accession='GSE89012',
                    title='Single nucleus RNA-seq of frozen placental tissue',
                    organism='homo sapiens',
                    data_type='single nucleus rna sequence',
                    extracted_molecule='mRNA',
                    superseries='no',
                    summary='snRNA-seq analysis of archived frozen placental samples for retrospective study.',
                    publication_date='2024-07-18'
                ),
                PlacentaStudy(
                    geo_accession='GSE90123',
                    title='Methylation array profiling of preeclamptic placentas',
                    organism='homo sapiens',
                    data_type='methylation array',
                    extracted_molecule='DNA',
                    superseries='yes',
                    summary='Epigenome-wide association study of preeclampsia using Illumina methylation arrays.',
                    publication_date='2024-08-09'
                ),
                PlacentaStudy(
                    geo_accession='GSE01234',
                    title='Gene expression in rat placental development',
                    organism='rattus norvegicus',
                    data_type='expression profiling by array',
                    extracted_molecule='total RNA',
                    superseries='no',
                    summary='Temporal gene expression profiling throughout rat placental development using microarrays.',
                    publication_date='2023-12-03'
                )
            ]
            
            db.session.add_all(test_data)
            db.session.commit()
            print("Test data added successfully!")

if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='0.0.0.0', port=5000)
