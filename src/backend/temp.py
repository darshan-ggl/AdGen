attr_desc = {
    "DealCurrencyCode": "Currency Code",
    "FacilityRateBasisCode": "Driver of the pricing level (i.e. external ratings, leveraged ratio, utilization, etc.)",
    "FacilityRateBasisDescription": "Classification of the different types of FacilityPricingRateBasisType, which will appear in the UI.",
    "FacilityRateBasisLongDescription": "Optional - Detailed description of the FacilityRateBasis",
    "EffectiveStartDate": "Date the identifier first become effective. aka start date, commence date.",
    "FacilityRoundingDecimalPrecisionCode": "Rounding applicable for decimal values",
    "FacilityRoundingDecimalPrecisionDescription": "Classification of the different types of FacilityRoundingDecimalPrecisionType, which will appear in the UI.",
    "FacilityRoundingDecimalPrecisionLongDescription": "Optional - Detailed description of the FacilityRoundingDecimalPrecision",
    "CreditAgreementDate": "Date of the original Credit Agreement",
    "DealCloseDate": "Date in which the original Credit Agreement closed / Citi entered Credit Agreement",
    "DealMaximumMatchFundedLoanNumber": "Maximum number of matchfunded (ex. LIBOR) loan contracts / interest periods allowed under the credit agreement",
    "DealPurposeID": "ID represents overarching credit agreement use of proceeds (e.g. Acquisition) at origination",
    "DealPrimaryCurrencyCode": "Currency Code",
    "FacilityPrepaymentCode": "Code denotes whether prepayment is mandatory or optional",
    "FacilityPrepaymentDescription": "Classification of the different types of FacilityPrepaymentType, which will appear in the UI.",
    "FacilityPrepaymentLongDescription": "Optional - Detailed description of the FacilityPrepayment",
    "EffectiveEndDate": "The date on which a charge or variation of a charge ceases to have effect on the identifier.",
    "OngoingFeeDetailToRangeComputationBasisText": "Rate basis value utilized for the formula (e.g. ratio, leverage, utilization, etc.)",
    "OngoingFeeDetailSpreadRate": "Actual rate / margin / spread value corresponding to the pricing level denoted",
    "OngoingFeeDetailEffectiveDate": "Date on which the specific pricing level becomes effective",
    "PricingCurrencyCode": "Currency Code",
    "FacilityPricingGridReferenceCode": "Code denotes the basis for applying pricing",
    "LenderCommitmentAmount": "Corresponding commitment / share of the facility / credit line for each respective lender per the commitment schedule of the credit agreement (primary); any subsequent changes / assignments should feed back from Loan IQ",
    "LenderProrataPercentage": "Percentage of the respective lender''s facility commitment amount divided by the total global facility commitment amount",
    "FacilityAvailableCurrencyCode": "Currency Code",
    "FacilityPurposeTypeID": "Primary purpose for the facility in terms of how the credit line will be utilized for the client (i.e. general corporate purposes, refinance, etc.)",
    "FacilityPurposeTypeLongDescription": "Long description for FacilityPurposeType",
    "FacilityPurposeDescription": "Classification of the different types of FacilityPurposeType, which will appear in the UI.",
    "SublimitCurrencyCode": "Currency Code",
    "FacilityRoundingID": "Number of decimal places utilized for alternative rate",
    "FacilityRoundingDescription": "Classification of the different types of FacilityRounding type, which will appear in the UI.",
    "FacilityRoundingLongDescription": "Optional - Detailed description of the FacilityRounding",
    "OngoingFeeEffectiveDate": "Effective / start / addition date in which this pricing option is available under the facility",
    "OngoingFeeMaturityDate": "Maturity / end / removal date in which this pricing option is no longer available under the facility",
    "OngoingFeeFloorRate": "Rate floor / minimum given for a specific rate / pricing option (e.g. LIBOR 1% floor, 0%, etc.)",
    "OngoingFeeCeilingRate": "Rate ceiling / maximum given for a specific rate / pricing option",
    "FeeTypeCode": "Code classifies fee- counting Accounting Units according to the type of fee that applies.",
    "NonBusinessDayRuleCode": "Defines requirement of how to treat fee payment if due date falls on the day of the month or quarter that is a weekend or holiday (e.g. preceding business day)",
    "FacilityFeeRateBasisCode": "Driver of the pricing level (i.e. external ratings, leveraged ratio, utilization, etc.)",
    "FacilityFeeBasisCode": "Pricing margins in basis points (BPS) or percentage (%)",
    "FacilityFeeBasisPointCode": "Pricing margins in basis points (BPS) or percentage (%)",
    "PricingDetailFromRangeComputationBasisText": "Rate basis value utilized for the formula (e.g. ratio, leverage, utilization, etc.)",
    "PricingDetailToRangeComputationBasisText": "Rate basis value utilized for the formula (e.g. ratio, leverage, utilization, etc.)",
    "PricingDetailSpreadRate": "Actual rate / margin / spread value corresponding to the pricing level denoted",
    "PricingDetailFloorRate": "Rate Floor / minimum given for a specific rate / pricing option (e.g. LIBOR 1% floor, 0%, etc.) corresponding with pricing level",
    "PricingDetailEffectiveDate": "Date on which the specific pricing level becomes effective",
    "PricingOptionFromRangeParameterSignCode": "Code represents formula signs to allow for the mathematical translation of the credit agreement pricing / margin grids.",
    "PricingOptionToRangeParameterSignCode": "Code represents formula signs to allow for the mathematical translation of the credit agreement pricing / margin grids.",
    "FacilityGlobalAmount": "Aggregate / total amount of the facility; sum of all lender shares if syndicated; equal to Citi commitment if bilateral loan",
    "FacilityEffectiveDate": "Date in which the facility became effective and all CPs are met facility is available for use / draw",
    "FacilityMaturityDate": "Date in which the facility matures / terminates after which no new principal can be released and all principal, interest, and fees due from the borrower(s) must be paid in full",
    "FacilityExpirationDate": "Date in which the facility may no longer have new loan draws (e.g. term loans that are single draw should expire on the same day as the original draw)",
    "ExtendedMaturityDate": "This field captures the last date that funds must be repaid, inclusive of extension options",
    "PricingDefaultInterestRate": "Interest rate to be applied in case of default",
    "OngoingFeeDefaultInterestRate": "Interest rate to be applied in case of default",
    "PrepaymentPenaltyAmount": "Penalty amount applicable in case of pre-payment",
    "FacilityGlobalCurrentCommitmentAmount": "Aggregate / total amount of the facility current amount (both LCs and loans); sum of all lender shares if syndicated; equal to citi commitment if bilateral loan (to feed from Loan IQ)",
    "FacilityTypeID": "Type of facility being reviewed (e.g. revolving credit, term loan A, term loan B, etc.)",
    "AmortizingOrAccretingCode": "- Accreting - used to describe facility where notional amount of credit exposure increases over life of facility. Applicable only to committed facilities.",
    "FacilityExtendedMaturityOptionCode": "This field captures the party that has the option to extend the maturity date (borrower or lender), as per Credit Agreement",
    "FacilityCoBorrowerStructureCode": "Capture co-borrower structure against each facility",
    "FacilityPrimaryCurrencyCode": "Currency Code",
    "FacilityPurposeCode": "Facility Purpose Code",
    "FacilityTypeCode": "Facility Type Code",
    "PrimaryAgentIndicator": "To identify if an administrative agent or a documentation agent is the primary agent in a facility. This is an optional field.",
    "PricingEffectiveDate": "Effective / start / addition date in which this pricing option is available under the facility",
    "PricingMaximumDrawAmount": "Maximum amount that a single draw / LC request can be made on using the specific pricing type",
    "PricingMinimumDrawAmount": "Minimum amount that a single draw / LC request can be made on using the specific pricing type",
    "PricingMinimumMultiplesNumber": "Minimum multiple in which a single draw / LC request can be made in for the specific pricing type (e.g. 1mm)",
    "InterestDueUponPrincipalIndicator": "Whether or not interest is due upon receipt of principal (e.g. LIBOR)",
    "InterestDueUponRepricingIndicator": "Whether or not interest is due upon repricing (e.g. LIBOR)",
    "PricingIntentNoticeAdvanceDayCount": "Number of business days the intention to notice to draw or reprice / LC request must be provided per the Credit Agreement",
    "PricingIntentNoticeTimeText": "Time by which the intention to notice to draw or reprice / LC request must be provided per the Credit Agreement on the request day",
    "PricingRateSetAdvanceDayCount": "Number of business days the rate needs to be set for the draw or reprice per the Credit Agreement",
    "PricingRateSetTimeText": "Time by which the rate needs to be set for the draw or reprice per the Credit Agreement on the rate set day",
    "PricingFloorRate": "Rate floor / minimum given for a specific rate / pricing option (e.g. LIBOR 1% floor, 0%, etc.)",
    "PricingCeilingRate": "Rate ceiling / maximum given for a specific rate / pricing option",
    "PricingLookbackNumber": "To be filled if Interest Type = Simple/Compounded",
    "CreditAdjustmentSpreadIndicator": "To capture whether CAS is applicable for the RFR pricing option or not.",
    "PricingFloorIndicator": "Pricing Floor Indicator",
    "FacilityPricingTypeID": "Pricing option / rate or fee available under the facility (LC, Swingline, LIBOR Loan, Prime Loan, etc.)",
    "FacilityPricingRateBasisCode": "Driver of the pricing level (i.e. external ratings, leveraged ratio, utilization, etc.)",
    "FacilityPricingBasisCode": "Pricing margins in basis points (BPS) or percentage (%)",
    "FacilityPricingBasisPointCode": "Pricing margins in basis points (BPS) or percentage (%)",
    "FacilityInterestTypeCode": "Term v Simple v Compounded",
    "FacilityPricingPaymentTypeCode": "Billing / payment convention for fee; payments made in arrears means you pay for the period that has passed vs. in advance means you pay for the period ahead",
    "PricingRateSetTimeCode": "Code represents time by which the intention notice to draw or reprice / LC request must be provided per the Credit Agreement on the request day",
    "PricingIntentNoticeTimeCode": "Code represents time by which the intention notice to draw or reprice / LC request must be provided per the Credit Agreement on the request day",
    "PricingRateSetTimezoneCode": "Code represents the time by which the intention notice to draw or reprice / LC request must be provided per the Credit Agreement on the request day",
    "PricingIntentNoticeTimezoneCode": "Code represents the time by which the intention notice to draw or reprice / LC request must be provided per the Credit Agreement on the request day",
    "FloorApplicationCode": "To determine how floor rate will be applied",
    "SublimitCommitmentAmount": "Corresponding commitment the Issuing / Fronting Bank is willing to issue / front / fund per the credit agreement",
    "ProRataPercentage": "Percentage of the respective Issuing / Fronting Bank''s issuing / Fronting commitment amount divided by the total global facility commitment amount available for the specific instrument available",
    "ApplicableHolidayCalendarCode": "Country or state holiday calendars codes for applicable currencies, funding jurisdictions, etc. as stipulated in credit agreement",
    "SublimitAmount": "Amount corresponding to sublimit type",
    "AmortizationPaymentDate": "The expected date in which the amortization payment - reduction of credit facility - is scheduled or expected",
    "AmortizationReductionGlobalAmount": "Global amount of amortization payment - reduction of credit facility - corresponding to the date",
    "FacilityPrepaymentApplicationCode": "Details how prepayment is applied for the facility - bullet, order of maturity, or client enforced",
    "BorrowerSublimitAmount": "Amount corresponding to sublimit type",
    "BorrowerSublimitTypeCode": "Specific sublimit or maximum amount (if applicable) the Borrower has access to underlying instruments within the credit line / facility (i.e. Letters of Credit, Swingline, Loans, FX, etc.)",
    "PricingLengthOfInterestPeriodText": "Duration of interest period for which the spread is applicable",
    "PricingCreditAdjustmentSpreadPercentage": "Credit adjustment spread value in % per annum",
    "CommitmentAmount": "Citi's commitment / hold amount at close (either for sale or for investment / maturity) per the credit agreement",
    "GlobalSublimitAmount": "Specific sublimit or maximum amount (if applicable) the Borrower has access to under the credit line / facility holistically (i.e. at the facility level)",
    "FeeCurrencyCode": "Currency Code"
}

