from flask import Blueprint, render_template, request, jsonify, session

reels_bp = Blueprint('reels', __name__)


@reels_bp.route('/reels')
def reels():
    categories = ["Tech", "Motivation", "Islamic", "AI"]
    selected_category = request.args.get("category")
    videos = []
    if selected_category:
        videos = [
            {"title": f"{selected_category} Reel 1", "video_id": "abc123"},
            {"title": f"{selected_category} Reel 2", "video_id": "def456"}
        ]
    return render_template("reels.html", user=session.get("user"), categories=categories,
                           selected_category=selected_category, videos=videos)


@reels_bp.route("/api/reels")
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
