import datetime
from datetime import timezone, timedelta
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

# =========================
# 한국시간(KST)
# =========================
KST = timezone(timedelta(hours=9))

# =========================
# 디자인 톤
# =========================
BG_COLOR = "#0A3B1C"
TEXT_MAIN = "#EAF6EE"
TEXT_SUB = "rgba(234,246,238,0.75)"
CARD_BG = "rgba(255,255,255,0.05)"
DIVIDER_COLOR = "rgba(255,255,255,0.22)"

# =========================
# 레이아웃 정의
# =========================
LAYOUT = [
    # 생성기
    [
        ("상세페이지 생성기", "https://misharp-image-maker-v3.streamlit.app/"),
        ("GIF 생성기", "https://misharp-gif-maker.streamlit.app/"),
        ("썸네일 생성기", "https://misharp-thumbnail-maker-2026.streamlit.app/"),
    ],
    [
        ("이미지 자르기 툴", "https://misharp-image-crop-v1.streamlit.app/"),
        ("블로그 생성기", "https://ms-blog-maker-v1.streamlit.app/"),
        ("", ""),
    ],
    "DIVIDER",

    # 운영
    [
        ("카페24 어드민", "https://eclogin.cafe24.com/Shop/"),
        ("미샵 홈페이지", "https://misharp.co.kr/"),
        ("미샵 스마트 스토어", "https://smartstore.naver.com/misharp2006"),
    ],
    [
        ("셀메이트", "https://misharp.sellmate.co.kr/login/login_prototype.asp"),
        ("스마트비즈", "https://smart-biz.co.kr/main.php"),
        ("크리마", "https://admin.cre.ma/v2/login"),
    ],
    [
        ("찰나", "https://charlla.io/"),
        ("인포크 링크", "https://link.inpock.co.kr/user/login"),
        ("URL 단축", "https://shor.kr/"),
    ],
    "DIVIDER",

    # 블로그
    [
        ("미샵 네이버 블로그", "https://blog.naver.com/misharp2006"),
        ("미샵 티스토리", "https://misharp2006.tistory.com/"),
        ("구글 블로거", "https://www.blogger.com/"),
    ],
    "DIVIDER",

    # 인사이트
    [
        ("핀터레스트", "https://kr.pinterest.com/"),
        ("네이버 실시간 패션키워드", "https://datalab.naver.com/shoppingInsight/sCategory.naver"),
        ("네이버 쇼핑 패션", "https://shopping.naver.com/window/main/fashion-group"),
    ],
    "DIVIDER",

    # AI
    [
        ("ChatGPT", "https://chatgpt.com/"),
        ("제미나이", "https://gemini.google.com/app"),
        ("클로드 AI", "https://claude.ai/login?returnTo=%2F%3F"),
    ],

    # 홈
    [
        ("네이버 홈", "https://www.naver.com/"),
        ("다음 홈", "https://www.daum.net/"),
        ("구글 홈", "https://www.google.com/"),
    ],
]

# =========================
# CSS (여백 통일 핵심)
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
        margin-bottom: 20px;
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
        color: {TEXT_MAIN} !important;
        text-decoration: none !important;
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.28);
        border-radius: 18px;
        padding: 14px 10px;
        font-size: 14px;
        font-weight: 600;
        text-align: center;
        transition: all .18s ease;
      }}

      a.tool-btn:hover {{
        background: rgba(255,255,255,0.08);
        border-color: rgba(255,255,255,0.55);
        transform: translateY(-2px);
      }}

      /* 🔥 핵심: 구분선 여백 완전 통일 */
      .divider {{
        height: 1px;
        background: {DIVIDER_COLOR};
        margin: 28px 0 28px 0; /* 위/아래 동일 + 넉넉 */
        border-radius: 999px;
      }}

      .footer {{
        margin-top: 36px;
        padding-top: 14px;
        border-top: 1px solid rgba(255,255,255,0.14);
        text-align: center;
        font-size: 12px;
        color: {TEXT_SUB};
      }}

      /* Streamlit 기본 여백 제거 */
      .block-container {{
        padding-top: 28px;
        padding-bottom: 20px;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# 이벤트 / 날씨
# =========================
def today_event(d):
    kr = holidays.KR()
    return str(kr.get(d)) if d in kr else "특별한 일정 없음"

@st.cache_data(ttl=600)
def get_weather():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=37.5665&longitude=126.9780"
        "&daily=weathercode,temperature_2m_max,temperature_2m_min"
        "&timezone=Asia%2FSeoul"
    )
    data = requests.get(url, timeout=10).json()
    code = int(data["daily"]["weathercode"][0])
    tmin = round(data["daily"]["temperature_2m_min"][0])
    tmax = round(data["daily"]["temperature_2m_max"][0])

    def code_to_text(c):
        return (
            "맑음" if c == 0 else
            "흐림" if c in (1,2,3) else
            "비" if c in (61,63,65) else
            "눈" if c in (71,73,75) else
            "변동"
        )

    return f"서울·경기 {code_to_text(code)} | 최저 {tmin}° / 최고 {tmax}°"

# =========================
# 화면 렌더
# =========================
st_autorefresh(interval=1000, key="clock")
now = datetime.datetime.now(KST)

st.markdown('<div class="wrap">', unsafe_allow_html=True)
st.markdown('<div class="title">MISHARP Creative Dashboard</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3, gap="large")

with c1:
    st.markdown(
        f"<div class='info-card'><div class='info-label'>실시간 날짜 / 시간</div><div class='info-value'>{now:%Y-%m-%d %H:%M:%S}</div></div>",
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f"<div class='info-card'><div class='info-label'>금일 이벤트</div><div class='info-value'>{today_event(now.date())}</div></div>",
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        f"<div class='info-card'><div class='info-label'>오늘의 날씨</div><div class='info-value'>{get_weather()}</div></div>",
        unsafe_allow_html=True,
    )

# =========================
# 버튼 + 구분선 렌더
# =========================
for item in LAYOUT:
    if item == "DIVIDER":
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        continue

    cols = st.columns(3, gap="large")
    for col, (name, link) in zip(cols, item):
        with col:
            if name:
                st.markdown(
                    f"<a class='tool-btn' href='{link}' target='_blank'>{name}</a>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown("<div style='height:52px;'></div>", unsafe_allow_html=True)

st.markdown(
    "<div class='footer'>미샵컴퍼니 직원 전용 · 제작 미샵컴퍼니 · 외부 유출 금함</div>",
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)
