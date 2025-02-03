from fastapi import FastAPI, Depends
from pymongo import MongoClient
from bson import ObjectId

# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.vectorstores import Chroma
# from langchain.chains import RetrievalQA
# from langchain.chat_models import ChatOpenAI
# from langchain.schema import HumanMessage

from .db.database import get_db, strategyHistory_collection
from pydantic import BaseModel
from typing import List
from bson import ObjectId
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import RetrievalQA, LLMChain
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

# FastAPI 앱 생성
app = FastAPI(
    title="Tax Check", version="1.0", description="사용자의 절세를 돕는 전략 보고서"
)

# OpenAI API 설정
# OPENAI_API_KEY = "your-openai-api-key"
# embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# # 벡터 DB (ChromaDB) 설정 - 절세 전략 & 세법 규정 분리 저장
# strategy_vector_store = Chroma(persist_directory="./strategy_db", embedding_function=embeddings)
# law_vector_store = Chroma(persist_directory="./law_db", embedding_function=embeddings)

# strategy_retriever = strategy_vector_store.as_retriever()
# law_retriever = law_vector_store.as_retriever()

llm = ChatOpenAI(model="gpt-4", openai_api_key=os.getenv("OPENAI_API_KEY"))

# DB Setting
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.compass
users_collection = db.users
strategyHistory_collection = db.strategyHistory

# 데이터 모델 정의


class Transactions(BaseModel):
    created_date: str #입출금날짜
    amount: float #거래금액
    is_dividend: int #배당금이면 1, 내가 납입한 거면 0

class Market(BaseModel):
    created_date: str #거래날짜
    buysell: int #buy는 1, sell은 0
    stock_name: str #종목명
    stock_amount: int #거래수량
    stock_price: float #거래단가
    average: float #평균단가가

class Stocks(BaseModel):
    stock_name: str #종목명
    average: float #평균단가
    valuation: float #평가금액
    stock_amount: int #보유수량

class AccountInfo(BaseModel):
    managing: str #운용사
    account_status: int #계좌상태
    account_number: str #계좌번호
    account_category: str #계좌종류 (IRP, ISA, 연금저축펀드, 해외주식계좌, 일반계좌)
    balance: float #평가금액
    purchase: float #매수금액
    profit: float #평가손익
    created_date: str #계좌개설일
    transactions: List[Transactions] #입출금
    market: List[Market] #매매내역
    stocks: List[Stocks] #보유종목
    
# ObjectId를 문자열로 변환하는 함수
def serialize_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj


# IRP/연금저축펀드 납입금액 계산
def calc_irp(account_info: List[AccountInfo]):
    total_irp = 0
    total_pb = 0
    irp_exist = 0
    pb_exist = 0
    for account in account_info:
        if account.account_category == 'IRP':
            irp_exist = 1
            for transaction in account.transactions:
                created_date = transaction.created_date
                amount = int(transaction.amount)
                
                if created_date[:4] == str(int(datetime.today().year)-1):
                    total_irp += amount

        if account.account_category == '연금저축계좌':
            pb_exist = 1
            for transaction in account.transactions:
                created_date = transaction.created_date
                amount = int(transaction.amount)
                
                if created_date[:4] == str(int(datetime.today().year)-1):
                    total_pb += amount

    # 연금저축계좌 최대
    remain_pb = 6000000 - total_pb

    # IRP 계좌 최대
    remain_irp = 3000000 - total_irp

    return remain_pb, remain_irp, remain_pb + remain_irp, pb_exist, irp_exist #연금저축계좌 남은납입금액, irp 남은납입금액, 총 남은납입금액

# 현재 금액일 시 세액 공제 얼마 받는지와 최대로 채우면 얼마 받는지
# 총급여 55,000,000원 이하는 16.5%(최대 1,485,000원), 초과 시 13.2%(최대 1,188,000원) 공제.
def calc_irp_tax(remains: float):
    now_over_pp = (
        9000000 - remains
    ) * 0.132  # 5500만원 초과인 경우 현재 납입 금액에서 받는 세액 공제
    now_min_pp = (
        9000000 - remains
    ) * 0.165  # 5500만원 이하하인 경우 현재 납입 금액에서 받는 세액 공제
    return now_min_pp, now_over_pp


# ISA 계좌 총 수익 통산
def profit_isa(account_info: List[AccountInfo]):
    total_profit = 0
    isa_exist = 0
    isa_category = ''
    for account in account_info:
        if account.account_category[:3] == 'ISA':
            isa_exist = 1
            isa_category = account.account_category[4:]
            total_profit += account.profit
            for transaction in account.transactions:
                if transaction.is_dividend == 1:
                    total_profit += transaction.amount
    return total_profit, isa_category, isa_exist


# ISA 계좌 서민형/일반형 확인 후 얼마큼 나오는지 확인
def isa_version(total_profit, isa_category):
    save_tax = 0
    if isa_category == "서민형":
        if total_profit < 4000000:
            save_tax += total_profit * 0.154
        else:
            save_tax += 4000000 * 0.154
            save_tax += (total_profit - 4000000) * (0.154 - 0.099)
    elif isa_category == "일반형":
        if total_profit < 2000000:
            save_tax += total_profit * 0.154
        else:
            save_tax += 2000000 * 0.154
            save_tax += (total_profit - 2000000) * (0.154 - 0.099)
    return save_tax  # 비과세로 save한 금액


