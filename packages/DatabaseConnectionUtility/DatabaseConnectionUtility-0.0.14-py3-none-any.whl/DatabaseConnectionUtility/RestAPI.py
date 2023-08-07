
import os, requests, json
import pandas as pd
import loggerutility as logger

class RestAPI:
    def testAPI(self, dbDetails):
        
        if 'URL' in dbDetails.keys():
            if dbDetails.get('URL') != None:
                url = dbDetails['URL']
        
        if 'KEY' in dbDetails.keys():
            if dbDetails.get('KEY') != None:
                apiToken = dbDetails['KEY']

        if 'AUTHENTICATION_TYPE' in dbDetails.keys():
            if dbDetails.get('AUTHENTICATION_TYPE') != None:
                authenticationType = dbDetails['AUTHENTICATION_TYPE']
        
        if 'NAME' in dbDetails.keys():
            if dbDetails.get('NAME') != None:
                userName = dbDetails['NAME']
        
        if 'LOGIN_URL' in dbDetails.keys():
            if dbDetails.get('LOGIN_URL') != None:
                loginUrl = dbDetails['LOGIN_URL']
        
        try:
            if authenticationType == "N":
                response = requests.get(url)
                if str(response.status_code) == '200':
                    logger.log(f"{response.url} -- {response} ","0")
                    return str(response.status_code)
                else:
                    logger.log(f"Invalid response for {response.url} {str(response)}","0")
                    raise Exception(f"Invalid response {str(response.status_code)} for {response.url}")

            elif authenticationType == "T":
                logger.log(f"Inside token-based condition","0")
                response = requests.request("POST",url + "?key="+ apiToken)
                if str(response.status_code) == '200':
                    logger.log(f"{response.url} -- {response} ","0")
                    return str(response.status_code)
                else:
                    logger.log(f"Invalid response for {response.url} {str(response)}","0")
                    raise Exception(f"Invalid response for {response.url} {str(response)}")

            elif authenticationType == "S":
                try:
                    session= requests.Session()
                    formParam = {'USER_CODE': userName, 'PASSWORD': apiToken, 'DATA_FORMAT':'JSON','APP_ID': 'INSIGHTCON'  }
                    logger.log(f"formParam session login::::{formParam}","0")
                    logger.log(f"Type-S loginUrl::{loginUrl}","0")
                    
                    response = session.post(loginUrl , formParam)
                    logger.log(f"response.status_code::{response.status_code}","0")
                    if str(response.status_code) == '200':
                        status = (json.loads(response.text))['Response']['status']
                        if status == 'success':
                            logger.log(f"Session based login successful","0")
                            return str(response.status_code)

                        elif status == 'error':
                            logger.log(f"session login response :: {json.loads(response.text)}","0")
                            errorMessage = str(json.loads(response.text)['Response']['results'])
                            logger.log(f"session login errorMessage :: {errorMessage}{type(errorMessage)}","0")
                            raise Exception(errorMessage)
                    else:
                        logger.log(f"Session Based Authentication Response: {str(response.status_code)}","0")
                    
                except Exception as e:
                    logger.log(f'\n Print exception returnSring inside auth_type-S : {e}', "0")
                    raise e

            else:
                logger.log(f"Invalid authenticationType::{authenticationType}","0")
                
        except Exception as e:
            logger.log(f"exception in RestAPI:: {e}","0")
            raise e

    def getData(self, calculationData):
        columnNameList=[]
        jsonDataResponse=""
        functionName=""
        paramLst, key_list, value_list=[],[],[]
        
        logger.log(f"inside RestAPI getData() calculationData::{calculationData}","0")
        if 'dbDetails' in calculationData.keys() and calculationData.get('dbDetails') != None:
            if 'AUTHENTICATION_TYPE' in calculationData['dbDetails'] and calculationData.get('dbDetails')['AUTHENTICATION_TYPE'] != None:
                authentication_Type = calculationData['dbDetails']['AUTHENTICATION_TYPE']

            if 'URL' in calculationData['dbDetails'] and calculationData.get('dbDetails')['URL'] != None:
                serverUrl = calculationData['dbDetails']['URL']

            if 'NAME' in calculationData['dbDetails'] and calculationData.get('dbDetails')['NAME'] != None:
                userName = calculationData['dbDetails']['NAME']

            if 'KEY' in calculationData['dbDetails'] and calculationData.get('dbDetails')['KEY'] != None:
                password = calculationData['dbDetails']['KEY']
            
            if 'source_sql' in calculationData.keys():
                if calculationData.get('source_sql') != None:
                    main_sqlQuery = calculationData['source_sql']
            
            if 'LOGIN_URL' in calculationData['dbDetails'] and calculationData.get('dbDetails')['LOGIN_URL'] != None:
                loginUrl = calculationData['dbDetails']['LOGIN_URL']


        if authentication_Type == 'N':               
            try:
                response = requests.get(serverUrl)
                if str(response.status_code) == '200':
                    logger.log(f"{response.url} -- {response} ","0")
                    jsonDataResponse = response.json()
                    logger.log(f"No-Auth jsonDataResponse : {jsonDataResponse}","0")
                else:
                    logger.log(f"No-Authentication Type Response: {str(response.status_code)}","0")
            except Exception as e:
                logger.log(f'\n Print exception returnString inside auth_type-N : {e}', "0")
                raise Exception(e)

        elif authentication_Type == 'T':      
            try:
                response = requests.request("POST",serverUrl + "?key="+ password)
                if str(response.status_code) == '200':
                    logger.log(f"{response} ","0")
                    jsonDataResponse = response.json()
                    logger.log(f"Auth_Type-T jsonDataResponse : {jsonDataResponse}","0")
                else:
                    logger.log(f"Auth_Type-T Response: {str(response.status_code)}","0")
            except Exception as e:
                logger.log(f'\n Print exception returnSring inside auth_type-T : {e}', "0")
                raise Exception(e)

        elif authentication_Type == 'S':   
            try:
                sqlQuery = main_sqlQuery
                logger.log(f"source_sql query::::{sqlQuery}","0")
                    
                if "where" in sqlQuery:
                    functionName = sqlQuery[sqlQuery.find("from")+4 : sqlQuery.find("where")].strip()
                    logger.log(f"RestAPI getData() functionName where::{functionName}","0")
                else:
                    functionName = sqlQuery[sqlQuery.find("from")+4 :].strip()
                    logger.log(f"RestAPI getData() functionName from::{functionName}","0")

                if "where" in sqlQuery:
                    new_sql= sqlQuery[sqlQuery.find("where")+5:].strip()
                    logger.log(f"new_sql::{new_sql}","0")
                    if "and" in new_sql:
                        new_sql1=new_sql.split("and")
                        paramLst=[i.strip() for i in new_sql1]
                        logger.log(f"paramLst::{paramLst}","0")
                    else:
                        paramLst.append(new_sql)
                        logger.log(f"paramLst else::{paramLst}","0")

                for i in paramLst:
                    element=i.split("=")
                    key_list.append(element[0])
                    value_list.append(element[1].strip()[1:-1])
                logger.log(f"vlaue: {value_list}","0")
                logger.log(f"key: {key_list}","0")
                

                session= requests.Session()
                formParam = {'USER_CODE': userName, 'PASSWORD': password, 'DATA_FORMAT':'JSON','APP_ID': 'INSIGHTCON'  }
                logger.log(f"RestAPI getData() formParam  ::::{formParam}","0")
                logger.log(f" RestAPI getData() TYPE_S serverUrl :::::{serverUrl}","0")
                
                for i in range(len(paramLst)):
                    formParam[key_list[i].upper()] = value_list[i]
                logger.log(f"Rest_API formParam getData() line 204::::{formParam}","0")
            
                response = session.post(loginUrl , formParam)
                if str(response.status_code) == '200':
                    status = (json.loads(response.text))['Response']['status']
                    if status == 'success':
                        logger.log(f"Session based login successful","0")
                        cookie = response.cookies
                        tokenId = json.loads((json.loads(response.text))['Response']['results'])['TOKEN_ID'] 
                        logger.log(f" RestAPI getData() TYPE_S cookie :::::{cookie} tokenid:::::::{tokenId}","0")
                        
                        serverUrl = serverUrl + "/" + functionName if serverUrl[-1] != "/" else serverUrl +  functionName
                        
                        formParam['TOKEN_ID']  = tokenId
                        logger.log(f"Rest_API formParam getData() line 220::::{formParam}","0")
                        response = session.post(serverUrl , formParam, cookies=cookie)
                        logger.log(f"Rest_API Type-S raw responseee ::: {response.text} \n","0")
                        response = json.loads(response.text)
                        logger.log(f"responseeeww ::: {response} \n","0")
                        status = response['Response']['status']
                        if status == "success":
                            jsonDataResponse=response['Response']['results']
                        elif status == "error":
                            errorMessage=json.loads(response['Response']['results'])['Root']['Errors']['error']['description']
                            logger.log(f"Rest_API Type-S responseee ::: {jsonDataResponse} \n{type(jsonDataResponse)}","0")
                            raise Exception(errorMessage)
                        
                        jsonDataResponse=json.loads(jsonDataResponse)
                        logger.log(f"Rest_API Type-S responseee after convert  ::: {jsonDataResponse} \n{type(jsonDataResponse)}","0")
                        
                        
                    elif status == 'error':
                        logger.log(f"visualList type-S : {json.loads(response.text)}","0")
                        return json.loads(response.text)
                        
                else:
                    logger.log(f"Session Based Authentication Response: {str(response.status_code)}","0")
                
            except Exception as e:
                logger.log(f'\n Print exception returnSring inside auth_type-S : {e}', "0")
                raise Exception(e)
        
        logger.log(f"jsonDataResponse::{jsonDataResponse}","0")
        if functionName == "getVisualData":
            dfObject = pd.DataFrame(jsonDataResponse[1:])
        else:
            dfObject = pd.DataFrame(jsonDataResponse)
        logger.log(f"dfObject::{dfObject}","0")

        columnNameStr= main_sqlQuery[7:main_sqlQuery.find("from")].strip()
        if "," in columnNameStr:
            columnNameStr=columnNameStr.split(",")
            columnNameList=[i.strip() for i in columnNameStr]
            dfObject = dfObject[columnNameList]
            logger.log(f" RestAPI no-AuthenticationType df:: {dfObject}","0")
        elif "*" in columnNameStr:
            pass
        else:
            dfObject = dfObject[columnNameStr].to_frame()  

        return dfObject

            
        
            
        