attribute_description = """ 
CommitmentAmount: Citi's commitment / hold amount at close (either for sale or for investment / maturity) per the credit agreement
ProRataPercentage: Percentage of the respective Issuing / Fronting Bank''s issuing / Fronting commitment amount divided by the total global facility commitment amount available for the specific instrument available

FeeTypeCode: Code classifies fee- counting Accounting Units according to the type of fee that applies.
PricingEffectiveDate: Effective / start / addition date in which this pricing option is available under the facility

Are theses mapped to maximumDrawAmount, minimumDrawAmount, minimumMultiples for FacilityInterestPricingOption?
PricingMaximumDrawAmount: Maximum amount that a single draw / LC request can be made on using the specific pricing type
PricingMinimumDrawAmount: Minimum amount that a single draw / LC request can be made on using the specific pricing type
PricingMinimumMultiplesNumber: Minimum multiple in which a single draw / LC request can be made in for the specific pricing type (e.g. 1mm)

FacilityPrimaryCurrencyCode: Currency Code
FacilityTypeID: Type of facility being reviewed (e.g. revolving credit, term loan A, term loan B, etc.)
FacilityGlobalAmount: Aggregate / total amount of the facility; sum of all lender shares if syndicated; equal to Citi commitment if bilateral loan
FacilityEffectiveDate: Date in which the facility became effective and all CPs are met facility is available for use / draw
FacilityMaturityDate: Date in which the facility matures / terminates after which no new principal can be released and all principal, interest, and fees due from the borrower(s) must be paid in full
FacilityExpirationDate: Date in which the facility may no longer have new loan draws (e.g. term loans that are single draw should expire on the same day as the original draw)
FacilityGlobalCurrentCommitmentAmount: Aggregate / total amount of the facility current amount (both LCs and loans); sum of all lender shares if syndicated; equal to citi commitment if bilateral loan (to feed from Loan IQ)
"""

