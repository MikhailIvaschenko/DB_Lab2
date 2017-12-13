from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django import forms
from django.forms import formset_factory
from django.views.decorators.csrf import csrf_protect

import re
import Scripts.lab2_django_project.startapp_console.models as FormClasses
import Scripts.lab2_django_project.startapp_console.database as Database
from Scripts.lab2_django_project.startapp_console.models import mainConnector
data = None
previousArgs = []


#methods' declarations
def resetData():
    global data
    global mainConnector
    data = mainConnector.getFormsetData()

def showMainTable(request):
    global data
    resetData()

    formSetBuilder = formset_factory(FormClasses.MainFormTable, extra=(len(data) - 3) / 3) #automatically collects the table : template=MainFormTable; count = extra=(len(data) - 3) / 3)
    filledFormSet = formSetBuilder(data)

    formResponse = {'Formset':filledFormSet}
    return render(request, 'Table.html', formResponse) #return page template filled with formResponse

def showSearchTable(request):
    acDSform = FormClasses.ACTDateSearch() #filter data between two values => l.w. task
    acCSform = FormClasses.ACTCurrencySearch() #get the records with the set currency
    acPFform = FormClasses.BRDTPriceFilter() #filter by price values
    brdOSform = FormClasses.BRDTOrgSearch() #get the records with the set organization
    caCSform = FormClasses.CATCodeSearch() #get the records with the set code
    caSSform = FormClasses.CATSchemeSearch() #get the records with the set scheme
    nomMUSform = FormClasses.NOMTMUSearch() #get the records with the set measure units
    nomFTSPhraseForm = FormClasses.NOMTFTPhraseSearch() #full text serach by a phrase => l.w. task
    nomFTSWordForm = FormClasses.NOMTFTWordSearch() #full text serach by a word => l.w. task

    return render(request, 'Search.html', {'form0': acDSform, 'form1': acCSform, 'form2': acPFform, 'form3': brdOSform,
                                           'form4': caCSform, 'form5': caSSform, 'form6': nomMUSform, 'form7': nomFTSPhraseForm,
                                           'form8': nomFTSWordForm})


def acDateSearch(request):
    rows = Database.combineRows(request.POST, mainConnector, FormClasses.AccountsTable.acDate, FormClasses.AccountsTable.acTable, FormClasses.AccountsTable.acColumns, 2)

    formSetBuilder = formset_factory(FormClasses.AccountsForm, extra=(len(rows) - 3) / 3)
    filledFormSet = formSetBuilder(rows)

    response = {}
    response['Formset'] = filledFormSet
    return render(request, 'SimpleTable.html', response)

def acCurrencySearch(request):
    rows = Database.combineRows(request.POST, mainConnector, FormClasses.AccountsTable.acCurrency,
                                FormClasses.AccountsTable.acTable, FormClasses.AccountsTable.acColumns, 1)

    formSetBuilder = formset_factory(FormClasses.AccountsForm, extra=(len(rows) - 3) / 3)
    filledFormSet = formSetBuilder(rows)

    response = {}
    response['Formset'] = filledFormSet
    return render(request, 'SimpleTable.html', response)
    #return HttpResponse(" ".join(rows))

def brdPriceFilter(request):
    rows = Database.combineRows(request.POST, mainConnector, FormClasses.BRDTable.brdPrice, FormClasses.BRDTable.brdTable, FormClasses.BRDTable.brdColumns, 2)

    formSetBuilder = formset_factory(FormClasses.BRDForm, extra=(len(rows) - 3) / 3)
    filledFormSet = formSetBuilder(rows)

    response = {}
    response['Formset'] = filledFormSet
    return render(request, 'SimpleTable.html', response)

def brdOrgSearch(request):
    rows = Database.combineRows(request.POST, mainConnector, FormClasses.BRDTable.brdOrgname, FormClasses.BRDTable.brdTable, FormClasses.BRDTable.brdColumns, 1)

    formSetBuilder = formset_factory(FormClasses.BRDForm, extra=(len(rows) - 3) / 3)
    filledFormSet = formSetBuilder(rows)

    response = {}
    response['Formset'] = filledFormSet
    return render(request, 'SimpleTable.html', response)

def caCodeSearch(request):
    rows = Database.combineRows(request.POST, mainConnector, FormClasses.CounteragentsTable.caCode, FormClasses.CounteragentsTable.caTable, FormClasses.CounteragentsTable.caColumns, 1)

    formSetBuilder = formset_factory(FormClasses.CounteragentsForm, extra=(len(rows) - 3) / 3)
    filledFormSet = formSetBuilder(rows)

    response = {}
    response['Formset'] = filledFormSet
    return render(request, 'SimpleTable.html', response)

def caSchemeSearch(request):
    rows = Database.combineRows(request.POST, mainConnector, FormClasses.CounteragentsTable.caCode, FormClasses.CounteragentsTable.caTable, FormClasses.CounteragentsTable.caColumns, 1)

    formSetBuilder = formset_factory(FormClasses.CounteragentsForm, extra=(len(rows) - 3) / 3)
    filledFormSet = formSetBuilder(rows)

    response = {}
    response['Formset'] = filledFormSet
    return render(request, 'SimpleTable.html', response)

def nomMUSearch(request):
    rows = Database.combineRows(request.POST, mainConnector, FormClasses.NomenclaturesTable.nomMU, FormClasses.NomenclaturesTable.nomTable,
    FormClasses.NomenclaturesTable.nomColumns, 1)

    formSetBuilder = formset_factory(FormClasses.NomenclaturesForm, extra=(len(rows) - 3) / 3)
    filledFormSet = formSetBuilder(rows)

    response = {}
    response['Formset'] = filledFormSet
    return render(request, 'SimpleTable.html', response)

