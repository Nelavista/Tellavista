from app import app, db
from models import Material

with app.app_context():
    # Count total materials
    total = Material.query.count()
    print(f"Total materials: {total}")
    
    # Count by source
    static = Material.query.filter_by(source='static').count()
    uploaded = Material.query.filter_by(source='uploaded').count()
    google = Material.query.filter_by(source='google_auto').count()
    
    print(f"Static materials: {static}")
    print(f"Uploaded materials: {uploaded}")
    print(f"Google materials: {google}")
    
    # Show some examples
    print("\nSample materials:")
    samples = Material.query.filter_by(is_approved=True).limit(10).all()
    for m in samples:
        print(f"  - {m.course_code}: {m.title}")