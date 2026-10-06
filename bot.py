import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="DAN FIT | מרכז הכושר והתזונה",
    page_icon="⚡",
    layout="wide"
)

# פונקציית הדפסה חכמה שפותחת את חלון ההדפסה של הדפדפן
def print_button(text_content: str, title: str, button_id: str):
    html_safe_text = text_content.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
    print_html = f"""
    <button onclick="printDoc_{button_id}()" style="
        width: 100%;
        background-color: #0f172a;
        color: #ffffff;
        border: none;
        border-radius: 12px;
        padding: 12px 20px;
        font-weight: 800;
        font-size: 1rem;
        cursor: pointer;
        font-family: inherit;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.2);
        transition: 0.2s;
    ">🖨️ הדפס / שמור כ-PDF</button>

    <script>
    function printDoc_{button_id}() {{
        var content = `{html_safe_text}`;
        var win = window.open('', '', 'height=700,width=900');
        win.document.write('<html><head><title>{title}</title>');
        win.document.write('<style>');
        win.document.write('body {{ font-family: Arial, sans-serif; direction: rtl; text-align: right; padding: 30px; color: #111; line-height: 1.6; }}');
        win.document.write('pre {{ white-space: pre-wrap; font-family: inherit; font-size: 14px; background: #f8fafc; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; }}');
        win.document.write('</style></head><body>');
        win.document.write('<h2 style="color: #2563eb; text-align: center; border-bottom: 2px solid #2563eb; padding-bottom: 10px;">{title}</h2>');
        win.document.write('<pre>' + content + '</pre>');
        win.document.write('</body></html>');
        win.document.close();
        win.focus();
        setTimeout(function() {{
            win.print();
            win.close();
        }}, 400);
    }}
    </script>
    """
    components.html(print_html, height=55)