# !/usr/bin/env python
# coding: utf-8

# In[ ]:


# %pip install --upgrade --quiet google-genai


# In[27]:


import os
import json
from google import genai
from google.genai.types import GenerateContentConfig, Part

PROJECT_ID = "jarvis-365810"
LOCATION = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")

PDF_MIME_TYPE = "application/pdf"
JSON_MIME_TYPE = "application/json"

# MODEL_ID = "gemini-1.5-pro"
MODEL_ID = "gemini-2.0-flash"
# MODEL_ID = "gemini-2.5-pro-preview-05-06"
client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

# In[11]:


from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime


class EntityAttributes(BaseModel):
    entityType: str
    externalId: int
    LIQRefID: Optional[str] = None


class LoanPurpose(BaseModel):
    entityAttributes: EntityAttributes
    creditAgreementId: Optional[int] = None
    facilityId: Optional[int] = None
    id: Optional[int] = None
    loanPurposeCode: Optional[str] = None
    isDeleted: Optional[bool] = None


class LenderShare(BaseModel):
    entityAttributes: EntityAttributes
    creditAgreementId: Optional[int] = None
    facilityId: Optional[int] = None
    id: Optional[int] = None
    isDeleted: Optional[bool] = None
    lenderId: Optional[str] = None
    commitmentAmount: Optional[int] = None
    proRata: Optional[int] = None
    finalAllocation: Optional[int] = None


