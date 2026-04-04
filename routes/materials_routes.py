import os
import requests
from bs4 import BeautifulSoup
from flask import Blueprint, render_template, request, jsonify, session
from utils.helpers import login_required, is_academic_book
from config import OPENROUTER_API_KEY

materials_bp = Blueprint('materials', __name__)

@materials_bp.route('/about')
def about():
    return render_template('about.html')

@materials_bp.route('/campus-map')
def campus_map():
    return render_template('campus-map.html')

@materials_bp.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')

@materials_bp.route('/settings')
@login_required
def settings():
    memory = {
        "traits": session.get('traits', []),
        "more_info": session.get('more_info', ''),
        "enable_memory": session.get('enable_memory', False)
    }
    return render_template('settings.html', memory=memory, theme=session.get('theme'), language=session.get('language'))

@materials_bp.route('/memory', methods=['POST'])
@login_required
def save_memory():
    session['theme'] = request.form.get('theme')
    session['language'] = request.form.get('language')
    session['notifications'] = 'notifications' in request.form
    flash('Settings saved!')
    return redirect('/settings')

@materials_bp.route('/materials')
@login_required
def materials():
    username = session['user']['username']
    user = User.query.filter_by(username=username).first()
    all_courses = ["Python", "Data Science", "AI Basics", "Math", "Physics"]
    selected_course = request.args.get("course")
    materials_list = []
    if selected_course:
        materials_list = [
            {"title": f"{selected_course} Introduction", "description": f"Basics of {selected_course}", "link": "https://youtube.com"},
            {"title": f"{selected_course} Tutorial", "description": f"Complete guide on {selected_course}", "link": "https://youtube.com"}
        ]
    return render_template("materials.html", courses=all_courses, selected_course=selected_course, materials=materials_list, user=user)

@materials_bp.route('/api/materials')
def get_study_materials():
    query = request.args.get("q", "python")
    pdfs = []
    try:
        pdf_html = requests.get(f"https://www.pdfdrive.com/search?q={query}", headers={"User-Agent": "Mozilla/5.0"}, timeout=10).text
        soup = BeautifulSoup(pdf_html, 'html.parser')
        for book in soup.select('.file-left')[:5]:
            title = book.select_one('img')['alt']
            link = "https://www.pdfdrive.com" + book.parent['href']
            pdfs.append({'title': title, 'link': link})
    except Exception as e:
        pdfs = [{"error": str(e)}]
    books = []
    try:
        ol_data = requests.get(f"https://openlibrary.org/search.json?q={query}", timeout=10).json()
        for doc in ol_data.get("docs", [])[:5]:
            books.append({"title": doc.get("title"), "author": ', '.join(doc.get("author_name", [])) if doc.get("author_name") else "Unknown", "link": f"https://openlibrary.org{doc.get('key')}"})
    except Exception as e:
        books = [{"error": str(e)}]
    return jsonify({"query": query, "pdfs": pdfs, "books": books})

@materials_bp.route('/ai/materials')
def ai_materials():
    topic = request.args.get("topic")
    level = request.args.get("level")
    department = request.args.get("department")
    goal = request.args.get("goal", "general")
    if not topic or not level or not department:
        return jsonify({"error": "Missing one or more parameters: topic, level, department"}), 400
    prompt = f"You're an educational AI helping a {level} student in the {department} department. They want to learn: '{goal}' in the topic of {topic}. Provide a short and clear explanation. End with: '📚 Here are materials to study further:'"
    explanation = ""
    try:
        headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json", "HTTP-Referer": "https://nelavista.com", "X-Title": "Nelavista AI Tutor"}
        payload = {"model": "openai/gpt-4o-mini", "messages": [{"role": "system", "content": "You are an educational AI assistant."}, {"role": "user", "content": prompt}], "temperature": 0.7, "max_tokens": 500}
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            explanation = response.json()["choices"][0]["message"]["content"]
        else:
            explanation = f"Let me help you learn {topic}. Start with the basic concepts and build from there. 📚 Here are materials to study further:"
    except Exception:
        explanation = f"Let me help you learn {topic}. Start with the basic concepts and build from there. 📚 Here are materials to study further:"
    pdfs = []
    try:
        pdf_html = requests.get(f"https://www.pdfdrive.com/search?q={topic}", headers={"User-Agent": "Mozilla/5.0"}, timeout=10).text
        soup = BeautifulSoup(pdf_html, 'html.parser')
        for book in soup.select('.file-left')[:10]:
            title = book.select_one('img')['alt']
            if is_academic_book(title, topic, department):
                link = "https://www.pdfdrive.com" + book.parent['href']
                pdfs.append({'title': title, 'link': link})
    except Exception:
        pdfs = [{"error": "Failed to fetch PDFs"}]
    books = []
    try:
        ol_data = requests.get(f"https://openlibrary.org/search.json?q={topic}", timeout=10).json()
        for doc in ol_data.get("docs", [])[:10]:
            title = doc.get("title", "")
            if is_academic_book(title, topic, department):
                books.append({"title": doc.get("title"), "author": ', '.join(doc.get("author_name", [])) if doc.get("author_name") else "Unknown", "link": f"https://openlibrary.org{doc.get('key')}"})
    except Exception:
        books = [{"error": "Failed to fetch books"}]
    return jsonify({"query": topic, "ai_explanation": explanation, "pdfs": pdfs, "books": books})

