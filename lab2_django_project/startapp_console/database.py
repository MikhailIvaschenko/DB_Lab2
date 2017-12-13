import MySQLdb as mdb
import os
from django.shortcuts import HttpResponse



class Connector(object):
    def __init__(self, host='localhost', user='root', password='qwerty', dbname='communal_payments_database'):
        self.Errors = ""
        self.__Status = False
        self.accountsKeys = []
        self.brdKeys = []
        self.caKeys = []
        self.nomKeys = []
        self.columnsToBeDisplayed = ('opCA_name', 'opNom_name', 'opBRD_id', 'opAC_id')
        try:
            self.Connection = mdb.connect(host, user, password, dbname)
            self.Cursor = self.Connection.cursor()
            self.__initSelectQueriesToLists()
            self.Status = True
        except Exception as risenException:
            self.Errors = risenException.__str__()
            self.Status = False
            if self.Connection:
                self.Connection.close()

    def __initSelectQueriesToLists(self):
        self.Cursor.execute("SELECT acID FROM accounts")
        rows = self.Cursor.fetchall()
        for row in rows:
            self.accountsKeys.append(row[0])

        self.Cursor.execute("SELECT brdID FROM brd")
        rows = self.Cursor.fetchall()
        for row in rows:
            self.brdKeys.append(row[0])

        self.Cursor.execute("SELECT caName FROM counteragents")
        rows = self.Cursor.fetchall()
        for row in rows:
            self.caKeys.append(row[0])

        self.Cursor.execute("SELECT nomName FROM nomenclatures")
        rows = self.Cursor.fetchall()
        for row in rows:
            self.nomKeys.append(row[0])

    def getMainTable(self):
        if self.Status:
            self.Cursor.execute("SELECT opCA_name, opNom_name, opBRD_id, opAC_id FROM operations")
            rows = self.Cursor.fetchall()
            return rows
        else:
            self.Errors = "Connection is not established!"
            return None

    def getFormsetData(self):
        if self.Status:
            try:
                data = {}
                insertdata = {}
                rows = self.getMainTable()
                rowsNumber = len(rows)
                formCounter = 0
                columnCounter = 0

                data.update({
                    'form-TOTAL_FORMS': rowsNumber.__str__(),
                    'form-INITIAL_FORMS': '0',
                    'form-MAX_NUM_FORMS': '', })

                for row in rows:
                    insertdata.clear()

                    columnCounter = 0
                    for field in row:
                        insertdata.update({'form-' + formCounter.__str__() + "-" + self.columnsToBeDisplayed[columnCounter]: field.__str__()})
                        columnCounter += 1
                    data.update(insertdata)
                    formCounter += 1
                return data
            except Exception as ex:
                self.Errors = ex.__str__()
                return None
        else:
            self.Errors = "Connection is not established!"
            return None

    def getDataFromList(self, field, table):
        result = []
        self.Cursor.execute("SELECT " + field + " FROM " + table + " GROUP BY " + field)
        rows = self.Cursor.fetchall()
        for row in rows:
            result.append((row[0], row[0]))
        return result
    def getList(self, keysList):
        result = []
        for key in keysList:
            result.append((key, key))
        return result

    def Update(self, previousArgs, newArgs):
        if self.Status:
            try:
                columnCounter = 0
                Query = "UPDATE operations SET "
                for arg in newArgs:
                    Query += self.columnsToBeDisplayed[columnCounter] + " = '" + arg.__str__() + "', "
                    columnCounter += 1
                Query = Query[0:len(Query)-2] + " WHERE "
                columnCounter = 0
                for arg in previousArgs:
                    Query += self.columnsToBeDisplayed[columnCounter] + " = '" + arg.__str__() + "' AND "
                    columnCounter += 1
                Query = Query[0:len(Query)-5]
                self.Cursor.execute(Query)
                self.Connection.commit()
                return True
                #return Query
            except Exception as ex:
                self.Errors = ex.__str__()
                return False
                #return Query
        else:
            self.Errors = "Connection is not established!"
            return False

    def Delete(self, args):
        if self.Status:
            try:
                Query = "DELETE FROM operations WHERE "
                columnCounter = 0
                for arg in args:
                    Query += self.columnsToBeDisplayed[columnCounter] + " = '" + arg.__str__() + "' AND "
                    columnCounter += 1
                Query = Query[0:len(Query) - 5]
                self.Cursor.execute(Query)
                self.Connection.commit()
                return True
            except Exception as ex:
                self.Errors = ex.__str__()
                return False
        else:
            self.Errors = "Connection is not established!"
            return False

    def Add(self, args):
        if self.Status:
            try:
                Query = "INSERT INTO operations ("
                for field in self.columnsToBeDisplayed:
                    Query += field.__str__() + ", "
                Query = Query[0:len(Query)-2] + ") VALUES ("
                for arg in args:
                    Query +="'"+ arg.__str__() + "', "
                Query = Query[0:len(Query)-2] + ")"
                self.Cursor.execute(Query)
                self.Connection.commit()
                #return Query
                return True
            except Exception as ex:
                self.Errors = ex.__str__()
                #return Query
                return False
        else:
            self.Errors = "Connection is not established!"
            return False

    def ParseXMLAccounts(self, File=""):
        if File == "":
            File = os.getcwd() + "\\startapp_console\\xmls\\Accounts.xml"
        file = open(File, 'r')
        if file is None:
            return
        if self.Status == False:
            return
        data = ["", "", "", "", "", ""]
        stringBuffer = "INSERT INTO accounts VALUES ('"
        for line in file:
            line = line.strip()
            allow = True
            if line.startswith("<row>") or line.startswith("</row") or line.startswith("<dataset>") or line.startswith("</dataset>") or line.startswith("<?xml"):
                continue
            elif line.startswith("<acID>"):
                line = line.replace("<acID>", "")
                line = line.replace("</acID>", "")
                data[0] = line
            elif line.startswith("<acDate>"):
                line = line.replace("<acDate>", "")
                line = line.replace("</acDate>", "")
                data[1] = line
            elif line.startswith("<acOperation_type>"):
                line = line.replace("<acOperation_type>", "")
                line = line.replace("</acOperation_type>", "")
                data[2] = line
            elif line.startswith("<acPrice>"):
                line = line.replace("<acPrice>", "")
                line = line.replace("</acPrice>", "")
                data[3] = line
            elif line.startswith("<acCurrency>"):
                line = line.replace("<acCurrency>", "")
                line = line.replace("</acCurrency>", "")
                data[4] = line
            elif line.startswith("<acGoods_type>"):
                line = line.replace("<acGoods_type>", "")
                line = line.replace("</acGoods_type>", "")
                data[5] = line


            for d in data:
                if d == "":
                    allow = False
                    break
            if allow:
                for item in data:
                    stringBuffer += item.__str__() + "', '"
                stringBuffer = stringBuffer[:len(stringBuffer)-3]
                stringBuffer += ")"

                try:
                    self.Cursor.execute(stringBuffer)
                    #self.Cursor.execute("INSERT INTO accounts VALUES (" + data[0].__str__() + ", '" + data[1].__str__() + "', '" + data[2].__str__() + "')")
                    self.Connection.commit()
                except:
                    pass
                data = ["", "", "", "", "", ""]
        file.close()

    def ParseXMLBRD(self, File=""):
        if File == "":
            File = os.getcwd() + "\\startapp_console\\xmls\\BRD.xml"
        file = open(File, 'r')
        if file is None:
            return
        if self.Status == False:
            return
        data = ["", "", "", "", ""]
        stringBuffer = "INSERT INTO brd VALUES ('"
        for line in file:
            line = line.strip()
            allow = True
            if line.startswith("<row>") or line.startswith("</row") or line.startswith("<dataset>") or line.startswith("</dataset>") or line.startswith("<?xml"):
                continue
            elif line.startswith("<brdID>"):
                line = line.replace("<brdID>", "")
                line = line.replace("</brdID>", "")
                data[0] = line
            elif line.startswith("<brdPrice>"):
                line = line.replace("<brdPrice>", "")
                line = line.replace("</brdPrice>", "")
                data[1] = line
            elif line.startswith("<brdCurrency>"):
                line = line.replace("<brdCurrency>", "")
                line = line.replace("</brdCurrency>", "")
                data[2] = line
            elif line.startswith("<brdOperation_types>"):
                line = line.replace("<brdOperation_types>", "")
                line = line.replace("</brdOperation_types>", "")
                data[3] = line
            elif line.startswith("<brdOrganization_name>"):
                line = line.replace("<brdOrganization_name>", "")
                line = line.replace("</brdOrganization_name>", "")
                data[4] = line

            for d in data:
                if d == "":
                    allow = False
                    break
            if allow:
                for item in data:
                    stringBuffer += item.__str__() + "', '"
                stringBuffer = stringBuffer[:len(stringBuffer)-3]
                stringBuffer += ")"

                try:
                    self.Cursor.execute(stringBuffer)
                    #self.Cursor.execute("INSERT INTO accounts VALUES (" + data[0].__str__() + ", '" + data[1].__str__() + "', '" + data[2].__str__() + "')")
                    self.Connection.commit()
                except:
                    pass
                data = ["", "", "", "", ""]
        file.close()

    def ParseXMLCounteragents(self, File=""):
        if File == "":
            File = os.getcwd() + "\\startapp_console\\xmls\\CounterAgents.xml"
        file = open(File, 'r')
        if file is None:
            return
        if self.Status == False:
            return
        data = ["", "", "", "", "", ""]
        stringBuffer = "INSERT INTO counteragents VALUES ('"
        for line in file:
            line = line.strip()
            allow = True
            if line.startswith("<row>") or line.startswith("</row") or line.startswith("<dataset>") or line.startswith("</dataset>") or line.startswith("<?xml"):
                continue
            elif line.startswith("<caName>"):
                line = line.replace("<caName>", "")
                line = line.replace("</caName>", "")
                data[0] = line
            elif line.startswith("<caUKTZED_code>"):
                line = line.replace("<caUKTZED_code>", "")
                line = line.replace("</caUKTZED_code>", "")
                data[1] = line
            elif line.startswith("<caScheme>"):
                line = line.replace("<caScheme>", "")
                line = line.replace("</caScheme>", "")
                data[2] = line
            elif line.startswith("<caITC>"):
                line = line.replace("<caITC>", "")
                line = line.replace("</caITC>", "")
                data[3] = line

            for d in data:
                if d == "":
                    allow = False
                    break
            if allow:
                for item in data:
                    stringBuffer += item.__str__() + "', '"
                stringBuffer = stringBuffer[:len(stringBuffer)-3]
                stringBuffer += ")"

                try:
                    self.Cursor.execute(stringBuffer)
                    self.Connection.commit()
                except:
                    pass
                data = ["", "", "", "", "", ""]
        file.close()

    def ParseXMLNomenclatures(self, File=""):
        if File == "":
            File = os.getcwd() + "\\startapp_console\\xmls\\Nomenclatures.xml"
        file = open(File, 'r')
        if file is None:
            return
        if self.Status == False:
            return
        data = ["", "", "", "", "", "", ""]
        stringBuffer = "INSERT INTO nomenclatures VALUES ('"
        for line in file:
            line = line.strip()
            allow = True
            if line.startswith("<row>") or line.startswith("</row") or line.startswith("<dataset>") or line.startswith("</dataset>") or line.startswith("<?xml"):
                continue
            elif line.startswith("<nomName>"):
                line = line.replace("<nomName>", "")
                line = line.replace("</nomName>", "")
                data[0] = line
            elif line.startswith("<nomVendore_code>"):
                line = line.replace("<nomVendore_code>", "")
                line = line.replace("</nomVendore_code>", "")
                data[1] = line
            elif line.startswith("<nomMU>"):
                line = line.replace("<nomMU>", "")
                line = line.replace("</nomMU>", "")
                data[2] = line
            elif line.startswith("<nomVAT_rate>"):
                line = line.replace("<nomVAT_rate>", "")
                line = line.replace("</nomVAT_rate>", "")
                data[3] = line
            elif line.startswith("<nomUKTZED_code>"):
                line = line.replace("<nomUKTZED_code>", "")
                line = line.replace("</nomUKTZED_code>", "")
                data[4] = line
            elif line.startswith("<nomStock_type>"):
                line = line.replace("<nomStock_type>", "")
                line = line.replace("</nomStock_type>", "")
                data[5] = line
            elif line.startswith("<Description>"):
                line = line.replace("<Description>", "")
                line = line.replace("</Description>", "")
                data[6] = line

            for d in data:
                if d == "":
                    allow = False
                    break
            if allow:
                for item in data:
                    stringBuffer += item.__str__() + "', '"
                stringBuffer = stringBuffer[:len(stringBuffer)-3]
                stringBuffer += ")"

                try:
                    self.Cursor.execute(stringBuffer)
                    #self.Cursor.execute("INSERT INTO accounts VALUES (" + data[0].__str__() + ", '" + data[1].__str__() + "', '" + data[2].__str__() + "')")
                    self.Connection.commit()
                except:
                    pass
                data = ["", "", "", "", "", "", ""]
        file.close()

    def getQueryDictionary(self, Query, Columns):
        if self.Status:
            try:
                data = {}
                insertdata = {}
                self.Cursor.execute(Query)
                rows = self.Cursor.fetchall()
                n = len(rows)
                Ocounter = 0
                Icounter = 0

                data.update({
                    'form-TOTAL_FORMS': n.__str__(),
                    'form-INITIAL_FORMS': '0',
                    'form-MAX_NUM_FORMS': '', })

                for row in rows:
                    insertdata.clear()
                    Icounter = 0
                    for field in row:
                        insertdata.update({'form-' + Ocounter.__str__() + "-" + Columns[Icounter]: field.__str__()})
                        Icounter += 1
                    data.update(insertdata)
                    Ocounter += 1
                return data
            except Exception as ex:
                self.Errors = ex.__str__()
                return None
        else:
            self.Errors = "Connection is not established!"
            return None