class FeePricing(BaseModel):
    entityAttributes: EntityAttributes
    creditAgreementId: Optional[int] = None
    facilityId: Optional[int] = None
    id: Optional[int] = None
    feeType: Optional[str] = None
    feeCategory: Optional[str] = None
    globalFeeAmount: Optional[str] = None
    basis: Optional[str] = None
    pricingEffectiveDate: Optional[str] = None
    isDeleted: Optional[bool] = None


class FacilityInterestPricingOption(BaseModel):
    entityAttributes: EntityAttributes
    creditAgreementId: Optional[int] = None
    facilityId: Optional[int] = None
    id: Optional[int] = None
    basis: Optional[str] = None
    maximumDrawAmount: Optional[str] = None
    minimumDrawAmount: Optional[str] = None
    minimumMultiples: Optional[str] = None
    ceiling: Optional[str] = None
    floor: Optional[str] = None
    pricingMaturityDate: Optional[str] = None
    isDeleted: Optional[bool] = None


class Currency(BaseModel):
    code: str
    isPrimary: bool


class FacilityInterestPricing(BaseModel):
    entityAttributes: EntityAttributes
    creditAgreementId: Optional[int] = None
    facilityId: Optional[int] = None
    id: Optional[int] = None
    pricingType: Optional[str] = None
    rateBasis: Optional[str] = None
    spread: Optional[str] = None
    isDeleted: Optional[bool] = None


class DealBorrower(BaseModel):
    entityAttributes: EntityAttributes
    customerExternalId: str
    isPrimaryBorrower: Optional[bool] = None
    isDeleted: Optional[bool] = None


class SigningEntity(BaseModel):
    entityAttributes: EntityAttributes
    branch: str
    processingArea: str


class DealAdmin(BaseModel):
    entityAttributes: EntityAttributes
    customerExternalId: str
    alias: str
    profileType: str


class DealFee(BaseModel):
    entityAttributes: EntityAttributes
    feeType: Optional[str] = None
    effectiveDate: Optional[str] = None
    expiryDate: Optional[str] = None
    frequency: Optional[str] = None
    arrearsAdvance: Optional[str] = None
    amortizingAccrualBased: Optional[str] = None
    nonBusinessDayRule: Optional[str] = None
    isDeleted: Optional[bool] = None


class DealEventFee(BaseModel):
    entityAttributes: EntityAttributes
    eventFeeType: Optional[str] = None
    flatAmountIndicator: Optional[str] = None
    flatAmount: Optional[str] = None
    distributeToAllLendersIndicator: Optional[str] = None
    percentageRate: Optional[Any] = None
    isDeleted: Optional[bool] = None


class HolidayCalendar(BaseModel):
    entityAttributes: EntityAttributes
    code: Optional[str] = None
    isDeleted: Optional[bool] = None


class PricingOption(BaseModel):
    entityAttributes: EntityAttributes
    optionName: Optional[str] = None
    isDeleted: bool


class AlternateIdentification(BaseModel):
    name: Optional[str] = None
    value: Optional[str] = None


class Facility(BaseModel):
    entityAttributes: EntityAttributes
    facilityName: str
    facilityType: str
    effectiveDate: str
    expiryDate: str
    maturityDate: str
    facilityGlobalAmount: str
    closingCommitment: str
    creditAgreementId: int
    facilityId: int
    alternateIdentification: List[AlternateIdentification]
    currencies: Optional[List[Currency]] = None
    isDeleted: Optional[bool] = None


class BankRole(BaseModel):
    value: str
    percent: Optional[Any] = None


class DealBankRole(BaseModel):
    entityAttributes: EntityAttributes
    customerExternalId: Optional[str] = None
    expenseCode: Optional[str] = None
    portfolioCode: Optional[str] = None
    bankRole: Optional[List[BankRole]] = None
    isDeleted: Optional[bool] = None


class Deal(BaseModel):
    entityAttributes: Optional[EntityAttributes] = None
    dealId: str
    dealName: str
    status: Optional[str] = None
    currency: str
    department: str
    expenseCode: Optional[str] = None
    maxNumberOfLoansAllowed: Optional[int] = None
    maxNumberOfUnfundedLoansAllowed: Optional[int] = None
    comments: Optional[str] = None
    eventType: Optional[str] = None
    commitmentSignedDate: Optional[str] = None
    creditAgreementType: Optional[str] = None
    industry: Optional[str] = None
    seniorityType: Optional[str] = None
    commitmentCounterSignedDate: Optional[str] = None
    subIndustry: Optional[str] = None
    leverageLandingType: Optional[str] = None
    globalOrganizationCodeType: Optional[str] = None
    launchDate: Optional[datetime] = None
    regulatorType: Optional[str] = None
    description: Optional[str] = None
    regionOfSyndicationType: Optional[str] = None
    regionOfOriginationType: Optional[str] = None
    creditAgreementDate: Optional[str] = None
    purposeType: Optional[str] = None
    isDeleted: Optional[bool] = None
    alternateIdentification: Optional[List[AlternateIdentification]] = None
    closingDate: Optional[str] = None
    pricingOptions: Optional[List[PricingOption]] = None
    holidayCalendars: Optional[List[HolidayCalendar]] = None
    signingEntity: Optional[SigningEntity] = None
    dealAdmin: Optional[DealAdmin] = None
    dealBorrowers: Optional[List[DealBorrower]] = None
    # dealBankRoles: Optional[List[DealBankRole]] = None
    dealFees: Optional[List[DealFee]] = None
    # dealEventFees: Optional[List[DealEventFee]] = None


