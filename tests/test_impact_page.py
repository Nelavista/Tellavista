"""/impact and the landing page's track-record band.

The student figures on both pages are fixed, verified numbers set in the templates (not
computed), so these tests pin them: a stray edit to one page can't leave the homepage and
/impact telling a visitor two different stories.
"""
import pytest


@pytest.fixture
def pages_client(app):
    from app.routes.static_pages_routes import pages_bp
    app.register_blueprint(pages_bp)
    return app.test_client()


def test_impact_page_shows_verified_figures(pages_client):
    resp = pages_client.get('/impact')
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    assert '2,500+' in html
    assert '500+' in html
    assert 'Students trained in AI' in html


def test_impact_page_is_indexable(pages_client):
    html = pages_client.get('/impact').get_data(as_text=True)
    assert '<title>Nelavista Impact | Students, AI Training &amp; University Community</title>' in html
    assert '<meta name="description"' in html
    assert 'rel="canonical" href="http://localhost/impact"' in html
    assert 'noindex' not in html


def test_landing_band_links_to_impact_with_same_figures(pages_client):
    resp = pages_client.get('/')
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    assert 'href="/impact"' in html
    assert 'data-target="2500"' in html
    assert 'data-target="500"' in html