@materials_bp.route("/mat101")
def math101():
    return render_template("mat101.html")

@materials_bp.route('/reels')
def reels():
    categories = ["Tech", "Motivation", "Islamic", "AI"]
    selected_category = request.args.get("category")
    videos = []
    if selected_category:
        videos = [{"title": f"{selected_category} Reel 1", "video_id": "abc123"}, {"title": f"{selected_category} Reel 2", "video_id": "def456"}]
    return render_template("reels.html", user=session.get("user"), categories=categories, selected_category=selected_category, videos=videos)

@materials_bp.route("/api/reels")
def get_reels():
    course = request.args.get("course")
    all_reels = [
        {"course": "Accountancy", "caption": "Introduction to Accounting", "video_url": "https://youtu.be/Gua2Bo_G-J0?si=FNnNZBbmBh0yqvrk"},
        {"course": "Accountancy", "caption": "Financial Statements Basics", "video_url": "https://youtu.be/fb7YCVR5fIU?si=XWozkxGoBV2HP2HW"},
        {"course": "Accountancy", "caption": "Management Accounting Overview", "video_url": "https://youtu.be/qISkyoiGHcI?si=BKRnkFfl-fqKXgLG"},
        {"course": "Accountancy", "caption": "Auditing Principles", "video_url": "https://youtu.be/27gabbJQZqc?si=rsOLmkD2QXOoxSoi"},
        {"course": "Accountancy", "caption": "Taxation Fundamentals", "video_url": "https://youtu.be/Cox8rLXYAGQ?si=CvKUaPuPJOxPb6cr"},
        {"course": "Accountancy", "caption": "Learn Accounting in under 5 hours", "video_url": "https://youtu.be/gPBhGkBN30s?si=bUYfaccZPlBni3aZ"},
        {"course": "Accountancy", "caption": "The ACCOUNTING BASICS for BEGINNERS (3 core parts)", "video_url": "https://youtu.be/Gua2Bo_G-J0?si=aM8ZPO-OqtV-ZbJ9"},
        {"course": "Accounting", "caption": "Basics of Double Entry", "video_url": "https://youtu.be/cjO8qHM5Wjg?si=P0hcqm9x-wjmXpN3"},
        {"course": "Accounting", "caption": "Trail Balance Explained", "video_url": "https://youtu.be/3_PfoTzSCQE?si=SGRI7KVJ6ZC3iJe7"},
        {"course": "Accounting", "caption": "Financial Analysis Techniques", "video_url": "https://youtu.be/g2wEFJ7upNs?si=ht44vAply2f7b-P0"},
        {"course": "Accounting", "caption": "Cost Accounting Overview", "video_url": "https://youtu.be/a5D3Iopi0-4?si=vXOVFcV1NqPGt6Tk"},
        {"course": "Accounting", "caption": "Budgeting and Forecasting", "video_url": "https://youtu.be/GjxhDo9luh8?si=BXn4Z5J-RdKJdBoP"},
        {"course": "Agriculture", "caption": "Introduction to Agriculture", "video_url": "https://youtu.be/1FLcijYWHZQ?si=B6iWcOVNXYCDWsKR"},
        {"course": "Agriculture", "caption": "Crop Production Techniques", "video_url": "https://youtu.be/j4-0rNhxoKs?si=XaUcN8zOq1EtkVbX"},
        {"course": "Agriculture", "caption": "Soil Fertility Management", "video_url": "https://youtu.be/TjbxOEEOCh0?si=grkiA5OewbgtFF78"},
        {"course": "Agriculture", "caption": "Livestock Management", "video_url": "https://youtu.be/TjbxOEEOCh0?si=Jr_UpYvei_oieZxz"},
        {"course": "Agriculture", "caption": "Agricultural Economics", "video_url": "https://youtu.be/fbOiwV3gBLg?si=f8HcQW1xdOEfQXEy"},
        {"course": "Arabic Studies", "caption": "Arabic Language Basics", "video_url": "https://youtu.be/X1mC1XY65Kc?si=gIIUVXBrseXau1Tj"},
        {"course": "Arabic Studies", "caption": "Arabic Grammar Essentials", "video_url": "https://youtu.be/CKD1O4tKZUA?si=JwH8Hb090aZTAI7n"},
        {"course": "Arabic Studies", "caption": "Conversational Arabic", "video_url": "https://youtu.be/dinQIb4ZFXY?si=eGF1Vhsdwm8imJ3Y"},
        {"course": "Arabic Studies", "caption": "Arabic Poetry Introduction", "video_url": "https://youtu.be/ZmjK5cu81RA?si=XnRGefNNXTCws278"},
        {"course": "Arabic Studies", "caption": "Arabic Writing Skills", "video_url": "https://youtu.be/b_WdZCrKr3k?si=pYe0F4bLx8FiT8HT"},
        {"course": "Banking and Finance", "caption": "Banking Systems Overview", "video_url": "https://youtu.be/fTTGALaRZoc?si=ThB2kkYTd_iIhFX1"},
        {"course": "Banking and Finance", "caption": "Financial Markets Basics", "video_url": "https://youtu.be/UOwi7MBSfhk?si=XSyvxPRp4mEQx2OH"},
        {"course": "Banking and Finance", "caption": "Loan and Credit Management", "video_url": "https://youtu.be/f3VgVOgAUoE?si=JwfSWSogIZeIMpY8"},
        {"course": "Banking and Finance", "caption": "Investment Banking Intro", "video_url": "https://youtu.be/-PkN15TtFnc?si=xgcAoZBAdge-PBjb"},
        {"course": "Banking and Finance", "caption": "Risk Management in Banking", "video_url": "https://youtu.be/BLAEuVSAlVM?si=hubXYQaexc2Iizjd"},
        {"course": "Biochemistry", "caption": "Introduction to Biochemistry", "video_url": "https://youtu.be/CHJsaq2lNjU?si=owCTFJffO4MyBtPB"},
        {"course": "Biochemistry", "caption": "Enzymes and their Functions", "video_url": "https://youtu.be/ozdO1mLXBQE?si=Xj6z5vY8rAgRMdA_"},
        {"course": "Biochemistry", "caption": "Metabolism Basics", "video_url": "https://youtu.be/onDQ9KgDSVw?si=4IKHj5VVJoahw51B"},
        {"course": "Biochemistry", "caption": "Protein Synthesis", "video_url": "https://youtu.be/8wAwLwJAGHs?si=vDuhcZbjQ0nNyhoL"},
        {"course": "Biochemistry", "caption": "Biochemical Techniques", "video_url": "https://youtu.be/lDWL_EEhReo?si=F4nhulNv3l0nxRcA"},
        {"course": "Botany", "caption": "Plant Classification", "video_url": "https://youtu.be/SAM5mcHkSxU?si=P1cX_dbg0pGJFDBB"},
        {"course": "Botany", "caption": "Photosynthesis Process", "video_url": "https://youtu.be/-ZRsLhaukn8?si=CfNMcb-tVWwq6-be"},
        {"course": "Botany", "caption": "Plant Anatomy", "video_url": "https://youtu.be/pvVvCt6Kdp8?si=3ubgF8WibXgzFLcI"},
        {"course": "Botany", "caption": "Plant Reproduction", "video_url": "https://youtu.be/h077JEQ8w6g?si=O5vHjcnuPetMLbCo"},
        {"course": "Botany", "caption": "Ecology and Environment", "video_url": "https://youtu.be/fxVGiq1kggg?si=ESD-BALtjmX0Qxcb"},
        {"course": "Zoology", "caption": "Animal Classification", "video_url": "https://example.com/videos/zoology1.mp4"},
    ]
    if course:
        matching = [r for r in all_reels if r["course"].lower() == course.lower()]
        return jsonify({"reels": matching})
    return jsonify({"reels": all_reels})