class BorrowerDetails(BaseModel):
    entityAttributes: Optional[EntityAttributes] = None
    creditAgreementId: Optional[int] = None
    facilityId: Optional[int] = None
    id: Optional[int] = None
    borrowerId: Optional[str] = None
    isPrimary: Optional[bool] = None
    effectiveDate: Optional[str] = None
    globalSublimit: Optional[str] = None
    isDeleted: Optional[bool] = None


class Counterparty(BaseModel):
    entityAttributes: Optional[EntityAttributes] = None
    isPrimary: Optional[bool] = None
    isDeleted: Optional[bool] = None


class LYNX(BaseModel):
    borrowerDetails: Optional[List[BorrowerDetails]] = None  # Refer Facility Borrower
    lenderShare: Optional[List[LenderShare]] = None  # Refer Lenders
    facilities: Optional[List[Facility]] = None  # fetching only top facilities
    facilityInterestPricingOption: Optional[List[FacilityInterestPricingOption]] = None  # Refer Borrowing Mechanics & Pricing
    # counterparties: Optional[List[Counterparty]] = None  # No info
    # deal: Optional[Deal] = None  # No info
    # facilityInterestPricing: Optional[List[FacilityInterestPricing]] = None  # NA
    # feePricing: Optional[List[FeePricing]] = None  # NA
    # loanPurpose: Optional[List[LoanPurpose]] = None  # NA


# ## Load file bytes

# In[12]:


file_path = "/home/jupyter/docs/sec.gov_Archives_edgar_data_1018724_000110465923113444_tm2329405d1_ex10-1.htm.pdf"
with open(file_path, "rb") as f:
    file_bytes = f.read()

# ## Prompt

# In[13]:


attribute_description = """ 
CommitmentAmount: Citi's commitment / hold amount at close (either for sale or for investment / maturity) per the credit agreement
ProRataPercentage: Percentage of the respective Issuing / Fronting Bank''s issuing / Fronting commitment amount divided by the total global facility commitment amount available for the specific instrument available

FeeTypeCode: Code classifies fee- counting Accounting Units according to the type of fee that applies.
PricingEffectiveDate: Effective / start / addition date in which this pricing option is available under the facility

PricingMaximumDrawAmount: Maximum amount that a single draw / LC request can be made on using the specific pricing type
PricingMinimumDrawAmount: Minimum amount that a single draw / LC request can be made on using the specific pricing type
PricingMinimumMultiplesNumber: Minimum multiple in which a single draw / LC request can be made in for the specific pricing type (e.g. 1mm)

FacilityPrimaryCurrencyCode: Currency Code
FacilityTypeID: Type of facility being reviewed (e.g. revolving credit, term loan A, term loan B, etc.)
FacilityGlobalAmount: Aggregate / total amount of the facility; sum of all lender shares if syndicated; equal to Citi commitment if bilateral loan
FacilityEffectiveDate: Date in which the facility became effective and all CPs are met facility is available for use / draw
FacilityMaturityDate: Date in which the facility matures / terminates after which no new principal can be released and all principal, interest, and fees due from the borrower(s) must be paid in full
FacilityExpirationDate: Date in which the facility may no longer have new loan draws (e.g. term loans that are single draw should expire on the same day as the original draw)
FacilityGlobalCurrentCommitmentAmount: Aggregate / total amount of the facility current amount (both LCs and loans); sum of all lender shares if syndicated; equal to citi commitment if bilateral loan (to feed from Loan IQ)
"""

# In[14]:


# entity_extraction_prompt = """You are a document entity extraction specialist that deals with loan / credit contracts. Given a document, your task is to extract the text value of the entities provided in the schema.
# - The values must only include text found in the document
# - Do not normalize any entity values.
# """

entity_extraction_prompt = f"""
You are an expert at data extraction and structured information processing. Your primary task is to meticulously extract all relevant entities and 
their corresponding attributes from the provided document. Present the extracted data as a single JSON object, strictly adhering to the Pydantic schema. 
If an attribute is defined as Optional and its value is not explicitly found in the document, omit that attribute from the JSON output. 
If multiple instances of a list-type entity (e.g., `facilities`, `loanPurpose`) are found, include them all as a list of objects.

Here are the entity attribute descriptions:
{attribute_description}
"""

# ## Send to Gemini API

# In[15]:


# temp = client.models.generate_content(
#     model=MODEL_ID,
#     contents=[
#         "Provided is a LoanOps Credit Agreement doc. Explain in brief what is covered in the doc.",
#         Part.from_bytes(data=file_bytes, mime_type=PDF_MIME_TYPE),
#     ],
# )
# print(temp.text)


