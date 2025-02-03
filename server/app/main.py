from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List
from app.db.database import strategyHistory_collection, db
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import RetrievalQA, LLMChain
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

# FastAPI 앱 생성
app = FastAPI()

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

# (3) LangChain을 사용하여 ChatGPT로 절세 전략 보고서 생성
@app.post("/generate_report")
async def generate_report(user_id: str, account_info: List[AccountInfo]):
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
    report_text = (prompt|llm|StrOutputParser()).invoke({"account-info-list":account_info})

    # (3-1) 보고서를 MongoDB에 저장
    report = {
        "user_id": user_id,
        "report_text": report_text,
        "created_at": datetime.utcnow()
    }
    await strategyHistory_collection.insert_one(report)
    
    return report

@app.get("/")
def get_reports():
    return {"home"}