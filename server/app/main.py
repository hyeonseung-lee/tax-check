from fastapi import FastAPI
from pymongo import MongoClient

# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.vectorstores import Chroma
# from langchain.chains import RetrievalQA
# from langchain.chat_models import ChatOpenAI
# from langchain.schema import HumanMessage
from pydantic import BaseModel
from typing import List

# FastAPI 앱 생성
app = FastAPI()

# MongoDB 설정
MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client["tax_saving_app"]
reports_collection = db["reports"]

# OpenAI API 설정
# OPENAI_API_KEY = "your-openai-api-key"
# embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# # 벡터 DB (ChromaDB) 설정 - 절세 전략 & 세법 규정 분리 저장
# strategy_vector_store = Chroma(persist_directory="./strategy_db", embedding_function=embeddings)
# law_vector_store = Chroma(persist_directory="./law_db", embedding_function=embeddings)

# strategy_retriever = strategy_vector_store.as_retriever()
# law_retriever = law_vector_store.as_retriever()

# llm = ChatOpenAI(model="gpt-4", openai_api_key=OPENAI_API_KEY)
# strategy_qa_chain = RetrievalQA.from_chain_type(llm, retriever=strategy_retriever)
# law_qa_chain = RetrievalQA.from_chain_type(llm, retriever=law_retriever)

# # 데이터 모델 정의
# class AccountInfo(BaseModel):
#     account_number: str
#     balance: float
#     transactions: List[dict]

# class TaxStrategy(BaseModel):
#     text: str

# class TaxLaw(BaseModel):
#     text: str

# # (1) 공인인증서를 통한 로그인 (임시 API)
# @app.post("/login")
# def login(cert_data: dict):
#     return {"message": "공인인증서 로그인 성공", "user_id": "sample_user"}

# # (2) 마이데이터 서비스 연동하여 계좌 정보 가져오기 (더미 데이터)
# @app.get("/accounts/{user_id}")
# def get_accounts(user_id: str):
#     return {
#         "user_id": user_id,
#         "accounts": [
#             {"account_number": "123-456-789", "balance": 1000000, "transactions": []},
#             {"account_number": "987-654-321", "balance": 500000, "transactions": []}
#         ]
#     }

# # (3) RAG에 절세 전략 추가
# @app.post("/add_tax_strategy")
# def add_tax_strategy(strategy: TaxStrategy):
#     """새로운 절세 전략을 벡터 DB에 추가"""
#     strategy_vector_store.add_texts([strategy.text])
#     return {"message": "절세 전략이 성공적으로 추가되었습니다."}

# # (4) RAG에 세법 규정 추가
# @app.post("/add_tax_law")
# def add_tax_law(law: TaxLaw):
#     """새로운 세법 규정을 벡터 DB에 추가"""
#     law_vector_store.add_texts([law.text])
#     return {"message": "세법 규정이 성공적으로 추가되었습니다."}

# # (5) Modular RAG 기반 절세 전략 보고서 생성 (세법 검증 포함)
# @app.post("/generate_verified_rag_report")
# def generate_verified_rag_report(user_id: str, account_info: AccountInfo):
#     """절세 전략을 검색한 후, 세법과 비교하여 검증 후 최종 보고서를 생성"""
#     account_data = f"계좌번호: {account_info.account_number}, 잔액: {account_info.balance}"

#     # 절세 전략 검색
#     strategy_info = strategy_qa_chain.run(account_data)

#     # 세법 검증
#     law_info = law_qa_chain.run(f"다음 절세 전략이 실제 세법에 맞는지 분석해줘: {strategy_info}")

#     # LLM을 이용한 최종 절세 전략 평가
#     prompt = f"""
#     사용자의 계좌 정보를 기반으로 절세 전략을 추천해줘.
#     절세 전략: {strategy_info}
#     관련 세법 규정: {law_info}

#     위 절세 전략이 세법과 일치하는지 분석하고, 만약 법적 문제가 있다면 수정된 절세 전략을 제시해줘.
#     """
#     response = llm([HumanMessage(content=prompt)])
#     report_text = response.content

#     # (6) MongoDB에 저장
#     report = {"user_id": user_id, "account_number": account_info.account_number, "report_text": report_text}
#     reports_collection.insert_one(report)

#     return {"user_id": user_id, "report": report_text}


# # (7) MongoDB에서 저장된 보고서 목록 불러오기
# @app.get("/reports/{user_id}")
# def get_reports(user_id: str):
#     reports = list(reports_collection.find({"user_id": user_id}, {"_id": 0}))
#     return {"user_id": user_id, "reports": reports}
@app.get("/")
def get_reports():
    return {"home"}