# In[26]:


response = client.models.generate_content(
    model=MODEL_ID,
    contents=[
        "The following document is a LoanOps Credit Agreement doc",
        Part.from_bytes(data=file_bytes, mime_type=PDF_MIME_TYPE),
    ],
    config=GenerateContentConfig(
        # system_instruction=temp.text + entity_extraction_prompt,
        system_instruction=entity_extraction_prompt,
        temperature=0,
        response_schema=LYNX,
        response_mime_type=JSON_MIME_TYPE,
    ),
)

# In[20]:


loan_contract_data = response.parsed
print("\n-------Extracted Entities--------")
print(loan_contract_data)

# In[21]:


json_object = json.loads(response.text)
output_str = json.dumps(json_object, indent=3)
print(output_str)

# In[ ]:


# In[ ]:


# ## 2.5 pro response
{
    "borrowerDetails": [
        {
            "entityAttributes": {
                "entityType": "BORROWER",
                "externalId": 101
            },
            "creditAgreementId": 1,
            "facilityId": 1,
            "id": 1001,
            "borrowerId": "AMAZON.COM, INC.",
            "isPrimary": true,
            "effectiveDate": "2023-11-01",
            "isDeleted": false
        }
    ],
    "lenderShare": [
        {
            "entityAttributes": {
                "entityType": "LENDER",
                "externalId": 201
            },
            "creditAgreementId": 1,
            "facilityId": 1,
            "id": 2001,
            "lenderId": "CITIBANK, N.A.",
            "commitmentAmount": null,
            "proRata": null,
            "finalAllocation": null
        },
        {
            "entityAttributes": {
                "entityType": "LENDER",
                "externalId": 202
            },
            "creditAgreementId": 1,
            "facilityId": 1,
            "id": 2002,
            "lenderId": "BOFA SECURITIES, INC.",
            "commitmentAmount": null,
            "proRata": null,
            "finalAllocation": null
        },
        {
            "entityAttributes": {
                "entityType": "LENDER",
                "externalId": 203
            },
            "creditAgreementId": 1,
            "facilityId": 1,
            "id": 2003,
            "lenderId": "DEUTSCHE BANK SECURITIES INC.",
            "commitmentAmount": null,
            "proRata": null,
            "finalAllocation": null
        },
        {
            "entityAttributes": {
                "entityType": "LENDER",
                "externalId": 204
            },
            "creditAgreementId": 1,
            "facilityId": 1,
            "id": 2004,
            "lenderId": "HSBC SECURITIES (USA), INC.",
            "commitmentAmount": null,
            "proRata": null,
            "finalAllocation": null
        },
        {
            "entityAttributes": {
                "entityType": "LENDER",
                "externalId": 205
            },
            "creditAgreementId": 1,
            "facilityId": 1,
            "id": 2005,
            "lenderId": "JPMORGAN CHASE BANK, N.A.",
            "commitmentAmount": null,
            "proRata": null,
            "finalAllocation": null
        },
        {
            "entityAttributes": {
                "entityType": "LENDER",
                "externalId": 206
            },
            "creditAgreementId": 1,
            "facilityId": 1,
            "id": 2006,
            "lenderId": "WELLS FARGO SECURITIES, LLC",
            "commitmentAmount": null,
            "proRata": null,
            "finalAllocation": null
        },
        {
            "entityAttributes": {
                "entityType": "LENDER",
                "externalId": 207
            },
            "creditAgreementId": 1,
            "facilityId": 1,
            "id": 2007,
            "lenderId": "WELLS FARGO BANK, NATIONAL ASSOCIATION",
            "commitmentAmount": null,
            "proRata": null,
            "finalAllocation": null
        },
        {
            "entityAttributes": {
                "entityType": "LENDER",
                "externalId": 208
            },
            "creditAgreementId": 1,
            "facilityId": 1,
            "id": 2008,
            "lenderId": "BARCLAYS BANK PLC",
            "commitmentAmount": null,
            "proRata": null,
            "finalAllocation": null
        },
        {
            "entityAttributes": {
                "entityType": "LENDER",
                "externalId": 209
            },
            "creditAgreementId": 1,
            "facilityId": 1,
            "id": 2009,
            "lenderId": "BNP PARIBAS",
            "commitmentAmount": null,
            "proRata": null,
            "finalAllocation": null
        },
        {
            "entityAttributes": {
                "entityType": "LENDER",
                "externalId": 210
            },
            "creditAgreementId": 1,
            "facilityId": 1,
            "id": 2010,
            "lenderId": "GOLDMAN SACHS BANK USA",
            "commitmentAmount": null,
            "proRata": null,
            "finalAllocation": null
        },
        {
            "entityAttributes": {
                "entityType": "LENDER",
                "externalId": 211
            },
            "creditAgreementId": 1,
            "facilityId": 1,
            "id": 2011,
            "lenderId": "MORGAN STANLEY SENIOR FUNDING, INC.",
            "commitmentAmount": null,
            "proRata": null,
            "finalAllocation": null
        },
        {
            "entityAttributes": {
                "entityType": "LENDER",
                "externalId": 212
            },
            "creditAgreementId": 1,
            "facilityId": 1,
            "id": 2012,
            "lenderId": "ROYAL BANK OF CANADA",
            "commitmentAmount": null,
            "proRata": null,
            "finalAllocation": null
        },
        {
            "entityAttributes": {
                "entityType": "LENDER",
                "externalId": 213
            },
            "creditAgreementId": 1,
            "facilityId": 1,
            "id": 2013,
            "lenderId": "SOCI\u00c9T\u00c9 G\u00c9N\u00c9RALE",
            "commitmentAmount": null,
            "proRata": null,
            "finalAllocation": null
        },
        {
            "entityAttributes": {
                "entityType": "LENDER",
                "externalId": 214
            },
            "creditAgreementId": 1,
            "facilityId": 1,
            "id": 2014,
            "lenderId": "TD SECURITIES (USA) LLC",
            "commitmentAmount": null,
            "proRata": null,
            "finalAllocation": null
        },
        {
            "entityAttributes": {
                "entityType": "LENDER",
                "externalId": 215
            },
            "creditAgreementId": 1,
            "facilityId": 1,
            "id": 2015,
            "lenderId": "THE BANK OF NOVA SCOTIA",
            "commitmentAmount": null,
            "proRata": null,
            "finalAllocation": null
        },
        {
            "entityAttributes": {
                "entityType": "LENDER",
                "externalId": 216
            },
            "creditAgreementId": 1,
            "facilityId": 1,
            "id": 2016,
            "lenderId": "BANCO BILBAO VIZCAYA ARGENTARIA, S.A. NEW YORK BRANCH",
            "commitmentAmount": null,
            "proRata": null,
            "finalAllocation": null
        },
        {
            "entityAttributes": {
                "entityType": "LENDER",
                "externalId": 217
            },
            "creditAgreementId": 1,
            "facilityId": 1,
            "id": 2017,
            "lenderId": "BANCO SANTANDER, S.A., NEW YORK BRANCH",
            "commitmentAmount": null,
            "proRata": null,
            "finalAllocation": null
        },
        {
            "entityAttributes": {
                "entityType": "LENDER",
                "externalId": 218
            },
            "creditAgreementId": 1,
            "facilityId": 1,
            "id": 2018,
            "lenderId": "BANK OF CHINA, LOS ANGELES BRANCH",
            "commitmentAmount": null,
            "proRata": null,
            "finalAllocation": null
        },
        {
            "entityAttributes": {
                "entityType": "LENDER",
                "externalId": 219
            },
            "creditAgreementId": 1,
            "facilityId": 1,
            "id": 2019,
            "lenderId": "NATIONAL WESTMINSTER BANK PLC",
            "commitmentAmount": null,
            "proRata": null,
            "finalAllocation": null
        },
        {
            "entityAttributes": {
                "entityType": "LENDER",
                "externalId": 220
            },
            "creditAgreementId": 1,
            "facilityId": 1,
            "id": 2020,
            "lenderId": "STANDARD CHARTERED BANK",
            "commitmentAmount": null,
            "proRata": null,
            "finalAllocation": null
        },
        {
            "entityAttributes": {
                "entityType": "LENDER",
                "externalId": 221
            },
            "creditAgreementId": 1,
            "facilityId": 1,
            "id": 2021,
            "lenderId": "U.S. BANK NATIONAL ASSOCIATION",
            "commitmentAmount": null,
            "proRata": null,
            "finalAllocation": null
        }
    ],
    "facilities": [
        {
            "entityAttributes": {
                "entityType": "FACILITY",
                "externalId": 1
            },
            "facilityName": "FIVE-YEAR REVOLVING CREDIT AGREEMENT",
            "facilityType": "Revolving Credit Facility",
            "effectiveDate": "2023-11-01",
            "expiryDate": "2028-11-01",
            "maturityDate": "2028-11-01",
            "facilityGlobalAmount": "15000000000",
            "closingCommitment": "15000000000",
            "creditAgreementId": 1,
            "facilityId": 1,
            "alternateIdentification": [],
            "currencies": [
                {
                    "code": "USD",
                    "isPrimary": true
                },
                {
                    "code": "EUR",
                    "isPrimary": false
                },
                {
                    "code": "GBP",
                    "isPrimary": false
                },
                {
                    "code": "JPY",
                    "isPrimary": false
                },
                {
                    "code": "CAD",
                    "isPrimary": false
                },
                {
                    "code": "AUD",
                    "isPrimary": false
                },
                {
                    "code": "CHF",
                    "isPrimary": false
                }
            ],
            "isDeleted": false
        }
    ],
    "facilityInterestPricingOption": [
        {
            "entityAttributes": {
                "entityType": "FACILITY_INTEREST_PRICING_OPTION",
                "externalId": 301
            },
            "creditAgreementId": 1,
            "facilityId": 1,
            "id": 3001,
            "basis": "Base Rate",
            "minimumDrawAmount": "1000000",
            "minimumMultiples": "500000",
            "isDeleted": false
        },
        {
            "entityAttributes": {
                "entityType": "FACILITY_INTEREST_PRICING_OPTION",
                "externalId": 302
            },
            "creditAgreementId": 1,
            "facilityId": 1,
            "id": 3002,
            "basis": "Term Benchmark USD",
            "minimumDrawAmount": "5000000",
            "minimumMultiples": "1000000",
            "isDeleted": false
        },
        {
            "entityAttributes": {
                "entityType": "FACILITY_INTEREST_PRICING_OPTION",
                "externalId": 303
            },
            "creditAgreementId": 1,
            "facilityId": 1,
            "id": 3003,
            "basis": "Alternative Currency Loan",
            "minimumDrawAmount": "Smallest multiple of 1,000,000 units of the Alternative Currency with a US Dollar Equivalent of USD 5,000,000 or more",
            "minimumMultiples": "Smallest multiple of 1,000,000 units of the Alternative Currency with a US Dollar Equivalent of USD 1,000,000 or more",
            "isDeleted": false
        }
    ]
}
# In[ ]:


