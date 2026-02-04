import datetime
import requests
import streamlit as st
import holidays
from streamlit_autorefresh import st_autorefresh

# =========================
# 기본 설정
# =========================
st.set_page_config(
    page_title="MISHARP Creative Dashboard",
    page_icon="🟢",
    layout="wide",
)

BG_COLOR = "#0A3B1C"   # 딥그린 (고급/부드러운 톤)
TEXT_MAIN = "#EAF6EE"
TEXT_SUB = "rgba(234,246,238,0.75)"
CARD_BG = "rgba(255,255,255,0.05)"

TOOLS = [
    ("상세페이지 생성기", "https://misharp-image-maker-v3.streamlit.app/"),
    ("썸네일 생성기", "https://misharp-thumbnail-maker-2026.streamlit.app/"),
    ("GIF 생성기", "https://misharp-gif-maker.streamlit.app/"),

    ("이미지 자르기 툴", "https://misharp-image-crop-v1.streamlit.app/"),
    ("카페24 어드민", "https://eclogin.cafe24.com/Shop/"),
    ("미샵 홈페이지", "https://misharp.co.kr/"),

    ("미샵 스마트스토어", "https://smartstore.naver.com/misharp2006"),
    ("셀메이트", "https://misharp.sellmate.co.kr/login/login_prototype.asp"),
    ("스마트비즈", "https://smart-biz.co.kr/main.php"),

    ("크리마", "https://admin.cre.ma/v2/login"),
    ("찰나", "https://charlla.io/"),
    ("미샵 네이버 블로그", "https://blog.naver.com/misharp2006"),

    ("미샵 티스토리", "https://misharp2006.tistory.com/"),
    ("핀터레스트", "https://kr.pinterest.com/"),
    ("URL 단축", "https://shor.kr/"),

    ("ChatGPT", "https://chatgpt.com/"),
    ("Gemini", "https://gemini.google.com/app"),
    ("네이버 실시간 패션키워드", "https://datalab.naver.com/shoppingInsight/sCategory.naver"),

    ("네이버 쇼핑 패션", "https://shopping.naver.com/window/main/fashion-group"),
    ("네이버 홈", "https://www.naver.com/"),
    ("다음 홈", "https://www.daum.net/"),

    ("구글 홈", "https://www.google.com/"),
]

# =========================
# 스타일
# =========================
st.markdown(
    f"""
    <style>
      .stApp {{
        background: {BG_COLOR};
      }}
      .wrap {{
        max-width: 1200px;
        margin: 0 auto;
      }}
      .title {{
        color: {TEXT_MAIN};
        font-size: 32px;
        font-weight: 650;
        letter-spacing: 0.4px;
        margin-bottom: 18px;
      }}

      .info-card {{
        background: {CARD_BG};
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 16px;
        padding: 16px 18px;
      }}
      .info-label {{
        color: {TEXT_SUB};
        font-size: 13px;
        margin-bottom: 6px;
      }}
      .info-value {{
        color: {TEXT_MAIN};
        font-size: 17px;
        font-weight: 600;
      }}

      a.tool-btn {{
        display: block;
        width: 100%;
        text-decoration: none !important;
        color: {TEXT_MAIN} !important;
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.28);
        border-radius: 18px;
        padding: 14px 10px;
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 0.2px;
        text-align: center;
        transition: all .18s ease;
      }}
      a.tool-btn:hover {{
        background: rgba(255,255,255,0.08);
        border-color: rgba(255,255,255,0.55);
        transform: translateY(-2px);
      }}

      .footer {{
        margin-top: 32px;
        padding-top: 14px;
        border-top: 1px solid rgba(255,255,255,0.14);
        text-align: center;
        font-size: 12px;
        color: {TEXT_SUB};
      }}

      .block-container {{
        padding-top: 28px;
        padding-bottom: 20px;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# 오늘의 정보
# =========================
def today_event(date_obj):
    kr = holidays.KR()
    if date_obj in kr:
        return str(kr.get(date_obj))

    custom = {
        (2, 14): "발렌타인데이",
        (3, 14): "화이트데이",
        (5, 8): "어버이날",
        (10, 1): "국군의 날",
        (11, 11): "빼빼로데이",
        (12, 31): "연말",
    }
    return custom.get((date_obj.month, date_obj.day), "특별한 일정 없음")

@st.cache_data(ttl=600)
def get_weather():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=37.5665&longitude=126.9780"
        "&daily=weathercode,temperature_2m_max,temperature_2m_min"
        "&timezone=Asia%2FSeoul"
    )
    data = requests.get(url, timeout=10).json()
    tmin = round(data["daily"]["temperature_2m_min"][0])
    tmax = round(data["daily"]["temperature_2m_max"][0])
    return f"서울·경기  |  최저 {tmin}° / 최고 {tmax}°"

st_autorefresh(interval=1000, key="clock")

now = datetime.datetime.now()

st.markdown('<div class="wrap">', unsafe_allow_html=True)
st.markdown('<div class="title">MISHARP Creative Dashboard</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3, gap="large")

with c1:
    st.markdown(
        f"""
        <div class="info-card">
          <div class="info-label">실시간 날짜 / 시간</div>
          <div class="info-value">{now.strftime("%Y-%m-%d %H:%M:%S")}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f"""
        <div class="info-card">
          <div class="info-label">금일 이벤트</div>
          <div class="info-value">{today_event(now.date())}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        f"""
        <div class="info-card">
          <div class="info-label">오늘의 날씨</div>
          <div class="info-value">{get_weather()}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

cols = st.columns(3, gap="large")
for i, (name, link) in enumerate(TOOLS):
    with cols[i % 3]:
        st.markdown(
            f'<a class="tool-btn" href="{link}" target="_blank">{name}</a>',
            unsafe_allow_html=True,
        )
    if i % 3 == 2:
        st.write("")

st.markdown(
    """
    <div class="footer">
      미샵컴퍼니 직원 전용 · 제작 미샵컴퍼니 · 외부 유출 금함
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)
