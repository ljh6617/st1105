import streamlit as st

st.title("10주차 스트림릿 연습")

st.info("안녕하세요. 소개페이지입니다. 블라블라")

st.error("에러창인데 빨간 박스")
st.success("성공창인데 초록 박스")
st.warning("경고창인데 노란 박스")

st.header("메인페이지")
st.subheader("그다음 중제목")
st.write("모든 내용 다 쓰기 가능")
st.markdown("이것은 **텍스트** 쓰기")
st.latex("ax^2+bx+c=0")
st.code("print('Hello teachers')")
st.write("---")
st.image("image1.jpeg", use_column_width=True)
st.image("https://cdn.eyesmag.com/content/uploads/posts/2024/10/24/3-91b6b86b-0f70-4308-ba73-d0558b744c7f.png")
st.video("https://www.youtube.com/watch?v=O5Ht2SAGzqs&list=RDO5Ht2SAGzqs&start_radio=1")
st.write("www.desmos.com/matrix")
st.link_button("데스모스 행렬 계산기 바로가기", url="https://www.desmos.com/matrix")
st.components.v1.iframe("https://www.desmos.com/matrix", height=500)

