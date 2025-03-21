
import streamlit as st
import datetime
import pandas as pd
import os

st.set_page_config(page_title="언더 경기 분석 체크리스트", layout="centered")

st.title("⚽ 언더 경기 분석 체크리스트")

st.subheader("📌 경기 정보 입력")
match_name = st.text_input("경기명 (예: 캐나다 vs 멕시코)")
match_date = st.date_input("경기 날짜", datetime.date.today())
predicted_score = st.text_input("예상 스코어 (예: 1-1)")
odds_info = st.text_input("오버/언더 배당 정보 (예: 오버 2.5 @1.85)")

st.subheader("✅ 체크리스트")
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

st.subheader("🟢 실제 경기 결과")
actual_result = st.text_input("최종 스코어 (예: 0-2)")
is_under = st.radio("언더로 끝났나요?", ["예", "아니오"])

st.subheader("📊 분석 결과")

score = sum(checks.values())
st.write(f"체크된 항목 수: {score} / 9")

# 요약 문장 생성
summary_points = [key for key, value in checks.items() if value]
summary = " / ".join(summary_points)
if summary:
    st.info(f"✅ 주요 언더 요인 요약: {summary}")

# 결과 판단
if score >= 6:
    st.success("✅ 언더 가능성이 높은 경기였습니다.")
elif 3 <= score < 6:
    st.warning("⚠️ 애매한 흐름입니다. 신중한 접근 필요.")
else:
    st.error("❌ 언더 가능성은 낮은 경기였습니다.")

# 데이터 저장
if st.button("📁 결과 저장하기 (CSV)"):
    save_data = {
        "날짜": match_date,
        "경기명": match_name,
        "예상 스코어": predicted_score,
        "배당 정보": odds_info,
        "체크 수": score,
        "주요 요약": summary,
        "실제 스코어": actual_result,
        "언더 결과": is_under,
    }
    df = pd.DataFrame([save_data])
    if not os.path.exists("match_results.csv"):
        df.to_csv("match_results.csv", index=False, encoding="utf-8-sig")
    else:
        df.to_csv("match_results.csv", mode="a", header=False, index=False, encoding="utf-8-sig")
    st.success("✅ CSV 파일로 저장되었습니다! (match_results.csv)")

if st.button("🔁 모든 데이터 초기화"):
    st.experimental_rerun()
