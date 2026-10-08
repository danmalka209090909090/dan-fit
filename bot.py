import streamlit as st
import streamlit.components.v1 as components
import time
import urllib.parse
import sqlite3
import json
from datetime import date
from PIL import Image
from google import genai

st.set_page_config(
    page_title="DaniFit Pro | פלטפורמת כושר ותזונה מתקדמת",
    page_icon="⚡",
    layout="wide"
)

# --- שכבת מסד נתונים מקומי (SQLite) לשמירה קבועה ---
DB_FILE = "danifit_data.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS daily_data (
            date_str TEXT PRIMARY KEY,
            water_ml INTEGER,
            extra_burned INTEGER,
            logged_items TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS pr_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise TEXT,
            weight REAL,
            reps INTEGER,
            custom_res TEXT,
            date_recorded TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS shopping_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT,
            search TEXT,
            checked INTEGER
        )
    """)
    conn.commit()
    conn.close()

def load_today_data():
    today = str(date.today())
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT water_ml, extra_burned, logged_items FROM daily_data WHERE date_str = ?", (today,))
    row = c.fetchone()
    conn.close()
    if row:
        return row[0], row[1], json.loads(row[2])
    return 0, 0, []

def save_today_data(water_ml, extra_burned, logged_items):
    today = str(date.today())
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO daily_data (date_str, water_ml, extra_burned, logged_items)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(date_str) DO UPDATE SET
            water_ml=excluded.water_ml,
            extra_burned=excluded.extra_burned,
            logged_items=excluded.logged_items
    """, (today, water_ml, extra_burned, json.dumps(logged_items, ensure_ascii=False)))
    conn.commit()
    conn.close()

def load_prs():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, exercise, weight, reps, custom_res, date_recorded FROM pr_records ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    prs = []
    for r in rows:
        prs.append({"id": r[0], "exercise": r[1], "weight": r[2], "reps": r[3], "custom_res": r[4], "date": r[5]})
    return prs

def add_pr(exercise, weight, reps, custom_res=""):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO pr_records (exercise, weight, reps, custom_res, date_recorded) VALUES (?, ?, ?, ?, ?)",
              (exercise, weight, reps, custom_res, str(date.today())))
    conn.commit()
    conn.close()

