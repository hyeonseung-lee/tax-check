from fastapi import FastAPI
from pymongo import MongoClient

# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.vectorstores import Chroma
# from langchain.chains import RetrievalQA
# from langchain.chat_models import ChatOpenAI
# from langchain.schema import HumanMessage
from pydantic import BaseModel
from typing import List
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import RetrievalQA, LLMChain
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

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

llm = ChatOpenAI(model="gpt-4", openai_api_key=os.getenv("OPENAI_API_KEY"))

# 데이터 모델 정의

class Transactions(BaseModel):
    created_date: str #입출금날짜
    amount: str #거래금액
    is_dividend: int #배당금이면 1, 내가 납입한 거면 0

class Market(BaseModel):
    created_date: str #거래날짜
    buysell: int #buy는 1, sell은 0
    stock_name: str #종목명
    stock_amount: str #거래수량
    stock_price: str #거래단가
    average: str #평균단가가

class Stocks(BaseModel):
    stock_name: str #종목명
    average: str #평균단가가 쉼표 넣어서 작성, ex) 2,000,000
    valuation: str #평가금액
    stock_amount: str #보유수량

class AccountInfo(BaseModel):
    managing: str #운용사
    account_status: int #계좌상태
    account_number: str #계좌번호
    account_category: str #계좌종류 (IRP, ISA, 연금저축펀드, 해외주식계좌, 일반계좌)
    balance: str #평가금액
    purchase: str #매수금액
    profit: str #평가손익
    created_date: str #계좌개설일
    transactions: List[Transactions] #입출금
    market: List[Market] #매매내역
    stocks: List[Stocks] #보유종목

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

# (3) LangChain을 사용하여 ChatGPT로 절세 전략 보고서 생성
@app.post("/generate_report")
def generate_report(user_id: str, account_info: AccountInfo):
    prompt = ChatPromptTemplate.from_template("""
    너는 대한민국의 증권 계좌를 통한 절세 도우미야. 네가 할 일은 계좌 정보를 확인하여, 각 계좌 정보에 맞는 세액 공제 및 절세 전략을 추천해 줘야 해.

        account-info의 데이터 정보는 다음과 같아.
        class Transactions(BaseModel):
            created_date: str #입출금날짜
            amount: str #거래금액
            is_dividend: int #배당금이면 1, 내가 납입한 거면 0

        class Market(BaseModel):
            created_date: str #거래날짜
            buysell: int #buy는 1, sell은 0
            stock_name: str #종목명
            stock_amount: str #거래수량
            stock_price: str #거래단가
            average: str #평균단가가

        class Stocks(BaseModel):
            stock_name: str #종목명
            average: str #평균단가가 쉼표 넣어서 작성, ex) 2,000,000
            valuation: str #평가금액

        class AccountInfo(BaseModel):
            managing: str #운용사
            account_status: int #계좌상태
            account_number: str #계좌번호
            account_category: str #계좌종류 (IRP, ISA, 연금저축계, 해외주식계좌, 일반계좌)
            balance: str #평가금액
            purchase: str #매수금액
            profit: str #평가손익
            created_date: str #계좌개설일
            transactions: List[Transactions] #입출금
            market: List[Market] #매매내역
            stocks: List[Stocks] #보유종목

        올해 납입금액: Transactions.created_date의 연도가 2024년인 항목을 모두 더하여 계산한다.
        올해 수익: Market.created_date의 연도가 2024년이며 buysell이 0인 항목의 (stock_price - average) * stock_amount + Transactions의 created_date가 2024년이며 is_dividend가 1인 항목으로 계산한다.
        손익통산: Market.buysell == 0인 항목들의 (stock_price - average) * stock_amount 항목을 총합하고 Transactions의 created_date가 2024년이며 is_dividend가 1인 항목을 합쳐서 계산한다.
        평가손익: AccountInfo.profit

        해외 주식 양도소득세 계산 시, 올해 수익을 손익통산하여 2,500,000이 될 수 있도록 계산하여 준다. 초과하는 내용은 (손익통산 - 2,500,000) * 0.22 의 세금이 부과함을 계산하여 안내한다.
        ISA 계좌의 경우 평가손익 2,000,000원까지 비과세이고, 초과분은 만기 시점에 9.9% 분리과세 함을 안내한다.

        IRP·연금저축계좌는 합쳐서 연 9,000,000원까지 납입 시 세액공제 가능. 연금저축계좌는 최대 6,000,000원까지 세액 공제 가능하니, 연금저축계좌부터 6,000,000원 한도를 채운 후 IRP는 3,000,000원까지 세액 공제 가능하다. 총급여 55,000,000원 이하는 16.5%(최대 1,485,000원), 초과 시 13.2%(최대 1,188,000원) 공제. 연금저축 단독 공제 한도는 6,000,000원이다. IRP는 9,000,000원에서 연금저축계좌 납입금액을 제외한 만큼 세액 공제가 가능하다.
        ISA는 연 20,000,000원, 총 100,000,000원 납입 가능. 운용 수익 (일반형: 2,000,000원, 서민형: 4,000,000원)까지 비과세, 만기 시 초과분은 9.9% 분리과세. ISA는 납입만으로 세액 공제는 되지 않고, 배당소득세에 대해서 2,000,000원까지 비과세, 초과분은 9.9% 분리 과세한다. 서민형일 때는 4,000,000원까지 비과세, 초과분은 9.9% 분리 과세한다.
        해외주식 양도소득세는 연 2,500,000원까지 비과세, 초과분은 22% 과세. 절세 방법: ① 2,500,000원 이하로 분할 매도 ② 손실 종목 매도로 수익과 상계 ③ 손실 종목은 다시 매수한다

        1. 연금저축계좌/IRP는 하나의 섹터로 각각 올해 납입 금액을 계산하여 추가로 납입할 금액을 통해 최대로 세액 공제를 받을 수 있는 전략을 계산하여 추천해 준다. 총 급여가 55,000,000원 이하인 경우, 초과인 경우 둘 다 계산한다.
        2. ISA 계좌의 경우 전체 평가손익을 기준으로 일반형은 2,000,000원 이하는 비과세 서민형은 4,000,000원 이하는 비과세로, 그 초과분은 0.099를 곱하여 세금을 계산해 준다. 서민형과 일반형 중 알맞은 것으로 계산한다.
        3. 해외주식 양도소득세는 올해 수익이 2,500,000원 이하로 만들 수 있는 매도 전략을 계산하여 추천해 준다.
        
        보고서 형식으로 친절하게 대답해 줘.
        사용자의 계좌 정보: {account-info-list}
    """)
    response = (prompt|llm|StrOutputParser())
    report_text = response.content

    # (3-1) 보고서를 MongoDB에 저장
    report = {"user_id": user_id, "report_text": report_text}
    reports_collection.insert_one(report)
    
    return {"user_id": user_id, "report": report_text}

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