@materials_bp.route('/CBT', methods=['GET'])
@login_required
def CBT():
    topics = ["Python", "Hadith", "AI", "Math"]
    selected_topic = request.args.get("topic")
    questions = []
    if selected_topic:
        questions = [{"question": f"What is {selected_topic}?", "options": ["Option A", "Option B", "Option C"], "answer": "Option A"}, {"question": f"Why is {selected_topic} important?", "options": ["Reason 1", "Reason 2", "Reason 3"], "answer": "Reason 2"}]
    return render_template("CBT.html", user=session.get("user"), topics=topics, selected_topic=selected_topic, questions=questions)

@materials_bp.route('/teach-me-ai')
@login_required
def teach_me_ai():
    return render_template('teach-me-ai.html')

@materials_bp.route('/api/ai-teach')
def ai_teach():
    course = request.args.get("course")
    level = request.args.get("level")
    if not course or not level:
        return jsonify({"error": "Missing course or level"}), 400
    prompt = f"You're a tutor. Teach a {level} student the basics of {course} in a friendly and easy-to-understand way."
    try:
        headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json", "HTTP-Referer": "https://nelavista.com", "X-Title": "Nelavista AI Tutor"}
        payload = {"model": "openai/gpt-4o-mini", "messages": [{"role": "system", "content": "You are an educational AI assistant."}, {"role": "user", "content": prompt}], "temperature": 0.7, "max_tokens": 800}
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            summary = response.json()["choices"][0]["message"]["content"]
        else:
            summary = f"Let me teach you the basics of {course}. We'll start with fundamental concepts and build up from there. This is perfect for {level} students!"
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)})