## JSON Structure
""""
Your task is to extract information and format it as a JSON object. 
The JSON should strictly adhere to the following structure. Pay close attention to whether a field expects a single object or a list of objects.

{
  "borrowerDetails": {
    "creditAgreementId": "integer | null",
    "facilityId": "integer | null",
    "id": "integer | null",
    "borrowerId": "string | null",
    "isPrimary": "boolean | null",
    "effectiveDate": "string | null (YYYY-MM-DD)",
    "globalSublimit": "string | null",
    "isDeleted": "boolean | null"
  },
  "lenderShares": [ // This indicates a list of objects
    {
      "creditAgreementId": "integer | null",
      "facilityId": "integer | null",
      "id": "integer | null",
      "isDeleted": "boolean | null",
      "lenderId": "string | null",
      "commitmentAmount": "integer | null",
      "proRata": "integer | null",
      "finalAllocation": "integer | null"
    }
  ],
  "facilities": [ // This indicates a list of objects
    {
      "facilityName": "string",
      "facilityType": "string",
      "effectiveDate": "string (YYYY-MM-DD)",
      "expiryDate": "string (YYYY-MM-DD)",
      "maturityDate": "string (YYYY-MM-DD)",
      "facilityGlobalAmount": "string",
      "closingCommitment": "string",
      "creditAgreementId": "integer",
      "facilityId": "integer",
      "alternateIdentification": [ // This indicates a list of objects
        {
          "name": "string | null",
          "value": "string | null"
        }
      ],
      "currencies": [ // This indicates a list of objects (assuming Currency structure)
        { 
          "code": "string", 
          "symbol": "string" 
        }
      ],
      "isDeleted": "boolean | null"
    }
  ],
  "facilityInterestPricingOptions": [ // This indicates a list of objects
    {
      "creditAgreementId": "integer | null",
      "facilityId": "integer | null",
      "id": "integer | null",
      "basis": "string | null",
      "maximumDrawAmount": "string | null",
      "minimumDrawAmount": "string | null",
      "minimumMultiples": "string | null",
      "ceiling": "string | null",
      "floor": "string | null",
      "pricingMaturityDate": "string | null (YYYY-MM-DD)",
      "isDeleted": "boolean | null"
    }
  ]
}

Extract the relevant information from the following text and provide the output as a JSON object strictly adhering to the schema provided above. Ensure all fields are included, even if null.

[Your input text here, e.g., details about a credit agreement, borrower, etc.]
"""

