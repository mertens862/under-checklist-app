
import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="라이브 경기 분석 체크리스트", layout="centered")

st.title("⚽ 라이브 경기 분석 체크리스트")

st.subheader("📌 경기 정보 입력")
match_name = st.text_input("경기명 (예: 캐나다 vs 멕시코)")
match_date = st.date_input("경기 날짜", datetime.date.today())
predicted_score = st.text_input("예상 스코어 (예: 1-1)")
odds_info = st.text_input("오버/언더 배당 정보 (예: 오버 2.5 @1.85)")

st.subheader("✅ 실시간 체크리스트")
checks = {
    "슈팅 대비 유효슈팅 비율이 낮다 (30% 이하)": st.checkbox("1. 슈팅 대비 유효슈팅 비율이 낮다 (30% 이하)"),
    "대부분 박스 밖에서 슈팅한다": st.checkbox("2. 대부분 박스 밖에서 슈팅한다"),
    "빅찬스가 적다 (2~3개 미만)": st.checkbox("3. 빅찬스가 적다 (2~3개 미만)"),
    "골 결정력이 부족하거나 키퍼 선방이 많다": st.checkbox("4. 골 결정력이 부족하거나 키퍼 선방이 많다"),
    "키퍼가 3회 이상 슈퍼세이브를 했다": st.checkbox("5. 키퍼가 3회 이상 슈퍼세이브를 했다"),
    "수비 집중력과 조직력이 좋았다": st.checkbox("6. 수비 집중력과 조직력이 좋았다"),
    "VAR, PK, 세트피스 등의 변수가 없었다": st.checkbox("7. VAR, PK, 세트피스 등의 변수가 없었다"),
    "경기 템포는 빠르지만 파울 등으로 자주 끊겼다": st.checkbox("8. 경기 템포는 빠르지만 파울 등으로 자주 끊겼다"),
    "오버 배당 쏠림에도 실제 흐름은 언더였다": st.checkbox("9. 오버 배당 쏠림에도 실제 흐름은 언더였다"),
}

st.subheader("📊 분석 결과")
score = sum(checks.values())
st.write(f"체크된 항목 수: {score} / 9")
summary_points = [key for key, value in checks.items() if value]
summary = " / ".join(summary_points)
if summary:
    st.info(f"✅ 체크된 주요 흐름 요약: {summary}")

# 판정 문구 수정
if score >= 6:
    st.success("✅ 언더 가능성이 높은 경기입니다.")
elif 3 <= score < 6:
    st.warning("⚠️ 애매한 흐름입니다. 신중한 접근이 필요합니다.")
else:
    st.error("🔥 오버 가능성이 높은 경기입니다.")

# 저장 기능
if st.button("📁 결과 저장하기 (CSV)"):
    save_data = {
        "날짜": match_date,
        "경기명": match_name,
        "예상 스코어": predicted_score,
        "배당 정보": odds_info,
        "체크 수": score,
        "주요 요약": summary,
    }
    df = pd.DataFrame([save_data])
    if not os.path.exists("match_results.csv"):
        df.to_csv("match_results.csv", index=False, encoding="utf-8-sig")
    else:
        df.to_csv("match_results.csv", mode="a", header=False, index=False, encoding="utf-8-sig")
    st.success("✅ CSV 파일로 저장되었습니다! (match_results.csv)")

# 결과 입력 안내 (선택 사항으로 변경)
st.subheader("📝 실제 경기 결과")
st.info("👉 이 체크리스트는 실시간 라이브 분석용입니다.

경기 종료 후 결과를 입력하시겠어요?")
add_result = st.checkbox("✔ 실제 경기 결과를 나중에 추가할 예정입니다.")

# 히스토리 보기 기능
st.subheader("📂 저장된 경기 히스토리 보기")

if os.path.exists("match_results.csv"):
    data = pd.read_csv("match_results.csv")
    search = st.text_input("🔍 경기명 또는 날짜로 검색", "")
    if search:
        filtered = data[data["경기명"].str.contains(search, case=False) | data["날짜"].astype(str).str.contains(search)]
    else:
        filtered = data
    st.dataframe(filtered)
    st.download_button("📥 CSV 다운로드", data=filtered.to_csv(index=False), file_name="match_results_filtered.csv")
else:
    st.info("아직 저장된 데이터가 없습니다.")

if st.button("🔁 모든 데이터 초기화"):
    st.experimental_rerun()
