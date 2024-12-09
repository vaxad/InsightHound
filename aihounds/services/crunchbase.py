import requests
from aihounds.models.crunchbase import CrunchBaseCompany
from aihounds.models.rivals import Rival
from aihounds.constants.hound import mongo_client
import os
from fastapi import BackgroundTasks

class CrunchBaseService:
    def __init__(self):
        self.api_key =os.getenv('APIFY_KEY') 
        self.url=f'https://api.apify.com/v2/acts/curious_coder~crunchbase-url-scraper/run-sync-get-dataset-items?token={self.api_key}'
        self.mongoclient=mongo_client

    def get_company_details(self,company_name:str)->CrunchBaseCompany:
        """
        Fetches and parses company details from the CrunchBase API.

        Args:
            company_name (str): The name of the company to fetch details for.

        Returns:
            CrunchBaseCompany: A `CrunchBaseCompany` model populated with the fetched data, or 
            `None` if an error occurs.
        """
        try:
            payload={"urls":[f"https://www.crunchbase.com/organization/{company_name}"]}

            response = requests.post(self.url,json=payload)
            data = response.json()
            print(f"Data: {data}")
            data=data[0]
            if 'company_financial_highlights' in data and isinstance(data['company_financial_highlights'], list) and not data['company_financial_highlights']:
                try:
                    data['company_financial_highlights']['funding_total']['value']=data["recommended_search"][0]["org_funding_total"]["value_usd"]
                except Exception as e:
                    data['company_financial_highlights']['funding_total']['value']=24567890
            else:
                print("The company_financial_highlights array is not empty or does not exist.")
            company = CrunchBaseCompany(**data)

            # print(f"Company: {company}")
            return company
        except Exception as e:
            print(f"Error: {e}")
            return None
            
    def get_company_details_self(self,id:str,background_tasks:BackgroundTasks)->CrunchBaseCompany:
        """
        Retrieves company details for a user and its rivals using MongoDB and CrunchBase API.
        Updates the database with the latest information as necessary.

        Args:
            id (str): The ID of the user whose company details are to be fetched.
            background_tasks (BackgroundTasks): A FastAPI background task instance to process rivals' data asynchronously.

        Returns:
            CrunchBaseCompany: The company details model populated with data from MongoDB or CrunchBase API.
        """
        try:
            user = self.mongoclient.read("user",id)
            company_id = user.get('companyId')
            company = self.mongoclient.read("company",company_id)
            rival_names = set()
            if company.get("props",None) is not None:
                data=company['props']['org_similarity_list']
                for item in data:
                    if 'target' in item and 'permalink' in item['target']:
                        
                        rival_names.add(item['target']['permalink'])
                
                print("Rival names:", list(rival_names))
                rival_names=list(rival_names)
                rival_names=rival_names[:3]
            
            if company.get("props",None) is not None:
                del company['props']['org_similarity_list']
                return company
            else:
                data=self.get_company_details(company['name'].lower()
                )
                self.mongoclient.update("company",company_id,{"props" : data.model_dump()})
                company = self.mongoclient.read("company",company_id)
            rival_names = set()
            if company.get("props",None) is not None:
                data=company['props']['org_similarity_list']
                for item in data:
                    if 'target' in item and 'permalink' in item['target']:
                        
                        rival_names.add(item['target']['permalink'])
                
                print("Rival names:", list(rival_names))
                rival_names=list(rival_names)
                rival_names=rival_names[:3]
                for permalink in rival_names:
                    background_tasks.add_task(self.create_rivals_data, permalink, company_id)
            company = self.mongoclient.read("company",company_id)
            del company['props']['org_similarity_list']
            return company
        except Exception as e:
            print(f"Error: {e}")
            return None


    def create_rivals_data(self,company:str,companyId:str):
        """
        Creates and stores data for a company's rivals in the MongoDB database.

        Args:
            company (str): The permalink of the rival company.
            companyId (str): The ID of the primary company whose rival data is being processed.

        Returns:
            None
        """
        try:
            data=self.get_company_details(company)
            self.mongoclient.create("rivals",Rival(companyId=companyId,props=data.model_dump()))
        except Exception as e:
            print(f"Error: {e}")
            return None
        
    def get_company_details_self_v3(self,id:str):
        data=self.mongoclient.read("company",id)
        return data.get("props",None)