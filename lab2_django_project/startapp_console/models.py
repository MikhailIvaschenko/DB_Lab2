from django.db import models

import Scripts.lab2_django_project.startapp_console.database as Database
from django import forms
# Create your models here.

mainConnector = Database.Connector()

class MainFormTable(forms.Form):
    opCA_name = forms.CharField(required=True, label='Counteragent', label_suffix='',
                              widget=forms.TextInput(attrs={'readonly': True}))
    opNom_name = forms.CharField(required=True, label='Nomenclature', label_suffix='',
                             widget=forms.TextInput(attrs={'readonly': True}))
    opBRD_id = forms.CharField(required=True, label='BRD number', label_suffix='',
                             widget=forms.TextInput(attrs={'readonly': True}))
    opAC_id = forms.CharField( required=True, label='Account', label_suffix='',
                           widget=forms.TextInput(attrs={'readonly': True}))

class ACTDateSearch(forms.Form):
    acDateLeft = forms.fields.DateField(required=True, label='Start date')
    acDateRight = forms.fields.DateField(required=True, label='Finish date')

class ACTCurrencySearch(forms.Form):
    acCurrency = forms.ChoiceField(choices=mainConnector.getDataFromList("acCurrency", "accounts"), required=True, label='Currency')

class BRDTPriceFilter(forms.Form):
    brdPriceLeft = forms.fields.FloatField(required=True, label='Bottom price border', min_value=0, max_value=10000)
    brdPriceRight = forms.fields.FloatField(required=True, label='Top price border', min_value=0, max_value=10000)

class BRDTOrgSearch(forms.Form):
    brdOrganization_name = forms.ChoiceField(choices=mainConnector.getDataFromList("brdOrganization_name", "brd"), required=True, label='Organization')

class CATCodeSearch(forms.Form):
    caUKTZED_code = forms.CharField(required=True, label='Counteragent\'s UKTZED_code')

class CATSchemeSearch(forms.Form):
    caScheme = forms.ChoiceField(choices=mainConnector.getDataFromList("caScheme", "counteragents"), required=True, label='Scheme')

class NOMTMUSearch(forms.Form):
    nomMU = forms.ChoiceField(choices=mainConnector.getDataFromList("nomMU", "nomenclatures"), required=True, label='Measure units')

class NOMTFTPhraseSearch(forms.Form):
    nomFTPhraseSearchResult = forms.CharField(required=True, label='Contains the following phrase', max_length=40)

class NOMTFTWordSearch(forms.Form):
    nomFTWordSearchResult = forms.CharField(required=True, label='Doesn\'t containt the following word', max_length=14)



class AccountsForm(forms.Form):
    acID = forms.CharField(required=True, label='acID ',
                              widget=forms.TextInput(attrs={'readonly': True}))
    acDate = forms.DateField(required=True, label='acDate ',
                           widget=forms.TextInput(attrs={'readonly': True}))
    acOperation_type = forms.CharField(required=True, label='acOperation_type ',
                              widget=forms.TextInput(attrs={'readonly': True}))
    acPrice = forms.FloatField(required=True, label='acPrice ',
                              widget=forms.TextInput(attrs={'readonly': True}))
    acCurrency = forms.CharField(required=True, label='acCurrency ',
                              widget=forms.TextInput(attrs={'readonly': True}))
    acGoods_type = forms.CharField(required=True, label='acGoods_type ',
                              widget=forms.TextInput(attrs={'readonly': True}))

class BRDForm(forms.Form):
    brdID = forms.CharField(required=True, label='brdID ',
                           widget=forms.TextInput(attrs={'readonly': True}))
    brdPrice = forms.FloatField(required=True, label='brdPrice ',
                               widget=forms.TextInput(attrs={'readonly': True}))
    brdCurrency = forms.CharField(required=True, label='brdCurrency ',
                               widget=forms.TextInput(attrs={'readonly': True}))
    brdOperation_types = forms.CharField(required=True, label='brdOperation_types ',
                                       widget=forms.TextInput(attrs={'readonly': True}))
    brdOrganization_name = forms.CharField(required=True, label='brdOrganization_name ',
                                 widget=forms.TextInput(attrs={'readonly': True}))

class CounteragentsForm(forms.Form):
    caName = forms.CharField(required=True, label='caID ',
                            widget=forms.TextInput(attrs={'readonly': True}))
    caUKTZED_code = forms.CharField(required=True, label='caUKTZED_code ',
                            widget=forms.TextInput(attrs={'readonly': True}))
    caScheme = forms.CharField(required=True, label='caScheme ',
                            widget=forms.TextInput(attrs={'readonly': True}))
    caITC = forms.CharField(required=True, label='caITC ',
                            widget=forms.TextInput(attrs={'readonly': True}))

class NomenclaturesForm(forms.Form):
    nomName = forms.CharField(required=True, label='nomName ',
                              widget=forms.TextInput(attrs={'readonly': True}))
    nomVendore_code = forms.DateField(required=True, label='nomVendore_code ',
                           widget=forms.TextInput(attrs={'readonly': True}))
    nomVAT_rate = forms.CharField(required=True, label='nomVAT_rate ',
                              widget=forms.TextInput(attrs={'readonly': True}))
    nomUKTZED_code = forms.CharField(required=True, label='nomUKTZED_code ',
                                widget=forms.TextInput(attrs={'readonly': True}))
    nomStock_type = forms.CharField(required=True, label='nomStock_type ',
                              widget=forms.TextInput(attrs={'readonly': True}))
    description = forms.CharField(required=True, label='Description ',
                                  widget=forms.Textarea(attrs={'readonly': True, 'rows': 3, 'cols': 20}))





class getFormTableTemplates(forms.Form):
    opCA_name = forms.ChoiceField(choices=mainConnector.getList(mainConnector.caKeys), required=True, label='CA_name')
    opNom_name = forms.ChoiceField(choices=mainConnector.getList(mainConnector.nomKeys), required=True, label='Nom_name')
    opBRD_id = forms.ChoiceField(choices=mainConnector.getList(mainConnector.brdKeys), required=True, label='BRD_id')
    opAC_id = forms.ChoiceField(choices=mainConnector.getList(mainConnector.accountsKeys), required=True, label='Account_id')

class AccountsTable():
    acDate = "acDate"
    acCurrency = "acCurrency"
    acTable = "accounts"
    acColumns = ["acID", "acDate", "acOperation_type", "acPrice", "acCurrency", "acGoods_type"]

class BRDTable():
    brdPrice = "brdPrice"
    brdOrgname = "brdOrganization_name"
    brdTable = "brd"
    brdColumns = ["brdID", "brdPrice", "brdCurrency", "brdOperation_types", "brdOrganization_name"]

class CounteragentsTable():
    caCode = "caUKTZED_code"
    caScheme = "caScheme"
    caTable = "counteragents"
    caColumns = ["caName", "caUKTZED_code", "caScheme", "caITC"]

class NomenclaturesTable():
    nomMU = "nomMU"
    nomTable = "nomenclatures"
    nomColumns = ["nomName", "nomVendore_code", "nomMU", "nomVAT_rate", "nomUKTZED_code", "nomStock_type", "description"]