# עיצוב בהיר ונקי
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

    .brand-header {
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        padding: 30px 24px 24px 24px;
        border-radius: 18px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
        text-align: center;
        margin-bottom: 25px;
    }
    
    .brand-title {
        font-family: 'Rubik', sans-serif;
        font-size: 2.8rem;
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
        max-width: 780px;
        margin: 12px auto 16px auto;
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
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.88rem;
        font-weight: 700;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }

    h1, h2, h3, .stSubheader {
        color: #0f172a !important;
        font-weight: 800 !important;
        border-bottom: 3px solid #2563eb;
        padding-bottom: 8px;
        margin-top: 20px !important;
        margin-bottom: 18px !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: #ffffff;
        padding: 8px 12px;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
    }

    .stTabs [data-baseweb="tab"] {
        color: #64748b !important;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 700;
        font-size: 1.05rem;
    }

    .stTabs [aria-selected="true"] {
        background-color: #2563eb !important;
        color: #ffffff !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.25);
    }

    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%);
        color: #ffffff !important;
        border: none;
        border-radius: 12px;
        padding: 14px 24px;
        font-size: 1.1rem;
        font-weight: 700;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.25);
    }

    .stDownloadButton > button {
        width: 100%;
        background-color: #ffffff !important;
        border: 2px solid #2563eb !important;
        color: #2563eb !important;
        border-radius: 12px;
        padding: 12px 20px;
        font-weight: 800;
        font-size: 1rem;
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

# מאגר מזונות
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

# כותרת מותג עליונה כולל תיאור מפורט
st.markdown("""
<div class="brand-header">
    <div class="brand-title">⚡ <span>DAN</span> FIT</div>
    <div class="brand-subtitle">הפלטפורמה החכמה של דן לתזונה, חיטוב וכושר שיא</div>
    <div class="brand-description">
        מערכת אישית ומתקדמת לניהול אורח חיים ספורטיבי: חישוב תפריטי תזונה מותאמים אישית ברמת הגרם,
        מעקב קלוריות וחלבון בזמן אמת עם יעדים יומיים, ובניית תוכניות ריצה וסיבולת לפי קצבים מדויקים.
    </div>
    <div class="brand-badges">
        <span class="badge-pill">🎯 תפריטי גרמים אישיים</span>
        <span class="badge-pill">🥗 מעקב קלוריות וחלבון</span>
        <span class="badge-pill">🏃 מאמן ריצה שבועי</span>
        <span class="badge-pill">🖨️ הדפסה ושמירה כ-PDF</span>
        <span class="badge-pill">⚡ 100% פעילות חלקה וללא תקלות</span>
    </div>
</div>
""", unsafe_allow_html=True)

tab_bmi, tab_nutrition, tab_running = st.tabs([
    "📊 מחשבון מדדים ותפריט מותאם",
    "🥗 יומן ומעקב קלוריות חכם",
    "🏃 מאמן ריצה מותאם אישית"
])

# --- חדר 1: מחשבון מדדים ותפריט מותאם ---
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
            "פעילות קלה (1-2 אימונים בשבוע)",
            "פעילות בינונית (3-4 אימונים בשבוע)",
            "פעילות גבוהה (5+ אימונים / ספורטאי)"
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

        act_factors = {
            "יושבני (ללא אימונים)": 1.2,
            "פעילות קלה (1-2 אימונים בשבוע)": 1.375,
            "פעילות בינונית (3-4 אימונים בשבוע)": 1.55,
            "פעילות גבוהה (5+ אימונים / ספורטאי)": 1.725
        }
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

        lunch_protein_req = protein_g * 0.40
        chicken_portion = int((lunch_protein_req / 31.0) * 100)
        fish_portion = int(chicken_portion * 1.15)
        
        lunch_carbs = carb_g * 0.40
        rice_portion = int((lunch_carbs / 28.0) * 100)
        sweet_potato = int(rice_portion * 1.2)

        oats_breakfast = int(carb_g * 0.25 * (40 / 27))
        egg_count = 3 if weight >= 68 else 2
        bread_breakfast = 2 if carb_g < 200 else 3
        oil_spoons = 1 if fat_g < 60 else 2

        st.success(f"מדד ה-BMI: **{bmi_val}** | קלוריות ליעד: **{target_cal} קק\"ל** | חלבון: **{protein_g} גרם** | פחמימות: **{carb_g} גרם** | שומן: **{fat_g} גרם**")

        menu_text = f"""==================================================
        תוכנית תזונה אישית - DAN FIT
==================================================
נתוני מתאמן: משקל {weight} ק"ג | גובה {height_cm} ס"מ | BMI: {bmi_val}
יעד: {goal} | רמת פעילות: {activity}
יעדים יומיים: {target_cal} קק"ל | {protein_g} גרם חלבון | {carb_g} גרם פחמימה | {fat_g} גרם שומן
--------------------------------------------------

ארוחה 1: בוקר ומטבוליזם (07:00-09:00)
-------------------------------------
• {egg_count} ביצים שלמות + כף גבינה לבנה 5%
• {bread_breakfast} פרוסות לחם מלא קל (או {oats_breakfast} גרם שיבולת שועל)
• כף טחינה גולמית משומשום מלא (15 גרם)
• ירקות חופשי

ארוחה 2: צהריים עיקרית (13:00-14:30)
-------------------------------------
• חלבון: {chicken_portion} גרם חזה עוף שקול לאחר בישול (חלופה: {fish_portion} גרם פילה דג בתנור)
• פחמימה: {rice_portion} גרם אורז בסמטי מבושל (חלופה: {sweet_potato} גרם בטטה אפויה)
• סלט ירקות קצוץ גדול + {oil_spoons} כפית שמן זית כתית מעולה

ארוחה 3: ביניים / תדלוק (16:30-17:30)
-------------------------------------
• 1 גביע יוגורט מועשר בחלבון (PRO / GO עם 20 גרם חלבון)
• פרי בינוני (בננה או תפוח)
• 10-12 שקדים טבעיים

ארוחה 4: ערב קלה והתאוששות (20:00-21:30)
---------------------------------------
• 1 קופסת טונה במים מסוננת או 180 גרם גבינת קוטג' 5%
• 2 פרוסות לחם מלא
• 1/4 אבוקדו בינוני
• סלט ירקות עשיר

דגש נוזלים: שתה לפחות {round(weight * 0.038, 1)} ליטר מים ביום!
=================================================="""
        
        st.session_state["saved_menu_text"] = menu_text
        st.session_state["saved_menu_weight"] = weight

    if "saved_menu_text" in st.session_state:
        st.text_area("📋 התוכנית שהופקה:", value=st.session_state["saved_menu_text"], height=320)
        c_dl, c_pr = st.columns(2)
        with c_dl:
            st.download_button(
                label="📥 שמור כקובץ טקסט (TXT)",
                data=st.session_state["saved_menu_text"],
                file_name=f"DAN_FIT_Nutrition_{st.session_state['saved_menu_weight']}kg.txt",
                mime="text/plain"
            )
        with c_pr:
            print_button(st.session_state["saved_menu_text"], "תוכנית תזונה אישית - DAN FIT", "menu")

# --- חדר 2: יומן ומעקב קלוריות חכם ---
with tab_nutrition:
    st.subheader("🥗 יומן מעקב קלוריות וחלבון בזמן אמת")
    
    user_cal_target = st.session_state.get("user_target_cal", 2200)
    user_p_target = st.session_state.get("user_target_p", 140)

    st.write(f"היעדים היומיים שלך: **{user_cal_target} קק\"ל** | **{user_p_target} גרם חלבון**")

    if "logged_items" not in st.session_state:
        st.session_state.logged_items = []

    tab_add_quick, tab_add_custom = st.tabs(["⚡ הוספה מהירה ממאגר המזונות", "✏️ הוספת מאכל אישי ידנית"])

    with tab_add_quick:
        qc1, qc2, qc3 = st.columns([3, 2, 2])
        with qc1:
            selected_food = st.selectbox("בחר מאכל:", list(FOOD_DATABASE.keys()))
        with qc2:
            unit_info = FOOD_DATABASE[selected_food]["unit"]
            quantity = st.number_input(f"כמות ({unit_info}):", min_value=0.25, max_value=20.0, value=1.0, step=0.25)
        with qc3:
            st.write("")
            st.write("")
            if st.button("הוסף ליומן ➕", key="btn_quick_add"):
                item_data = FOOD_DATABASE[selected_food]
                st.session_state.logged_items.append({
                    "name": selected_food,
                    "qty": quantity,
                    "unit": unit_info,
                    "cal": round(item_data["cal"] * quantity),
                    "p": round(item_data["p"] * quantity, 1),
                    "c": round(item_data["c"] * quantity, 1),
                    "f": round(item_data["f"] * quantity, 1)
                })
                st.rerun()

    with tab_add_custom:
        cu1, cu2, cu3, cu4 = st.columns(4)
        with cu1:
            c_name = st.text_input("שם המאכל:", "שייק חלבון")
        with cu2:
            c_cal = st.number_input("קלוריות (קק\"ל):", min_value=0, max_value=2000, value=180)
        with cu3:
            c_p = st.number_input("חלבון (גרם):", min_value=0.0, max_value=150.0, value=25.0, step=0.5)
        with cu4:
            st.write("")
            st.write("")
            if st.button("הוסף מאכל ידני ➕", key="btn_custom_add"):
                st.session_state.logged_items.append({
                    "name": c_name,
                    "qty": 1.0,
                    "unit": "מנה",
                    "cal": int(c_cal),
                    "p": float(c_p),
                    "c": 0.0,
                    "f": 0.0
                })
                st.rerun()

    tot_cal = sum(x["cal"] for x in st.session_state.logged_items)
    tot_p = round(sum(x["p"] for x in st.session_state.logged_items), 1)
    tot_c = round(sum(x["c"] for x in st.session_state.logged_items), 1)
    tot_f = round(sum(x["f"] for x in st.session_state.logged_items), 1)

    rem_cal = user_cal_target - tot_cal
    rem_p = round(user_p_target - tot_p, 1)

    st.write("---")
    st.write("### 📊 התקדמות יומית לקראת היעד:")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        cal_pct = min(max(tot_cal / user_cal_target, 0.0), 1.0)
        st.write(f"**קלוריות:** {tot_cal} מתוך {user_cal_target} קק\"ל")
        st.progress(cal_pct)
    with col_p2:
        prot_pct = min(max(tot_p / user_p_target, 0.0), 1.0)
        st.write(f"**חלבון:** {tot_p} מתוך {user_p_target} גרם")
        st.progress(prot_pct)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("סך קלוריות", f"{tot_cal} קק\"ל", delta=f"{rem_cal} ליעד")
    m2.metric("סך חלבון", f"{tot_p} גרם", delta=f"{rem_p} ליעד")
    m3.metric("סך פחמימות", f"{tot_c} גרם")
    m4.metric("סך שומן", f"{tot_f} גרם")

    if st.session_state.logged_items:
        st.write("### 📝 פירוט המאכלים שנאכלו היום:")
        for idx, item in enumerate(st.session_state.logged_items):
            c_txt, c_del = st.columns([5, 1])
            with c_txt:
                st.write(f"• **{item['name']}** ({item['qty']} {item['unit']}): **{item['cal']} קק\"ל** | חלבון: {item['p']}g")
            with c_del:
                if st.button("❌ מחק", key=f"del_{idx}"):
                    st.session_state.logged_items.pop(idx)
                    st.rerun()

        log_summary = f"""==================================================
        סיכום יומן תזונה יומי - DAN FIT
==================================================
סך קלוריות: {tot_cal} קק"ל
חלבון כולל: {tot_p} גרם
פחמימות כולל: {tot_c} גרם
שומן כולל: {tot_f} גרם
--------------------------------------------------
פירוט המאכלים:
""" + "\n".join([f"• {x['name']} ({x['qty']} {x['unit']}): {x['cal']} קק\"ל | חלבון: {x['p']}g" for x in st.session_state.logged_items])

        col_b1, col_b2, col_b3 = st.columns(3)
        with col_b1:
            if st.button("נקה יומן 🔄"):
                st.session_state.logged_items = []
                st.rerun()
        with col_b2:
            st.download_button("📥 שמור יומן (TXT)", data=log_summary, file_name="DAN_FIT_daily_log.txt")
        with col_b3:
            print_button(log_summary, "סיכום יומן תזונה יומי - DAN FIT", "log")

# --- חדר 3: מאמן ריצה מותאם אישית ---
with tab_running:
    st.subheader("🏃 מאמן ריצה וסיבולת אישי")
    
    r_col1, r_col2, r_col3 = st.columns(3)
    with r_col1:
        run_weight = st.number_input("משקל רץ (ק״ג):", min_value=40.0, max_value=150.0, value=weight, step=0.5, key="run_w")
        run_exp = st.selectbox("ניסיון ריצה נוכחי:", [
            "מתחיל מוחלט (לא רץ בכלל / מתנשף מהר)",
            "מתחיל מתקדם (מצליח לרוץ 1-2 ק״מ ברצף)",
            "רץ בינוני (רץ 3-5 ק״מ קבוע)",
            "מתקדם (רץ מעל 5 ק״מ בקצב טוב)"
        ])
    with r_col2:
        run_goal = st.selectbox("מטרת אימוני הריצה:", [
            "לרוץ 20 דקות רצוף ללא עצירה",
            "ריצת 3 ק״מ רציפה בקצב נוח",
            "ריצת 5 ק״מ בפחות מ-25-28 דקות",
            "שריפת שומן ושיפור סיבולת לב-ריאה (אינטרוולים)"
        ])
        days_per_week = st.select_slider("כמה ימי אימון ריצה נוחים לך בשבוע?", options=[2, 3, 4], value=3)
    with r_col3:
        target_pace_pref = st.selectbox("סוג אימון מועדף:", [
            "ריצות בוקר קלילות (לפני לימודים/עבודה)",
            "אימוני ערב עם דגש שריפת קלוריות",
            "משולב חיזוק כוח רגליים וליבה"
        ])

    if st.button("בנה לי תוכנית ריצה אישית שבועית 🚀"):
        if "מתחיל מוחלט" in run_exp:
            easy_pace = "07:30–08:30"
            interval_pace = "06:45–07:15"
            est_burn = int(run_weight * 3.5)
        elif "מתחיל מתקדם" in run_exp:
            easy_pace = "06:45–07:15"
            interval_pace = "06:00–06:30"
            est_burn = int(run_weight * 4.5)
        elif "בינוני" in run_exp:
            easy_pace = "05:45–06:15"
            interval_pace = "05:00–05:30"
            est_burn = int(run_weight * 5.5)
        else:
            easy_pace = "04:50–05:20"
            interval_pace = "04:15–04:45"
            est_burn = int(run_weight * 6.5)

        st.success(f"התוכנית מוכנה | קצב קל מומלץ: **{easy_pace} דקות לק״מ** | שריפה משוערת: **~{est_burn} קלוריות לאימון**")

        if days_per_week == 2:
            sessions = f"""• אימון 1: חימום 5 דקות הליכה | 20-25 דקות בקצב קל ({easy_pace}) או דקה ריצה + דקה הליכה | 5 דקות שחרור.
• אימון 2: חימום 5 דקות | ריצת נפח של 3-4 ק"מ בקצב איטי | 3 סטים של 15 סקוואטים במשקל גוף."""
        elif days_per_week == 3:
            sessions = f"""• אימון 1 (נפח קל): 25 דקות ריצה קלה בקצב {easy_pace} דק'/ק"מ | 5 דק' שחרור.
• אימון 2 (אינטרוולים): 1 ק"מ חימום | 5 סטים של 400 מטר מהיר ({interval_pace}) + 90 שניות הליכה | שחרור.
• אימון 3 (סופ"ש ארוך): ריצה מתונה של 4-5 ק"מ בקצב נוח | תרגילי מתיחות."""
        else:
            sessions = f"""• אימון 1: 3-4 ק"מ ריצה רגועה בקצב {easy_pace}.
• אימון 2: 6 סטים של 400 מטר מהיר ({interval_pace}) עם 75 שניות הליכה בין סט לסט.
• אימון 3: ריצת טמפו של 3.5 ק"מ בקצב מאתגר.
• אימון 4: ריצת נפח של 5-6 ק"מ בקצב איטי לבניית סיבולת."""

        run_output = f"""==================================================
        תוכנית ריצה שבועית - DAN FIT
==================================================
רץ: משקל {run_weight} ק"ג | רמה: {run_exp}
יעד: {run_goal} | תדירות: {days_per_week} אימונים בשבוע
קצב אירובי מומלץ: {easy_pace} דק'/ק"מ
שריפה ממוצעת לאימון: ~{est_burn} קלוריות
--------------------------------------------------
מערך האימונים השבועי:
{sessions}
--------------------------------------------------
טיפ זהב: שמור על נחיתה במרכז כף הרגל (ולא על העקב) למניעת כאבי ברכיים!
=================================================="""

        st.session_state["saved_run_output"] = run_output
        st.session_state["saved_days_per_week"] = days_per_week

    if "saved_run_output" in st.session_state:
        st.text_area("🏃 התוכנית שהופקה:", value=st.session_state["saved_run_output"], height=280)
        c_rdl, c_rpr = st.columns(2)
        with c_rdl:
            st.download_button(
                label="📥 שמור כקובץ טקסט (TXT)",
                data=st.session_state["saved_run_output"],
                file_name=f"DAN_FIT_Running_{st.session_state['saved_days_per_week']}days.txt",
                mime="text/plain"
            )
        with c_rpr:
            print_button(st.session_state["saved_run_output"], "תוכנית ריצה שבועית - DAN FIT", "running")