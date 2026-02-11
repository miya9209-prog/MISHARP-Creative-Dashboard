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
# 한국시간(KST) 고정
# =========================
KST = timezone(timedelta(hours=9))

# =========================
# 디자인 톤
# =========================
BG_COLOR = "#0A3B1C"
TEXT_MAIN = "#EAF6EE"
TEXT_SUB = "rgba(234,246,238,0.75)"
CARD_BG = "rgba(255,255,255,0.05)"
DIVIDER = "rgba(255,255,255,0.20)"  # 구분선(얇은 흰색)

# =========================
# 섹션/그리드
# - "DIVIDER"는 구분선 렌더
# - 빈칸은 ("","") 유지
# =========================
LAYOUT = [
    # 1) 생성기 섹션
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

    # 2) 운영 섹션
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
        ("URL 단축", "https://shor.kr/"),  # ✅ 인포크 링크 옆으로 이동
    ],
    "DIVIDER",

    # 3) 블로그 섹션
    [
        ("미샵 네이버 블로그", "https://blog.naver.com/misharp2006"),
        ("미샵 티스토리", "https://misharp2006.tistory.com/"),
        ("구글 블로거", "https://www.blogger.com/blog/posts/1654930311466056029?hl=ko&tab=jj"),
    ],
    "DIVIDER",

    # 4) 인사이트 섹션
    [
        ("핀터레스트", "https://kr.pinterest.com/"),
        ("네이버 실시간 패션키워드", "https://datalab.naver.com/shoppingInsight/sCategory.naver"),
        ("네이버 쇼핑 패션", "https://shopping.naver.com/window/main/fashion-group"),
    ],
    "DIVIDER",

    # 5) AI 섹션
    [
        ("ChatGPT", "https://chatgpt.com/"),  # ✅ 기존 URL단축 자리로 이동(아래 섹션 첫 칸)
        ("제미나이", "https://gemini.google.com/app"),
        ("클로드 AI", "https://claude.ai/login?returnTo=%2F%3F"),  # ✅ 추가
    ],

    # 6) 홈 섹션
    [
        ("네이버 홈", "https://www.naver.com/"),
        ("다음 홈", "https://www.daum.net/"),
        ("구글 홈", "https://www.google.com/"),
    ],
]

# =========================
# CSS
# =========================
st.markdown(
    f"""
    <style>
      .stApp {{ background: {BG_COLOR}; }}
      .wrap {{ max-width: 1200px; margin: 0 auto; }}

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
        line-height: 1.25;
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

      .divider {{
        height: 1px;
        background: {DIVIDER};
        margin: 18px 0 18px 0;
        border-radius: 999px;
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
# 오늘의 이벤트
# =========================
def today_event(date_obj):
    kr = holidays.KR()
    if date_obj in kr:
        return str(kr.get(date_obj))

    custom = {
        (1, 1): "새해 첫날",
        (2, 14): "발렌타인데이",
        (3, 14): "화이트데이",
        (5, 8): "어버이날",
        (10, 1): "국군의 날",
        (11, 11): "빼빼로데이",
        (12, 31): "연말",
    }
    return custom.get((date_obj.month, date_obj.day), "특별한 일정 없음")

# =========================
# 날씨 (상태 + 최저/최고)
# =========================
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
        if c == 0: return "맑음"
        if c in (1, 2, 3): return "흐림"
        if c in (45, 48): return "안개"
        if c in (51, 53, 55, 56, 57): return "이슬비"
        if c in (61, 63, 65, 66, 67): return "비"
        if c in (71, 73, 75, 77): return "눈"
        if c in (80, 81, 82): return "소나기"
        if c in (95, 96, 99): return "천둥/폭풍"
        return "변동"

    return f"서울·경기 {code_to_text(code)} | 최저 {tmin}° / 최고 {tmax}°"

# =========================
# 화면 렌더
# =========================
st_autorefresh(interval=1000, key="clock_refresh")
now = datetime.datetime.now(KST)

st.markdown('<div class="wrap">', unsafe_allow_html=True)
st.markdown('<div class="title">MISHARP Creative Dashboard</div>', unsafe_allow_html=True)

# 상단 정보
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
    try:
        weather_value = get_weather()
    except Exception:
        weather_value = "날씨 정보를 불러오지 못했어요"

    st.markdown(
        f"""
        <div class="info-card">
          <div class="info-label">오늘의 날씨</div>
          <div class="info-value">{weather_value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# =========================
# 하단 레이아웃 렌더 (구분선 포함)
# =========================
for item in LAYOUT:
    if item == "DIVIDER":
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        continue

    row = item
    cols = st.columns(3, gap="large")
    for col, (name, link) in zip(cols, row):
        with col:
            if name:
                st.markdown(
                    f'<a class="tool-btn" href="{link}" target="_blank" rel="noopener noreferrer">{name}</a>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown('<div style="height:52px;"></div>', unsafe_allow_html=True)

# 푸터
st.markdown(
    """
    <div class="footer">
      미샵컴퍼니 직원 전용 · 제작 미샵컴퍼니 · 외부 유출 금함
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)
