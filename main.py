import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

# 2. 메인 타이틀
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("1년치(365일) 일별 박스오피스 데이터를 바탕으로 시간 흐름에 따른 시각화 그래프를 제공합니다.")
st.markdown("---")

# 3. 데이터 로드 및 전처리 함수
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # '날짜' 열을 문자열 변환 후 datetime 객체로 변환 (YYYYMMDD -> YYYY-MM-DD)
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# ==========================================
# [섹션 1] 영화별 일관객수 변화 (선 그래프)
# ==========================================
st.subheader("1. 영화별 일관객수 추이")

# 영화 목록 추출 (가나다순 정렬)
movie_list = sorted(df['영화명'].unique())

# 영화 선택 드롭다운
selected_movie = st.selectbox(
    "📊 관객수 추이를 확인할 영화를 선택하세요:",
    movie_list,
    index=0
)

# 선택한 영화 데이터 필터링 및 날짜순 정렬
filtered_df = df[df['영화명'] == selected_movie].sort_values('날짜')

# Plotly 선 그래프 생성
fig1 = px.line(
    filtered_df,
    x='날짜',
    y='일관객',
    title=f"<{selected_movie}> 날짜별 일관객수 변화",
    labels={'날짜': '날짜', '일관객': '일일 관객수(명)'},
    hover_data={'날짜': '|%Y-%m-%d', '일관객': ':,d'}
)

# 그래프 디자인 요소 설정
fig1.update_traces(mode='lines+markers', line=dict(width=2.5))
fig1.update_layout(
    xaxis_title="날짜",
    yaxis_title="일일 관객수(명)",
    hovermode="x unified",
    margin=dict(l=20, r=20, t=50, b=20)
)

# Plotly 그래프 출력
st.plotly_chart(fig1, use_container_width=True)

# 그래프 해설 문구 자리
st.info("💡 **이 그래프로 알 수 있는 것:** 특정 영화의 개봉 후 시간 경과에 따른 관객수 증감 추이와 주말/평일 관객 격차 폭을 한눈에 확인할 수 있습니다.")

st.markdown("---")

# ==========================================
# [섹션 2] 상위 Top 5 영화의 개봉일차별 일관객수 비교 (가로축: 개봉일차)
# ==========================================
st.subheader("2. 일관객 합계 Top 5 영화의 개봉일차별 일관객수 비교")

# 전체 기간 동안 일관객 합계 상위 5개 영화 추출
top5_movies = (
    df.groupby('영화명')['일관객']
    .sum()
    .nlargest(5)
    .index.tolist()
)

# Top 5 영화 데이터 필터링
top5_df = df[df['영화명'].isin(top5_movies)].copy()

# 각 영화별 최초 등재 날짜(개봉일) 기준 '개봉일차' 로직 계산
top5_df['최초날짜'] = top5_df.groupby('영화명')['날짜'].transform('min')
top5_df['개봉일차'] = (top5_df['날짜'] - top5_df['최초날짜']).dt.days + 1

# 개봉일차 기준으로 정렬
top5_df = top5_df.sort_values(['영화명', '개봉일차'])

# Plotly 복수 선 그래프 생성 (x축: 개봉일차)
fig2 = px.line(
    top5_df,
    x='개봉일차',
    y='일관객',
    color='영화명',
    title="기간 내 일관객 합계 Top 5 영화의 개봉일차별 일관객수 비교",
    labels={'개봉일차': '개봉일차 (일)', '일관객': '일일 관객수(명)', '영화명': '영화 제목'},
    hover_data={'날짜': '|%Y-%m-%d', '개봉일차': '%d일차', '일관객': ':,d'}
)

fig2.update_traces(mode='lines+markers')
fig2.update_layout(
    xaxis_title="개봉일차 (1일차 = 차트에 진입한 첫날)",
    yaxis_title="일일 관객수(명)",
    hovermode="x unified",
    legend_title_text="영화 선택 (범례 클릭 시 토글)",
    margin=dict(l=20, r=20, t=50, b=20)
)

st.plotly_chart(fig2, use_container_width=True)

# 그래프 해설 문구 자리
st.info("💡 **이 그래프로 알 수 있는 것:** 개봉 시기가 서로 다른 흥행작들의 개봉 후 동일 시점(일차별) 관객 동원력과 흥행 유효기간, 관객 감소율을 동일 기준선상에서 직관적으로 비교할 수 있습니다.")

st.markdown("---")

# ==========================================
# [섹션 3] (추가 예정 구역)
# ==========================================
st.subheader("3. 누적관객수 성장 곡선 (추가 예정)")
st.caption("📌 이 구역에는 시간 흐름에 따른 누적관객수 달성 속도 비교 그래프가 추가될 예정입니다.")
# TODO: 다음 그래프 구현 위치
