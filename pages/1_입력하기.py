import streamlit as st

classcode = "1234"
code = st.text_input("강의 코드를 입력하세요")
# 비어 있으면 입력 안내, 1234이면 환영, 그 외에는 불일치
if not code:
    st.warning("코드를 입력하세요")
elif code == classcode:
    st.success("환영합니다")
else:
    st.error("코드가 일치하지 않습니다")

st.subheader("다양한 인풋")

#객관식(라디오버튼, 체크박스), 주관식(숫자만 입력, 텍스트 입력), 슬라이더, 파일 업로드

#a가 답임!
answer = st.radio("객관식", ["A", "B", "C", "D"])
if answer == "A":
    st.success("정답입니다")
else:
    st.error("오답입니다")

agree = st.checkbox("동의합니다.")
if agree:
    st.success("동의하셨습니다.")
else:
    st.error("동의하지 않으셨습니다.")

answer2 = text_input = st.text_input("이름을 입력해주세요.", placeholder="홍길동")
answer3 = st.number_input("나이를 입력해주세요.", min_value=0, max_value=100, step=5, value=20)
st.write(answer3*2+1)

if st.button("확인"):
    st.success("확인되었습니다.")

#라디오버튼 문제에 대한 정답 제출하기 버튼 -> 피드백
if st.button("정답 제출하기"):
    st.success("확인되었습니다.")