prompt_v2 = """
You are an expert financial and legal analyst. Your task is to precisely extract factual data points from the provided Credit Agreement document. Precision and completeness are paramount.

**Extraction Instructions:**

1.  **Comprehensive Document Review:**
    * Read the entire Credit Agreement meticulously to understand its full scope, parties, and transaction structure. Identify key sections like Definitions, Commitments, and Facility details.

2.  **Semantic Understanding over Literal Matching:**
    * **Do not rely solely on exact keyword matches.** Deeply interpret the **meaning and intent** of the language. Recognize synonyms, varied phrasing, and concepts rephrased throughout the document (e.g., "effective date" could be "dated as of," "commencement date").
    * **Contextual Interpretation:** Understand terms based on their surrounding text. A "limit" may mean different things in different sections (draw limit vs. total amount).
    * **Infer Implicit Information:** Some information may be implied (e.g., the consistently named "Borrower" is the primary one).

3.  **Targeted Entity Identification & Precision:**
    * Actively search for each required entity's value. Prioritize explicitly stated and quantifiable information.
    * **Numerical & Date Values:** Extract numbers accurately. Standardize all dates to `YYYY-MM-DD` format. Capture monetary values as strings including their currency (e.g., "$100,000,000").
    * **Boolean Logic:** Determine `true`/`false` for boolean flags based on explicit or clear implicit indicators (e.g., `isDeleted` is false unless explicitly stated otherwise).

4.  **Handle Multiple Instances:**
    * Identify and extract **every distinct instance** of entities that can appear multiple times (e.g., all lenders, all facilities). Meticulously process information presented in different section, tables (each row is a record) or as enumerated lists.
    * If an entity or a specific field is **genuinely not present**, explicitly stated as "N/A," or cannot be confidently determined due to ambiguity, set its value to `null`. **Do not infer, invent, or hallucinate.**

5.  **Output Format:**
    * Provide only the extracted information following the specified JSON structure template. No summaries, interpretations, or conversational text. Begin directly with the JSON.
"""