# 해외 주식 계좌 손익통산
def overseas_profit(account_info: List[AccountInfo]):
    target_year = str(int(datetime.today().year) - 1)

    total_profit = 0

    for account in account_info:
        if account.account_category == "해외주식계좌":
            # 매매 수익 계산
            for market in account.market:
                created_date = market.created_date
                buysell = int(market.buysell)
                stock_price = int(market.stock_price)
                average = int(market.average)
                stock_amount = int(market.stock_amount)

                if created_date and buysell == 0:
                    transaction_year = created_date[:4]
                    if transaction_year == target_year:
                        total_profit += (stock_price - average) * stock_amount

            # 배당금 수익 계산
            for transaction in account.transactions:
                created_date = transaction.created_date
                is_dividend = int(transaction.is_dividend)
                amount = int(transaction.amount)

                if created_date and is_dividend == 1:
                    transaction_year = created_date[:4]
                    if transaction_year == target_year:
                        total_profit += amount

    return total_profit


# 해외주식 매도 전략
def overseas_min_tax(total_profit):
    if total_profit > 2500000:
        return "손실 중인 종목 매도"
    else:
        return "아직 2,500,000원 미만의 수익이기에에 비과세 한도입니다."
      
# (3) LangChain을 사용하여 ChatGPT로 절세 전략 보고서 생성
@app.post("/generate_report")
def generate_report(user_id: str, account_info: List[AccountInfo], db=Depends(get_db)):
    # 남은 연금저축계좌 납입금액, 남은 irp 납입금액, 남은 전체 납입금액
    remain_pb, remain_irp, remain_pp, pb_exist, irp_exist = calc_irp(account_info)

    # 지금까지 납입한 연금저축계좌와 irp의 세액 공제 금액
    now_min_pp, now_over_pp = calc_irp_tax(remain_pp)

    # ISA 손익통산과 계좌 종류 
    isa_total_profit, isa_category, isa_exist = profit_isa(account_info)

    # ISA로 절세한 금액
    save_tax = isa_version(isa_total_profit, isa_category)

    # 해외주식 손익통산
    overseas_total_profit = overseas_profit(account_info)

    # 해외주식 매도 전략
    overseas_min = overseas_min_tax(overseas_total_profit)

    prompt = ChatPromptTemplate.from_template(
        """
    너는 대한민국의 증권 계좌를 통한 절세 도우미야.
    계산을 통해 얻은 정보들을 활용하여, 사용자가 편하게 이해할 수 있도록 보고서 형식으로 작성해 줘야 해.

    1. 연금저축계좌/IRP
    최대로 세액 공제를 받기 위해 우선 연금저축계좌와 IRP 계좌가 있는지 확인.
    {pb_exist}가 1이면 연금저축계좌가 존재한다.
    {irp_exist}가 1이면 IRP계좌가 존재한다.
    0일 경우 존재하지 않으니, 계좌 개설 안내와 함께 납입을 안내한다.
    연금저축계좌에 추가 납입해야 하는 금액: {remain_pb}
    IRP에 추가 납입해야 하는 금액: {remain_irp}

    2. ISA 계좌
    {isa_exist}가 1이면 ISA 계좌가 존재하고 0이면 존재하지 않는다. ISA 계좌의 혜택과 함께 개설을 권유해야 한다.
    ISA 계좌가 존재하지 않는다면 아래 지금까지 얻은 수익과 절세한 금액은 보고서에 사용하지 않는다.
    ISA 계좌에서 지금까지 얻은 수익: {isa_total_profit},
    ISA 계좌를 사용했기에 절세한 금액: {save_tax}

    3. 해외주식 양도소득세 계산
    해외 주식 손익통산한 금액: {overseas_total_profit}
    해외 주식 매도 전략: {overseas_min}
    해외 주식을 손익통산한 금액이 0일 경우, 아직 해외 주식을 매도하지 않은 것 같지만 연 250만원까지는 수익에 대해 비과세이므로, 250만원까지는 매도해도 된다고 안내해 줘.

    이러한 계산을 기반으로 정중하게 보고서를 작성해 줘. 각 계좌별 절세 전략과 함께 길고 친절하게 설명해 줘.
    마크 다운 형식으로 제목이 조금 더 크고 돋보이게 출력해 줘.                                  
    """
    )

    report_text = (prompt|llm|StrOutputParser()).invoke({"remain_pb":remain_pb, "remain_irp":remain_irp, "isa_total_profit":isa_total_profit, 
                                                         "pb_exist":pb_exist, "irp_exist":irp_exist, "isa_exist":isa_exist,
                                                         "save_tax": save_tax, "overseas_total_profit":overseas_total_profit, "overseas_min":overseas_min})


    # (3-1) 보고서를 MongoDB에 저장
    report = {"user_id": user_id, "report_text": report_text}
    strategyHistory_collection.insert_one(report)

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
#     strategyHistory_collection.insert_one(report)

#     return {"user_id": user_id, "report": report_text}


# # (7) MongoDB에서 저장된 보고서 목록 불러오기
@app.get("/")
async def get_reports(db=Depends(get_db)):
    history = await db.strategyHistory.find({}, {"_id": 0}).to_list(100)
    return {"history": history}


# # (8) MongoDB에서 저장된 보고서 ID로 상세조회
@app.get("/{id}")
async def get_report_detail(id: str, db=Depends(get_db)):
    object_id = ObjectId(id)
    history = (
        await db.strategyHistory.find({"_id": object_id}, {"_id": 0}).to_list(100)
    )
    return history
