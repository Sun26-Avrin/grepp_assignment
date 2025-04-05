Docker Image 로 만드는데 실패해서, 로컬 설치 방법을 작성합니다.

#### 실행방법
1. python 3.12.9 버전 이상 설치
2. postgresql@14 버전 설치
3. postgresql 실행
4. python3 -m venv venv
5. source venv/bin/activate
6. pip install -r requirements.txt
7. uvicorn app.main:app --reload