def delete_pr(pr_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM pr_records WHERE id = ?", (pr_id,))
    conn.commit()
    conn.close()

# אתחול נתונים
init_db()
if "db_initialized" not in st.session_state:
    w, b, items = load_today_data()
    st.session_state.water_ml = w
    st.session_state.extra_burned_cals = b
    st.session_state.logged_items = items
    st.session_state.db_initialized = True

if "shopping_list" not in st.session_state:
    st.session_state.shopping_list = [
        {"item": "חזה עוף טרי (1 ק״ג)", "search": "חזה עוף", "checked": False},
        {"item": "טונה במים (4 קופסאות)", "search": "טונה במים", "checked": False},
        {"item": "יוגורט חלבון PRO 20g", "search": "יוגורט פרו", "checked": False},
        {"item": "גבינת קוטג' 5%", "search": "קוטג 5", "checked": False},
        {"item": "תבנית ביצים L", "search": "ביצים L", "checked": False},
        {"item": "אורז בסמטי (1 ק״ג)", "search": "אורז בסמטי", "checked": False},
        {"item": "שיבולת שועל דקה", "search": "שיבולת שועל", "checked": False},
        {"item": "טורטיות מקמח מלא", "search": "טורטיות", "checked": False},
        {"item": "שמן זית כתית מעולה", "search": "שמן זית", "checked": False}
    ]

# עיצוב ונראות
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&family=Rubik:wght@400;600;700;800;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #f8fafc !important;
        font-family: 'Assistant', 'Rubik', sans-serif !important;
        direction: rtl;
        text-align: right;
        color: #1e293b !important;
    }

    .top-header-bar {
        display: flex;
        justify-content: flex-start;
        align-items: center;
        padding: 4px 10px 10px 10px;
    }

    .bsd-badge {
        font-weight: 800;
        font-size: 1.05rem;
        color: #64748b;
        letter-spacing: 1.5px;
    }

    .brand-header {
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        padding: 32px 24px;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.04);
        text-align: center;
        margin-bottom: 20px;
    }
    
    .brand-title {
        font-family: 'Rubik', sans-serif;
        font-size: 3rem;
        font-weight: 900;
        color: #0f172a;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .brand-title span {
        color: #2563eb;
    }

    .brand-subtitle {
        font-size: 1.25rem;
        color: #2563eb;
        font-weight: 800;
        margin-top: 6px;
    }

    .brand-description {
        font-size: 1.02rem;
        color: #475569;
        font-weight: 500;
        max-width: 800px;
        margin: 12px auto 18px auto;
        line-height: 1.6;
    }

    .brand-badges {
        display: flex;
        justify-content: center;
        gap: 10px;
        flex-wrap: wrap;
    }

    .badge-pill {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        color: #334155;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.88rem;
        font-weight: 700;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }

    .card-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    }

    .story-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #ffffff;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        max-width: 480px;
        margin: 0 auto 20px auto;
        box-shadow: 0 15px 35px rgba(15, 23, 42, 0.3);
        border: 2px solid #38bdf8;
    }

    .water-box {
        background: #f0f9ff;
        border: 1px solid #bae6fd;
        padding: 18px;
        border-radius: 16px;
        margin-bottom: 20px;
    }

    .suggest-box {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        padding: 18px;
        border-radius: 16px;
        margin-top: 15px;
        margin-bottom: 20px;
    }

    .quick-shop-btn {
        display: inline-block;
        text-align: center;
        background: #eff6ff;
        color: #2563eb !important;
        border: 1px solid #bfdbfe;
        padding: 6px 14px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.88rem;
        text-decoration: none;
        transition: 0.2s;
    }

    .quick-shop-btn:hover {
        background: #2563eb;
        color: #ffffff !important;
    }

    h1, h2, h3, .stSubheader {
        color: #0f172a !important;
        font-weight: 800 !important;
        border-bottom: 2px solid #2563eb;
        padding-bottom: 8px;
        margin-top: 20px !important;
        margin-bottom: 18px !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #ffffff;
        padding: 8px 12px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
    }

    .stTabs [data-baseweb="tab"] {
        color: #64748b !important;
        border-radius: 12px;
        padding: 10px 22px;
        font-weight: 700;
        font-size: 1.05rem;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.25);
    }

    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: #ffffff !important;
        border: none;
        border-radius: 12px;
        padding: 14px 24px;
        font-size: 1.1rem;
        font-weight: 800;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.25);
        transition: all 0.2s ease;
    }

    input, textarea, .stSelectbox {
        direction: rtl !important;
        text-align: right !important;
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
    }

    label {
        color: #334155 !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# בס"ד
st.markdown("""
<div class="top-header-bar">
    <span class="bsd-badge">בס״ד</span>
</div>
""", unsafe_allow_html=True)

# מאגר מזונות בסיסי
FOOD_DATABASE = {
    "חזה עוף צלוי": {"cal": 165, "p": 31.0, "c": 0.0, "f": 3.6, "unit": "100 גרם"},
    "פילה דג סלמון": {"cal": 208, "p": 20.0, "c": 0.0, "f": 13.0, "unit": "100 גרם"},
    "טונה במים (מסוננת)": {"cal": 130, "p": 28.0, "c": 0.0, "f": 1.0, "unit": "קופסה (נטו)"},
    "ביצה שלמה (L)": {"cal": 75, "p": 6.5, "c": 0.5, "f": 5.0, "unit": "יחידה"},
    "חלבון ביצה (לבן בלבד)": {"cal": 17, "p": 3.6, "c": 0.2, "f": 0.1, "unit": "יחידה"},
    "יוגורט חלבון (PRO / GO)": {"cal": 125, "p": 20.0, "c": 6.5, "f": 0.5, "unit": "גביע (200 גרם)"},
    "גבינה לבנה 5%": {"cal": 95, "p": 10.0, "c": 4.0, "f": 5.0, "unit": "100 גרם"},
    "גבינת קוטג' 5%": {"cal": 95, "p": 11.0, "c": 3.5, "f": 5.0, "unit": "100 גרם"},
    "אורז בסמטי מבושל": {"cal": 130, "p": 2.7, "c": 28.0, "f": 0.3, "unit": "100 גרם"},
    "פסטה מבושלת": {"cal": 155, "p": 5.5, "c": 30.0, "f": 1.0, "unit": "100 גרם"},
    "בטטה אפויה": {"cal": 90, "p": 2.0, "c": 21.0, "f": 0.1, "unit": "100 גרם"},
    "שיבולת שועל": {"cal": 150, "p": 5.0, "c": 27.0, "f": 3.0, "unit": "40 גרם"},
    "לחם מלא": {"cal": 75, "p": 3.5, "c": 13.0, "f": 1.0, "unit": "פרוסה"},
    "בננה בינונית": {"cal": 105, "p": 1.3, "c": 27.0, "f": 0.3, "unit": "יחידה"},
    "תפוח עץ": {"cal": 80, "p": 0.4, "c": 21.0, "f": 0.2, "unit": "יחידה"},
    "שמן זית כתית מעולה": {"cal": 120, "p": 0.0, "c": 0.0, "f": 13.5, "unit": "כף"},
    "טחינה גולמית": {"cal": 100, "p": 3.0, "c": 2.0, "f": 9.0, "unit": "כף"},
    "אבוקדו": {"cal": 160, "p": 2.0, "c": 8.5, "f": 14.5, "unit": "חצי פרי"}
}

# מאגר שבת
SHABBAT_FOOD_DB = {
    "כוסית יין קידוש / תירוש (100 מ״ל)": {"cal": 85, "p": 0.2, "c": 18.0, "f": 0.0},
    "פרוסת חלת שבת (50 גרם)": {"cal": 145, "p": 4.5, "c": 26.0, "f": 2.5},
    "מנת דג חריף (אמנון ברוטב, 150 גרם)": {"cal": 210, "p": 28.0, "c": 4.0, "f": 9.0},
    "מנת פילה סלמון עשבי תיבול (150 גרם)": {"cal": 310, "p": 30.0, "c": 0.0, "f": 20.0},
    "כרע עוף / ירך בתנור (יחידה ללא עור)": {"cal": 220, "p": 26.0, "c": 1.0, "f": 12.0},
    "מנת צלי בקר מבושל (150 גרם)": {"cal": 290, "p": 36.0, "c": 2.0, "f": 15.0},
    "מנת חמין / צ'ולנט מסורתית עם בשר": {"cal": 460, "p": 28.0, "c": 45.0, "f": 18.0},
    "צלחת סלטי שבת מבושלים (3 כפות)": {"cal": 130, "p": 1.8, "c": 9.0, "f": 10.0}
}

# כותרת ראשית
st.markdown("""
<div class="brand-header">
    <div class="brand-title">⚡ <span>DaniFit</span> Pro</div>
    <div class="brand-subtitle">הפלטפורמה המקצועית והחכמה לתזונה, חיטוב וכושר שיא</div>
    <div class="brand-description">
        מערכת מתקדמת עם שמירת נתונים קבועה: מעקב קלוריות חכם וסוגר פינות, סריקת מנות במצלמת AI,
        הזמנת קניות בלחיצה לסופר, כרטיסיית הישגים שבועית לסטורי, סעודות שבת ומרכז אימוני כוח וריצה.
    </div>
    <div class="brand-badges">
        <span class="badge-pill">💾 שמירת נתונים קבועה (SQLite)</span>
        <span class="badge-pill">📸 סורק AI חכם (Gemini Vision)</span>
        <span class="badge-pill">🛒 הזמנת קניות בלחיצה לסופר</span>
        <span class="badge-pill">📲 כרטיסיית סיכום שבועית לסטורי</span>
        <span class="badge-pill">🧘 סדרת חימום ומתיחות</span>
    </div>
</div>
""", unsafe_allow_html=True)

# באנר מוטיבציה מתחלף
motivation_html = """
<div style="
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border: 1px solid #38bdf8;
    border-radius: 14px;
    padding: 12px 20px;
    text-align: center;
    margin-bottom: 22px;
    box-shadow: 0 4px 15px rgba(56, 189, 248, 0.15);
">
    <span style="font-size: 1.2rem; margin-left: 8px;">🔥</span>
    <span id="mot-quote" style="
        font-family: 'Assistant', 'Rubik', sans-serif;
        font-size: 1.12rem;
        font-weight: 800;
        color: #38bdf8;
        transition: opacity 0.5s ease-in-out;
    ">המשכיות מנצחת כישרון בכל יום.</span>
</div>

<script>
const quotes = [
    "המשכיות מנצחת כישרון בכל יום. 🔥",
    "התוצאות שאתה רוצה מחר תלויות במה שתעשה היום. ⚡",
    "אל תוותר על מה שאתה הכי רוצה בשביל מה שבא לך עכשיו. 🏆",
    "משמעת עצמית זה לבחור בין מה שקל עכשיו למה שמשתלם אחר כך. 💪",
    "קילומטר אחד יותר, עוד סט אחד – שם קורה השינוי. 🏃",
    "ההבדל בין מטרה לחלום זה תוכנית עבודה מדויקת. 🎯"
];
let qIndex = 0;
const qElem = document.getElementById("mot-quote");

setInterval(() => {
    if (qElem) {
        qElem.style.opacity = 0;
        setTimeout(() => {
            qIndex = (qIndex + 1) % quotes.length;
            qElem.innerText = quotes[qIndex];
            qElem.style.opacity = 1;
        }, 500);
    }
}, 6000);
</script>
"""
components.html(motivation_html, height=75)

# הטאבים
tab_bmi, tab_nutrition, tab_ai_cam, tab_story, tab_warmup, tab_shabbat, tab_shopping, tab_workout = st.tabs([
    "📊 מחשבון מדדים ותפריט",
    "🥗 יומן ומעקב קלוריות חכם",
    "📸 סורק AI למנות ומוצרים",
    "📲 סיכום שבועי לסטורי",
    "🧘 חימום ומתיחות דינמי",
    "🕯️ מחשבון סעודות שבת",
    "🛒 רשימת קניות לסופר",
    "🏋️ מרכז אימונים וכוח"
])

# --- טאב 1: מחשבון מדדים ותפריט ---
with tab_bmi:
    st.subheader("📊 אבחון מדדים אישי ובניית תפריט מדויק")
    col1, col2, col3 = st.columns(3)
    with col1:
        weight = st.number_input("משקל (ב-ק״ג):", min_value=35.0, max_value=160.0, value=71.0, step=0.5)
        age = st.number_input("גיל:", min_value=12, max_value=80, value=17, step=1)
    with col2:
        height_cm = st.number_input("גובה (ב-ס״מ):", min_value=120, max_value=220, value=175, step=1)
        activity = st.selectbox("רמת פעילות גופנית:", [
            "יושבני (ללא אימונים)",
            "פעילות קלה (1–2 אימונים בשבוע)",
            "פעילות בינונית (3–4 אימונים בשבוע)",
            "פעילות גבוהה (5+ אימונים בשבוע / ספורטאי)"
        ])
    with col3:
        goal = st.selectbox("מטרת היעד:", [
            "חיטוב וירידה באחוזי שומן",
            "בניית מסת שריר נקייה (Lean Bulk)",
            "שיפור סיבולת וביצועים"
        ])
        diet_pref = st.selectbox("העדפת תזונה:", ["סטנדרט (כולל עוף ובקר)", "עשיר דגים ומוצרי חלב", "צמחוני"])

    if st.button("בנה תפריט תזונה מפורט ומותאם אישית 🎯"):
        height_m = height_cm / 100
        bmi_val = round(weight / (height_m ** 2), 1)
        act_factors = {"יושבני (ללא אימונים)": 1.2, "פעילות קלה (1–2 אימונים בשבוע)": 1.375, "פעילות בינונית (3–4 אימונים בשבוע)": 1.55, "פעילות גבוהה (5+ אימונים בשבוע / ספורטאי)": 1.725}
        factor = act_factors[activity]
        bmr = (10 * weight) + (6.25 * height_cm) - (5 * age) + 5
        tdee = int(bmr * factor)

        if "חיטוב" in goal:
            target_cal = int(tdee - (tdee * 0.18))
            protein_g = int(weight * 2.1)
            fat_g = int(weight * 0.8)
        elif "מסת שריר" in goal:
            target_cal = int(tdee + 350)
            protein_g = int(weight * 2.0)
            fat_g = int(weight * 1.0)
        else:
            target_cal = tdee
            protein_g = int(weight * 1.7)
            fat_g = int(weight * 0.9)

        carb_cals = target_cal - ((protein_g * 4) + (fat_g * 9))
        carb_g = max(int(carb_cals / 4), 80)

        st.session_state["user_target_cal"] = target_cal
        st.session_state["user_target_p"] = protein_g

        chicken_portion = int(((protein_g * 0.40) / 31.0) * 100)
        rice_portion = int(((carb_g * 0.40) / 28.0) * 100)

        st.success(f"מדד BMI: **{bmi_val}** | יעד יומי: **{target_cal} קק\"ל** | חלבון: **{protein_g} גרם** | פחמימות: **{carb_g} גרם** | שומן: **{fat_g} גרם**")

        menu_text = f"""תוכנית תזונה אישית - DaniFit Pro
נתונים: משקל {weight} ק"ג | גובה {height_cm} ס"מ | BMI: {bmi_val}
יעד קלורי: {target_cal} קק"ל | חלבון: {protein_g}g | פחמימה: {carb_g}g | שומן: {fat_g}g
• ארוחת בוקר: 2-3 ביצים, 2 פרוסות לחם מלא, כף טחינה, ירקות.
• ארוחת צהריים: {chicken_portion} גרם חזה עוף שקול מבושל + {rice_portion} גרם אורז בסמטי + סלט ושמן זית.
• ארוחת ביניים: יוגורט חלבון PRO 20g + פרי + 10 שקדים.
• ארוחת ערב: קופסת טונה במים / 180 גרם קוטג' 5% + 2 פרוסות לחם מלא + אבוקדו."""
        st.session_state["saved_menu_text"] = menu_text

    if "saved_menu_text" in st.session_state:
        st.text_area("📋 התוכנית שהופקה:", value=st.session_state["saved_menu_text"], height=200)

# --- טאב 2: יומן קלוריות חכם ---
with tab_nutrition:
    st.subheader("🥗 יומן מעקב קלוריות ומאקרו בזמן אמת (נשמר אוטומטית)")

    st.markdown('<div class="water-box">', unsafe_allow_html=True)
    w_col1, w_col2, w_col3, w_col4 = st.columns([3, 1.2, 1.2, 1])
    with w_col1:
        water_target = 3000
        water_progress = min(st.session_state.water_ml / water_target, 1.0)
        st.markdown(f"💧 **מעקב שתיית מים:** {st.session_state.water_ml} מ״ל מתוך {water_target} מ״ל")
        st.progress(water_progress)
    with w_col2:
        if st.button("🥤 +250 מ״ל", key="btn_w_250"):
            st.session_state.water_ml += 250
            save_today_data(st.session_state.water_ml, st.session_state.extra_burned_cals, st.session_state.logged_items)
            st.rerun()
    with w_col3:
        if st.button("🍶 +500 מ״ל", key="btn_w_500"):
            st.session_state.water_ml += 500
            save_today_data(st.session_state.water_ml, st.session_state.extra_burned_cals, st.session_state.logged_items)
            st.rerun()
    with w_col4:
        if st.button("🔄 אפס מים", key="btn_w_reset"):
            st.session_state.water_ml = 0
            save_today_data(st.session_state.water_ml, st.session_state.extra_burned_cals, st.session_state.logged_items)
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    base_cal_target = st.session_state.get("user_target_cal", 2200)
    user_p_target = st.session_state.get("user_target_p", 140)
    final_cal_target = base_cal_target + st.session_state.extra_burned_cals

    tab_add_quick, tab_add_custom = st.tabs(["⚡ הוספה מהירה ממאגר", "✏️ הוספה ידנית"])
    with tab_add_quick:
        qc_meal, qc1, qc2, qc3 = st.columns([2, 3, 2, 2])
        with qc_meal:
            meal_type = st.selectbox("ארוחה:", ["ארוחת בוקר", "ארוחת צהריים", "ארוחת ביניים", "ארוחת ערב"], key="q_meal")
        with qc1:
            selected_food = st.selectbox("בחר מאכל:", list(FOOD_DATABASE.keys()))
        with qc2:
            quantity = st.number_input(f"כמות ({FOOD_DATABASE[selected_food]['unit']}):", min_value=0.25, max_value=20.0, value=1.0, step=0.25)
        with qc3:
            st.write("")
            st.write("")
            if st.button("הוסף ליומן ➕", key="btn_quick_add"):
                item_data = FOOD_DATABASE[selected_food]
                st.session_state.logged_items.append({
                    "meal": meal_type,
                    "name": selected_food,
                    "qty": quantity,
                    "unit": item_data["unit"],
                    "cal": round(item_data["cal"] * quantity),
                    "p": round(item_data["p"] * quantity, 1),
                    "c": round(item_data["c"] * quantity, 1),
                    "f": round(item_data["f"] * quantity, 1)
                })
                save_today_data(st.session_state.water_ml, st.session_state.extra_burned_cals, st.session_state.logged_items)
                st.rerun()

    with tab_add_custom:
        cu_meal, cu1, cu2, cu3, cu4 = st.columns([2, 3, 2, 2, 2])
        with cu_meal:
            c_meal = st.selectbox("ארוחה:", ["ארוחת בוקר", "ארוחת צהריים", "ארוחת ביניים", "ארוחת ערב"], key="c_meal")
        with cu1:
            c_name = st.text_input("שם המאכל:", "שייק חלבון")
        with cu2:
            c_cal = st.number_input("קלוריות:", min_value=0, max_value=2000, value=180)
        with cu3:
            c_p = st.number_input("חלבון (גרם):", min_value=0.0, max_value=150.0, value=25.0, step=0.5)
        with cu4:
            st.write("")
            st.write("")
            if st.button("הוסף מאכל ידני ➕", key="btn_custom_add"):
                st.session_state.logged_items.append({
                    "meal": c_meal,
                    "name": c_name,
                    "qty": 1.0,
                    "unit": "מנה",
                    "cal": int(c_cal),
                    "p": float(c_p),
                    "c": 0.0,
                    "f": 0.0
                })
                save_today_data(st.session_state.water_ml, st.session_state.extra_burned_cals, st.session_state.logged_items)
                st.rerun()

    tot_cal = sum(x["cal"] for x in st.session_state.logged_items)
    tot_p = round(sum(x["p"] for x in st.session_state.logged_items), 1)
    tot_c = round(sum(x["c"] for x in st.session_state.logged_items), 1)
    tot_f = round(sum(x["f"] for x in st.session_state.logged_items), 1)
    remain_cal = final_cal_target - tot_cal
    remain_p = max(0.0, round(user_p_target - tot_p, 1))

    st.markdown("---")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("🔥 נצרכו היום", f"{tot_cal} קק\"ל")
    m2.metric("🎯 יעד יומי", f"{final_cal_target} קק\"ל")
    m3.metric("⚖️ נותר להיום", f"{remain_cal} קק\"ל", delta=remain_cal)
    m4.metric("🥩 חלבון שהושג", f"{tot_p} / {user_p_target}g")
    m5.metric("🍞 פחמימות ושומן", f"{tot_c}g פח' | {tot_f}g שומן")

    st.markdown("### 📋 פירוט ארוחות היום")
    if not st.session_state.logged_items:
        st.info("היומן ריק עדיין להיום. הוסף מאכלים למעלה או השתמש בסורק ה-AI!")
    else:
        for idx, item in enumerate(st.session_state.logged_items):
            c_info, c_del = st.columns([5, 1])
            with c_info:
                st.write(f"• **[{item['meal']}]** {item['name']} ({item['qty']} {item['unit']}) — **{item['cal']} קק\"ל** | חלבון: {item['p']}g | פחמימה: {item['c']}g | שומן: {item['f']}g")
            with c_del:
                if st.button("🗑️ מחק", key=f"del_item_{idx}"):
                    st.session_state.logged_items.pop(idx)
                    save_today_data(st.session_state.water_ml, st.session_state.extra_burned_cals, st.session_state.logged_items)
                    st.rerun()

    if remain_cal > 200 or remain_p > 15:
        st.markdown('<div class="suggest-box">', unsafe_allow_html=True)
        st.markdown(f"💡 **המלצת AI לסגירת הפינה היומית:** חסרים לך **{remain_p} גרם חלבון** ו-**{remain_cal} קלוריות**.")
        if remain_p > 20:
            st.markdown("- מומלץ: גביע יוגורט PRO (20g חלבון) או קופסת טונה במים עם ירקות.")
        else:
            st.markdown("- מומלץ: 150 גרם גבינת קוטג' 5% עם תפוח עץ.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- טאב 3: סורק AI אמיתי (Gemini Vision) ---
with tab_ai_cam:
    st.subheader("📸 סורק AI חכם לתזונה (Gemini Vision)")
    st.caption("צלם כל מוצר, משקה, תווית ערכים או צלחת אוכל, וה-AI יזהה ויחלץ את הערכים ישירות ליומן.")

    scan_mode = st.radio("בחר אופן צילום:", ["📷 צילום חי במצלמה", "📁 העלאת קובץ תמונה"], horizontal=True)
    uploaded_file = st.camera_input("כוון את המצלמה למנה או למוצר:") if scan_mode == "📷 צילום חי במצלמה" else st.file_uploader("בחר תמונה:", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        pil_img = Image.open(uploaded_file)
        st.image(pil_img, caption="תמונת המקור", width=320)

        if st.button("🔍 נתח מנה/מוצר עם AI עכשיו", type="primary"):
            api_key = st.secrets.get("GEMINI_API_KEY")
            if not api_key:
                st.error("לא הוגדר GEMINI_API_KEY בלשונית ה-Secrets ב-Streamlit Settings.")
            else:
                with st.spinner("ה-AI קורא את התווית ומנתח את הערכים..."):
                    try:
                        client = genai.Client(api_key=api_key)
                        prompt = """
                        אתה מומחה תזונה וסורק מזון חכם. נתח את התמונה המצורפת (מוצר עם תווית, בקבוק משקה, או צלחת אוכל).
                        זהה את שם הפריט במדויק וקרא או הערך את הערכים התזונתיים עבור המנה/הבקבוק כולו.
                        החזר אך ורק תשובת JSON בפורמט הבא ללא שום מילים או עיצוב נוסף:
                        {
                            "name": "שם המוצר או המאכל בעברית",
                            "cal": 140,
                            "p": 25.0,
                            "c": 5.0,
                            "f": 2.0
                        }
                        """
                        res = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=[prompt, pil_img]
                        )
                        cleaned = res.text.strip().replace("```json", "").replace("```", "").strip()
                        food_info = json.loads(cleaned)
                        st.session_state["scanned_ai_dish"] = food_info
                        st.success(f"זוהה בהצלחה: **{food_info['name']}**")
                    except Exception as err:
                        st.error(f"שגיאה בניתוח התמונה: {err}")

        if "scanned_ai_dish" in st.session_state:
            dish = st.session_state["scanned_ai_dish"]
            st.markdown(f"""
            <div class="card-box">
                <h4>🍽️ {dish['name']}</h4>
                <p><b>קלוריות:</b> {dish['cal']} קק"ל | <b>חלבון:</b> {dish['p']} גרם | <b>פחמימות:</b> {dish['c']} גרם | <b>שומן:</b> {dish['f']} גרם</p>
            </div>
            """, unsafe_allow_html=True)

            meal_choice = st.selectbox("לאיזו ארוחה להוסיף?", ["ארוחת צהריים", "ארוחת בוקר", "ארוחת ביניים", "ארוחת ערב"], key="ai_meal_choice")

            if st.button("➕ הוסף ישירות ליומן היומי שלי!", key="btn_confirm_ai_add"):
                st.session_state.logged_items.append({
                    "meal": meal_choice,
                    "name": dish["name"],
                    "qty": 1.0,
                    "unit": "מנה",
                    "cal": int(dish["cal"]),
                    "p": float(dish["p"]),
                    "c": float(dish["c"]),
                    "f": float(dish["f"])
                })
                save_today_data(st.session_state.water_ml, st.session_state.extra_burned_cals, st.session_state.logged_items)
                st.success(f"הפריט '{dish['name']}' נוסף בהצלחה ליומן!")
                time.sleep(1)
                st.rerun()

# --- טאב 4: כרטיסיית סטורי שבועית ---
with tab_story:
    st.subheader("📲 הפקת כרטיסיית הישגים שבועית לסטורי")
    st.caption("הפק תמונה מעוצבת לשיתוף באינסטגרם / וואטסאפ.")
    
    st.markdown("""
    <div class="story-card">
        <h2 style="color: #38bdf8; margin: 0; font-size: 2rem;">⚡ DANIFIT PRO</h2>
        <p style="color: #94a3b8; margin-top: 4px;">סיכום ביצועים שבועי</p>
        <hr style="border-color: #334155; margin: 20px 0;">
        <div style="font-size: 1.25rem; font-weight: 700; margin-bottom: 12px;">🔥 5 אימונים הושלמו בהצלחה</div>
        <div style="font-size: 1.25rem; font-weight: 700; margin-bottom: 12px;">🥩 100% עמידה ביעד החלבון השבועי</div>
        <div style="font-size: 1.25rem; font-weight: 700; margin-bottom: 12px;">💧 ממוצע 3.2 ליטר מים ביום</div>
        <div style="font-size: 1.25rem; font-weight: 700; margin-bottom: 16px;">🏆 שיא אישי חדש (PR) נשבר!</div>
        <div style="background: rgba(56, 189, 248, 0.15); border: 1px dashed #38bdf8; border-radius: 12px; padding: 10px; margin-top: 15px;">
            <b style="color: #38bdf8;">משמעת מנצחת הכל 🦾</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- טאב 5: חימום ומתיחות ---
with tab_warmup:
    st.subheader("🧘 סדרת חימום ומתיחות דינמיות לפני אימון")
    warmups = [
        ("סיבובי ידיים ומפרקים", "30 שניות קדימה ו-30 שניות אחורה"),
        ("סיבובי אגן ומותניים", "10 סיבובים לכל כיוון"),
        ("סמוך-קום קל / ג'אמפינג ג'קס", "45 שניות להעלאת דופק"),
        ("מתיחת שוקיים והמסטרינג", "30 שניות לכל רגל"),
        ("פתיחת בית חזה ומתיחת כתפיים", "30 שניות סטטיות")
    ]
    for ex_name, ex_desc in warmups:
        st.markdown(f"""
        <div class="card-box">
            <h4>🏃 {ex_name}</h4>
            <p style="color: #475569; margin: 0;"><b>הנחיות:</b> {ex_desc}</p>
        </div>
        """, unsafe_allow_html=True)

# --- טאב 6: מחשבון סעודות שבת ---
with tab_shabbat:
    st.subheader("🕯️ מחשבון שבת קודש חכם")
    st.caption("שמור על המאקרו והמשקל גם בארוחות השבת והחגים.")

    shab_food = st.selectbox("בחר מנת שבת:", list(SHABBAT_FOOD_DB.keys()))
    shab_qty = st.number_input("כמות מנות:", min_value=1.0, max_value=5.0, value=1.0, step=0.5)

    if st.button("חשב ערכי מנת שבת 🍷"):
        data = SHABBAT_FOOD_DB[shab_food]
        cal = int(data["cal"] * shab_qty)
        p = round(data["p"] * shab_qty, 1)
        c = round(data["c"] * shab_qty, 1)
        f = round(data["f"] * shab_qty, 1)
        st.info(f"ערכי המנה: **{cal} קק\"ל** | חלבון: **{p}g** | פחמימות: **{c}g** | שומן: **{f}g**")

# --- טאב 7: רשימת קניות לסופר ---
with tab_shopping:
    st.subheader("🛒 רשימת קניות חכמה והזמנה מהירה לסופר")
    st.caption("סמן מוצרים שחסרים לך והזמן אותם ישירות בלחיצה אחת לאתרי האונליין:")

    for idx, shop_item in enumerate(st.session_state.shopping_list):
        s_c1, s_c2, s_c3 = st.columns([4, 2, 2])
        with s_c1:
            st.session_state.shopping_list[idx]["checked"] = st.checkbox(shop_item["item"], value=shop_item["checked"], key=f"shop_chk_{idx}")
        with s_c2:
            shuf_url = f"https://www.shufersal.co.il/online/he/search?text={urllib.parse.quote(shop_item['search'])}"
            st.markdown(f'<a href="{shuf_url}" target="_blank" class="quick-shop-btn">חפש בשופרסל 🔍</a>', unsafe_allow_html=True)
        with s_c3:
            rami_url = f"https://www.rami-levy.co.il/he/online/search?q={urllib.parse.quote(shop_item['search'])}"
            st.markdown(f'<a href="{rami_url}" target="_blank" class="quick-shop-btn">רמי לוי 🛒</a>', unsafe_allow_html=True)

# --- טאב 8: מרכז אימונים וקיר שיאים (PR) ---
with tab_workout:
    st.subheader("🏋️ מרכז אימונים אישי וקיר שיאים (נשמר ב-SQLite)")

    with st.expander("➕ הוסף שיא אישי חדש (PR)", expanded=True):
        p_c1, p_c2, p_c3, p_c4 = st.columns(4)
        with p_c1:
            pr_ex = st.selectbox("תרגיל:", ["בנץ' פרס (לחיצת חזה)", "סקוואט", "דדליפט", "מתח עם משקל", "מקבילים עם משקל", "ריצת 5 ק\"מ (דקות)"])
        with p_c2:
            pr_w = st.number_input("משקל (ק\"ג) / זמן:", min_value=0.0, max_value=400.0, value=60.0, step=2.5)
        with p_c3:
            pr_r = st.number_input("חזרות:", min_value=1, max_value=50, value=5, step=1)
        with p_c4:
            st.write("")
            st.write("")
            if st.button("רשום שיא! 🏆"):
                add_pr(pr_ex, pr_w, pr_r)
                st.success("השיא נשמר בהצלחה במסד הנתונים!")
                st.rerun()

    current_prs = load_prs()
    if not current_prs:
        st.info("עדיין לא נרשמו שיאים. רשום את השיא הראשון שלך למעלה!")
    else:
        for pr in current_prs:
            pr_box_c1, pr_box_c2 = st.columns([5, 1])
            with pr_box_c1:
                st.markdown(f"""
                <div class="card-box" style="margin-bottom: 10px; padding: 14px;">
                    <b>🏅 {pr['exercise']}</b> — {pr['weight']} ק"ג ל-{pr['reps']} חזרות <span style="color: #64748b; font-size: 0.85rem;">({pr['date']})</span>
                </div>
                """, unsafe_allow_html=True)
            with pr_box_c2:
                if st.button("🗑️", key=f"del_pr_{pr['id']}"):
                    delete_pr(pr['id'])
                    st.rerun()