def commitTextSearch(requestPost, connector, field, table, Columns, matchArgument, valueProcessArgumentStart):
        if field in requestPost:
            val = requestPost[field]
        Query = "SELECT * FROM " + table + " WHERE" + matchArgument + "MATCH (Description) AGAINST (" + valueProcessArgumentStart + val.__str__() + "\"' IN BOOLEAN MODE)"
        return connector.getQueryDictionary(Query, Columns)

def combineCAwithMaxAcSum(requestPost):
    Query = "SELECT caName, max(result) from counterAgents join (operations join accounts on operations.opAC_id = accounts.acID) on counterAgents.caName = operations.opCA_name"

def combineRows(requestPost, connector, field, table, Columns, queryType):
        if queryType == 1:
            if field in requestPost:
                val = requestPost[field]
            Query = "SELECT * FROM " + table + " WHERE " + field + " = \'" + val.__str__() + '\''
            return connector.getQueryDictionary(Query, Columns)
        elif queryType == 2:
            leftBoarder = field.__str__() + "Left"
            rightBoarder = field.__str__() + "Right"
            if leftBoarder in requestPost:
                From = requestPost[leftBoarder]
            if rightBoarder in requestPost:
                To = requestPost[rightBoarder]

            Query = "SELECT * FROM " + table + " WHERE " + field + " BETWEEN '" + From.__str__() + "' AND '" + To.__str__() + "'"
            #Query = "SELECT * FROM accounts WHERE acDate BETWEEN '" + From.__str__() + "' AND '" + To.__str__() + "'"
            return connector.getQueryDictionary(Query, Columns)





 #brds columns