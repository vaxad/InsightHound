from pydantic import BaseModel
from typing import Optional, Any,List

class CrunchBaseCompany(BaseModel):
    short_description:Optional[str]
    title:Optional[str]
    key_employee_change_list:Optional[List[Any]]=None
    current_employees_summary:Optional[Any]=None
    funds_summary:Optional[Any]=None
    current_advisors_image_list:Optional[List[Any]]=None
    org_funding_total:Optional[Any]=None
    org_num_investors:Optional[int]=None
    org_similarity_list:Optional[List[Any]]=None
    company_financials_highlights:Optional[Any]=None
    investors_list:Optional[List[Any]]=None