def nomFTWordSearch(request):
    rows = Database.commitTextSearch(requestPost=request.POST, connector=mainConnector, field="nomFTWordSearchResult",
            table=FormClasses.NomenclaturesTable.nomTable, Columns=FormClasses.NomenclaturesTable.nomColumns, matchArgument=" NOT ", valueProcessArgumentStart="\'+ \"")

    formSetBuilder = formset_factory(FormClasses.NomenclaturesForm, extra=(len(rows) - 3) / 3)
    filledFormSet = formSetBuilder(rows)

    response = {}
    response['Formset'] = filledFormSet
    return render(request, 'SimpleTable.html', response)
    #return HttpResponse(Query.__str__())

def nomFTPhraseSearch(request):
    rows = Database.commitTextSearch(requestPost=request.POST, connector=mainConnector, field="nomFTPhraseSearchResult",
            table=FormClasses.NomenclaturesTable.nomTable, Columns=FormClasses.NomenclaturesTable.nomColumns, matchArgument=" ", valueProcessArgumentStart="\'\"")

    formSetBuilder = formset_factory(FormClasses.NomenclaturesForm, extra=(len(rows) - 3) / 3)
    filledFormSet = formSetBuilder(rows)

    response = {}
    response['Formset'] = filledFormSet
    return render(request, 'SimpleTable.html', response)

def comeBackToSTwithResult(request):
    return redirect('http://127.0.0.1:8000/MainFormTable/SearchMainTable/')

def collectDataForEditting(request, Key):
    global previousArgs
    if "form-" + Key + "-opCA_name" in request.POST:
        opCA_name = request.POST["form-" + Key + "-opCA_name"]
    if "form-" + Key + "-opNom_name" in request.POST:
        opNom_name = request.POST["form-" + Key + "-opNom_name"]
    if "form-" + Key + "-opBRD_id" in request.POST:
        opBRD_id = request.POST["form-" + Key + "-opBRD_id"]
    if "form-" + Key + "-opAC_id" in request.POST:
        opAC_id = request.POST["form-" + Key + "-opAC_id"]
    previousArgs = [ opCA_name ,opNom_name, opBRD_id, opAC_id]
    SearchMainTable = FormClasses.getFormTableTemplates({'opCA_name': opCA_name, 'opNom_name': opNom_name, 'opBRD_id': opBRD_id, 'opAC_id': opAC_id})
    return render(request, 'CommitEditting.html', {'form': SearchMainTable})
def collectDataForAdding(request):
    SearchMainTable = FormClasses.getFormTableTemplates({'opCA_name': '', 'opNom_name': '', 'opBRD_id': '', 'opAC_id': ''})
    return render(request, 'CommitAdding.html', {'form': SearchMainTable})
def collectDataForDeleting(request, Key):
    global data
    global mainConnector
    updateDataBuffer = ["", "", "", ""]
    if "form-" + Key + "-opCA_name" in request.POST:
        opCA_name = request.POST["form-" + Key + "-opCA_name"]
    if "form-" + Key + "-opNom_name" in request.POST:
        opNom_name = request.POST["form-" + Key + "-opNom_name"]
    if "form-" + Key + "-opBRD_id" in request.POST:
        opBRD_id = request.POST["form-" + Key + "-opBRD_id"]
    if "form-" + Key + "-opAC_id" in request.POST:
        opAC_id = request.POST["form-" + Key + "-opAC_id"]

    updateDataBuffer = [opCA_name ,  opNom_name ,  opBRD_id ,  opAC_id ]
    mainConnector.Delete(updateDataBuffer)
    resetData()
    return redirect('http://127.0.0.1:8000/MainFormTable/')

def commitEditting(request):
    global data
    global previousArgs
    global mainConnector
    updateDataBuffer = ["", "", "", ""]
    for field in request.POST:
        if re.match("opCA_name",field):
            updateDataBuffer[0] = request.POST[field]
        if re.match("opNom_name", field):
            updateDataBuffer[1] =  request.POST[field]
        if re.match("opBRD_id", field):
            updateDataBuffer[2] =  request.POST[field]
        if re.match("opAC_id", field):
            updateDataBuffer[3] =  request.POST[field]

    q = mainConnector.Update(previousArgs, updateDataBuffer)
    resetData()
    previousArgs = []
    return redirect('http://127.0.0.1:8000/MainFormTable/')
    #return HttpResponse(q.__str__())
def commitAdding(request):
    global data
    global mainConnector
    updateDataBuffer = ["", "", "", ""]
    for field in request.POST:
        if re.match("opCA_name",field):
            updateDataBuffer[0] = request.POST[field]
        if re.match("opNom_name", field):
            updateDataBuffer[1] = request.POST[field]
        if re.match("opBRD_id", field):
            updateDataBuffer[2] = request.POST[field]
        if re.match("opAC_id", field):
            updateDataBuffer[3] = request.POST[field]


    mainConnector.Add(updateDataBuffer)
    resetData()
    return redirect('http://127.0.0.1:8000/MainFormTable/')

def detectButton(request):
    for s in request.POST:
        if s.startswith("edit"):
            return collectDataForEditting(request, s[4:])
        if s.startswith("delete"):
            return collectDataForDeleting(request, s[6:])
        if s.startswith("add"):
            return collectDataForAdding(request)
        if s.startswith("search"):
            return redirect('http://127.0.0.1:8000/MainFormTable/SearchMainTable/')

def redirectToMT(request):
    return redirect('http://127.0.0.1:8000/MainFormTable/')