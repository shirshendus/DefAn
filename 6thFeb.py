from pyspark import SparkConf
from pyspark.context import SparkContext as sc
import numpy as np
import pandas as sc
import matplotlib.pyplot as mp
from matplotlib.patches import Rectangle
#matplotlib.use('TkAgg')
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 12,9
import warnings
warnings.filterwarnings("ignore")

import sys
import webbrowser
import os
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

# --------------Declaring required  Variables / dataframes -------------------
fileLocation='Defect Dump21feb.csv'
FTPFileLocation='FTP_FP.csv'
VidurFilelocation = 'VIDUR_PID.csv'
release= 2018.02
yGraph=[]
y2Graph=[]
y3Graph=[]
y4Graph=[]
commentsETE=[]
commentsCounts=[]
ISTCount=[]
ETECount=[]
PVTCount=[]
FTPTotal=[]
EDF_Apps = ['GCP' , 'EDF' , 'SXP', 'CSI - (FED) - GCP']
Apps= ['BGW', 'CADM','EUAM', 'UB', 'EDF Family' , 'ADOPT',
       'IGLOO', 'Pricer-D','SSDF', 'ROME', 'GIOM',  'USRP', 
       'NC3','AOTS-CM' , 'AOTS-M', 'AOTS-TM']
num=len(Apps)
x= np.linspace(0,num*5,num=num)
y= [0,10,20,30,40,50,60,70,80,90,100]
yTicks=[]
for i in [0,1,2,3,4,5,6,7,8,9,10]:
    yTicks.append(repr(10*i)+'%')
ISTTarget=75
ETETarget = 25.0
PVTtarget = 5
DDTarget= 3.4

# -------------- Loading DataFrames ..... -----------------
dataFrame=sc.read_csv(fileLocation, usecols=['RELEASE','TEST_PHASE', 'PROJECT', 'DEFECT_ID',
                                             'STATUS', 'ASSIGNED_TO_APP','ASSIGN_TO_UUID', 'ROOT_CAUSE_APP',
                                             'ROOT_CAUSE_CATEGORY', 'DATE_CREATED_SERVER', 'IBM_APP', 'HOURS_TO_FIX',
                                             'TURNAROUND_HOURS', 'ROOT_CAUSE', 'SCENARIO_TYPE', 'SEVERITY', 'DEFECT_AGE',
                                             'PHASE_FOUND_IN', 'ROOT_CAUSE_APP'])
dataframeFTP=sc.read_csv(FTPFileLocation, usecols=['App', 'FTP'])
dataFrameVidurPID=sc.read_csv(VidurFilelocation, usecols=['Project'])
#graphDataFrame=sc.DataFrame(columns=columns1)
#    dataFrame= dataFrame[np.isfinite(dataFrame[''])]
#    print (dataFrame)
#    data = dataFrame[(dataFrame['DEFECT_AGE'] >= 100) & (dataFrame['SEVERITY'] == 'Severity 1') & (dataFrame['PHASE_FOUND_IN'] =='End to End Testing (ETE)') & (dataFrame['ASSIGNED_TO_APP'] == 'PRICER-D') | (dataFrame['ASSIGNED_TO_APP'] == 'GCP')]
print (dataFrame.count())
#    countETE= dataFrame[(dataFrame['PHASE_FOUND_IN'] =='End to End Testing (ETE)') & ((dataFrame['ASSIGNED_TO_APP']=='PRICER-D') | (dataFrame['ASSIGNED_TO_APP']== 'GCP') | (dataFrame['ASSIGNED_TO_APP']== 'EDF') | (dataFrame['ASSIGNED_TO_APP']=='EFMS') | (dataFrame['ASSIGNED_TO_APP']=='ASOC') | (dataFrame['ASSIGNED_TO_APP']== 'NC3') | (dataFrame['ASSIGNED_TO_APP']== 'ROME')| (dataFrame['ASSIGNED_TO_APP']== 'CTP') | (dataFrame['ASSIGNED_TO_APP']== 'AOTS-M') | (dataFrame['ASSIGNED_TO_APP']== 'AOTS-CM')| (dataFrame['ASSIGNED_TO_APP']== 'IGLOO')| (dataFrame['ASSIGNED_TO_APP']== 'USRP')| (dataFrame['ASSIGNED_TO_APP']== 'SXP'))]
#    countIST = dataFrame[(dataFrame['PHASE_FOUND_IN'] =='Integrated Systems Testing')& ((dataFrame['ASSIGNED_TO_APP']=='PRICER-D') | (dataFrame['ASSIGNED_TO_APP']== 'GCP') | (dataFrame['ASSIGNED_TO_APP']== 'EDF') | (dataFrame['ASSIGNED_TO_APP']=='EFMS') | (dataFrame['ASSIGNED_TO_APP']=='ASOC') | (dataFrame['ASSIGNED_TO_APP']== 'NC3') | (dataFrame['ASSIGNED_TO_APP']== 'ROME')| (dataFrame['ASSIGNED_TO_APP']== 'CTP') | (dataFrame['ASSIGNED_TO_APP']== 'AOTS-M') | (dataFrame['ASSIGNED_TO_APP']== 'AOTS-CM')| (dataFrame['ASSIGNED_TO_APP']== 'IGLOO')| (dataFrame['ASSIGNED_TO_APP']== 'USRP')| (dataFrame['ASSIGNED_TO_APP']== 'SXP'))]
#    countPVT= dataFrame[(dataFrame['PHASE_FOUND_IN'] =='PVT') & ((dataFrame['ASSIGNED_TO_APP']=='PRICER-D') | (dataFrame['ASSIGNED_TO_APP']== 'GCP') | (dataFrame['ASSIGNED_TO_APP']== 'EDF') | (dataFrame['ASSIGNED_TO_APP']=='EFMS') | (dataFrame['ASSIGNED_TO_APP']=='ASOC') | (dataFrame['ASSIGNED_TO_APP']== 'NC3') | (dataFrame['ASSIGNED_TO_APP']== 'ROME')| (dataFrame['ASSIGNED_TO_APP']== 'CTP') | (dataFrame['ASSIGNED_TO_APP']== 'AOTS-M') | (dataFrame['ASSIGNED_TO_APP']== 'AOTS-CM')| (dataFrame['ASSIGNED_TO_APP']== 'IGLOO')| (dataFrame['ASSIGNED_TO_APP']== 'USRP')| (dataFrame['ASSIGNED_TO_APP']== 'SXP'))]
#    Apps = dataFrame.groupby('ASSIGNED_TO_APP')['ASSIGNED_TO_APP'].last()

#Apps = ['Pricer-D' ,  'GCP' ,  'EDF' , 'EFMS' , 'ASOC' ,  'NC3' ,  'ROME',  'CTP' ,  'AOTS-M' ,  'AOTS-CM',  'IGLOO',  'USRP',  'SXP']......Not added due to less FTPs 'ASOC' ,'EFMS' ,'GPS', 'Data Warehouse','CTP' ,   
#EDF_Apps = ['GCP' , 'EDF' , 'SXP', 'SCOPE', 'NCD', 'CSI - (FED) - GCP', 'GCP-EBDP','GCP-EDN', 'GCP-EIN', 'GCP-EBDP']

# ----------------- Processing Data, Calculation of Metrics ------------------------->

'''       Counting the defects 
#       Considering Projects which are as per Vidur release (Defects created for these projects in earlier releases in TDP will also be included)
            Test Phases in 'End to End Testing (ETE)', 'User Acceptance Test (UAT)
            Status in 'Deferred' or 'Closed'
            Excluding duplicates
            
        '''
for app in Apps:
    if app == 'EDF Family': #for EDF Family of Apps
        countETE= dataFrame[(dataFrame['RELEASE']=='2018.02') & (dataFrame['STATUS']=='Closed'
                            ) & (dataFrame['PHASE_FOUND_IN'].isin(['Iteration Test', 'Performance/Load']
                            ) | dataFrame['TEST_PHASE'].isin(['ETE', 'IST', 'REG','UAT'])
                            ) & (dataFrame['ROOT_CAUSE_APP'].isin(EDF_Apps)) & (dataFrame['STATUS'].isin(['Closed'])
                            ) & (dataFrame['PROJECT'].isin(dataFrameVidurPID['Project'])
                            ) & (dataFrame['ROOT_CAUSE_CATEGORY'].isin(['Coding','Design Specification', 'Environment', 'Data']) 
                            | (dataFrame['ROOT_CAUSE_CATEGORY'].isin(['Deployment'])
                            &(dataFrame['ROOT_CAUSE'].isin(['Software Versioning','Packaging']))))]
        countPVT= dataFrame[(dataFrame['RELEASE']=='2018.02')
                            & (dataFrame['STATUS']=='Closed') 
                            & (dataFrame['TEST_PHASE'] =='PVT') 
                            & (dataFrame['ROOT_CAUSE_APP'].isin(EDF_Apps)) 
                            & (dataFrame['STATUS'].isin(['Deferred','Closed'])) 
                            & (dataFrame['PROJECT'].isin(dataFrameVidurPID['Project']))
                            & (dataFrame['ROOT_CAUSE_CATEGORY'].isin(['Coding','Design Specification', 'Environment', 'Data']) 
                            | (dataFrame['ROOT_CAUSE_CATEGORY'].isin(['Deployment'])
                            &(dataFrame['ROOT_CAUSE'].isin(['Software Versioning','Packaging']))))]
        countIST2=dataFrame[(dataFrame['RELEASE']=='2018.02')
                            & (dataFrame['ROOT_CAUSE_APP'].isin(EDF_Apps))
                            & (dataFrame['PHASE_FOUND_IN'].isin(['Iteration Test', 'Performance/Load']) 
                            | dataFrame['TEST_PHASE'].isin(['ETE', 'IST', 'REG','UAT'])) 
                            & (dataFrame['STATUS'].isin(['Deferred','Closed']))
                            & ~(dataFrame['ROOT_CAUSE'].isin(['Not a defect','Duplicate'])) 
                            & (dataFrame['PROJECT'].isin(dataFrameVidurPID['Project']))]
#        Summing up FTPs for application from input csv
        appFTP=dataframeFTP[dataframeFTP['App'].str.lower()=='EDF Family of Applications'.lower()]
    else: #for other Apps        
        countETE= dataFrame[(dataFrame['RELEASE']=='2018.02') & (dataFrame['STATUS']=='Closed') & (dataFrame['PHASE_FOUND_IN'].isin(['Iteration Test', 'Performance/Load']) | dataFrame['TEST_PHASE'].isin(['ETE', 'IST', 'REG','UAT'])) & (dataFrame['ROOT_CAUSE_APP'] == app) & (dataFrame['STATUS'].isin(['Closed'])) & (dataFrame['PROJECT'].isin(dataFrameVidurPID['Project'])) & (dataFrame['ROOT_CAUSE_CATEGORY'].isin(['Coding','Design Specification', 'Environment', 'Data']) | (dataFrame['ROOT_CAUSE_CATEGORY'].isin(['Deployment'])&(dataFrame['ROOT_CAUSE'].isin(['Software Versioning','Packaging']))))]
#        countETE= dataFrame[(dataFrame['PHASE_FOUND_IN'].isin(['End to End Testing (ETE)', 'User Acceptance Test (UAT)'])) & (dataFrame['ROOT_CAUSE_APP'] == app) & (dataFrame['STATUS'].isin(['Deferred','Closed']))& (dataFrame['PROJECT'].isin(dataFrameVidurPID['Project'])) & (dataFrame['ROOT_CAUSE']!= 'Duplicate')]
    #    countIST = dataFrame[(dataFrame['PHASE_FOUND_IN'] =='Integrated Systems Testing') & (dataFrame['ASSIGNED_TO_APP'] == app) & (dataFrame['STATUS'] != 'Cancelled')]
        countPVT= dataFrame[(dataFrame['RELEASE']=='2018.02') 
                            & (dataFrame['PHASE_FOUND_IN'] =='PVT') 
                            & (dataFrame['ROOT_CAUSE_APP']== app) 
                            & (dataFrame['STATUS'].isin(['Deferred','Closed']))
                            & (dataFrame['PROJECT'].isin(dataFrameVidurPID['Project']))]
        countIST2=dataFrame[(dataFrame['RELEASE']=='2018.02')
                            & (dataFrame['ROOT_CAUSE_APP']== app)
                            &(dataFrame['PHASE_FOUND_IN'].isin(['Regression Testing', 'Integrated Systems Testing'])) 
                            & (dataFrame['STATUS'].isin(['Deferred','Closed'])) 
                            & ~(dataFrame['ROOT_CAUSE'].isin(['Not a defect','Duplicate']))
                            & (dataFrame['PROJECT'].isin(dataFrameVidurPID['Project']))]
        appFTP=dataframeFTP[dataframeFTP['App'].str.lower() == app.lower()]
    sumFTP=appFTP['FTP'].sum()
    TotalIST = countIST2['DEFECT_ID'].count()
    TotalETE = countETE['DEFECT_ID'].count()
    TotalPVT = countPVT['DEFECT_ID'].count()
    defectDensity= ((TotalIST+TotalETE)/(sumFTP*158/1000))
    print("Application Name ======> "+ app)
    commentsCounts.append("\nTotal ETE Defects :" +repr(countETE['DEFECT_ID'].count())+"\nTotal IST Defects :"+repr(countIST2['DEFECT_ID'].count())+"\nTotal PVT Defects :" + repr(countPVT['DEFECT_ID'].count()))
#    Calculation and store in arrays
    ETE_CONT = 100*TotalETE/(TotalETE+TotalIST)
    PVT_CONT = 100*TotalPVT/(TotalPVT+TotalETE+TotalIST)
    IST_CONT = 100*TotalIST/(TotalETE+TotalIST)
    yGraph.append(round(ETE_CONT,2))
    y2Graph.append(round(PVT_CONT,2))
    y3Graph.append(round(defectDensity,2))
    y4Graph.append(round(IST_CONT,2))
    FTPTotal.append(sumFTP)
    ISTCount.append(TotalIST)
    ETECount.append(TotalETE)
    PVTCount.append(TotalPVT)
    
#    graphDataFrame=sc.DataFrame([{app, ETE_CONT, PVT_CONT}], columns=columns1)
    print('ETE Containment of '+ repr(app)+' is ' + repr(ETE_CONT))
    print('PVT containment of '+ repr(app)+' is ' + repr(PVT_CONT))
    print('IST Containment :'+repr(IST_CONT))
    reqIST = 0
    if ETE_CONT >= ETETarget:
# calculating Recommnded new Defects  
        reqIST = TotalETE/(ETETarget/(100-ETETarget))
        commentsETE.append("Recommendation if it's suitable for your application & Tower guidelines \n \nETE Phase Containment Metrics is above Target of " + repr(ETETarget) + "% !\n        "+repr(int(reqIST-countIST2['DEFECT_ID'].count())) +" defects at IST phase were needed \n        to keep ETE Phase Cont at or below " + repr(ETETarget) + "%")
    else:
        commentsETE.append(" ")#empty - no recommendation for good condition
    print('Required total Defect',(reqIST))

class DraggableRectangle:
    def __init__(self, rect):
        self.rect = rect
        self.press = None

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.rect.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.rect.axes: return

        contains, attrd = self.rect.contains(event)
        if not contains: return
#        print(event.xdata)
        i=int((event.xdata+1)//5.1)
        print(i)
        fig=plt.figure(1)
        ax=fig.add_subplot(111)
        ax.set_title(Apps[i]+' Containment Metrics Details')
        ax.set_ylim([0,100])
        ax.set_ylabel('Phase Conatinment Metrics')
        ax.set_xticks([1,2,3,4])
        ax.set_xticklabels(['IST Contnmnt', 'ETE Contnmnt', 'PVT Contnmnt', 'Defect Density'])
        ax.set_yticks(y)
        ax.set_yticklabels(yTicks)
        
        
        print(y4Graph[i], yGraph[i], y2Graph[i])
        ax.bar(x=[1,2,3], height=[y4Graph[i], yGraph[i], y2Graph[i]], color=['y','b','g'], alpha=0.6)
        ax.axhline(y=PVTtarget, xmax=3, linewidth = 2, color='g', alpha = 0.6)
        ax.text(-0.03, PVTtarget+2,'Target of\n PVT PC <'+repr(PVTtarget)+'%', color='k')
        ax.axhline(y=ETETarget, xmax=3, linewidth = 2, color='b', alpha = 0.6)
        ax.text(-0.03, ETETarget+2,'Target of\n ETE PC < '+repr(ETETarget)+'%', color='k')
        ax.axhline(y=ISTTarget, xmax=3, linewidth = 2, color='y', alpha = 0.6)
        ax.text(-0.03, ISTTarget+2,'Target of\n IST PC > '+repr(ISTTarget)+'%', color='k')
        
        ax1=ax.twinx()
        ax1.set_ylim([0,5])
        ax1.set_ylabel('Defect Density')
        ax1.axhline(y=DDTarget, xmax=52, linewidth = 2, color='k', alpha = 0.5)
        ax1.text(3.6, DDTarget,'Target DD\n <'+repr(DDTarget), color='k')
        ax1.text(3.1, y3Graph[i], '<-- Defect Density')
        ax1.plot(3, y3Graph[i],'o', color='k', alpha =0.6)
        plt.show()
        
#        ax2=fig.add_subplot(122)
#        ax2.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
#        details=Apps[i]+"\n\n\n"+commentsCounts[i]+"\n\n\nIST Containment : "+repr("%.2f" %round(y4Graph[i]))+"%\n\nETE Phase Containment: "+repr("%.2f" %round(yGraph[i]))+"%\n\nPVT Phase Containment: "+repr("%.2f" %round(y2Graph[i], 2))+"%\n\nDefect Density: "+repr("%.2f" %round(y3Graph[i],2))+"\n\n"+commentsETE[i]
#        ax2.text(0.05, 0.3, details)
#        plt.show()
        fig.savefig("figure.png")
        plt.close(fig) 
# calculating Recommnded new Defects
        if yGraph[i] >= ETETarget:
            reqIST = ETECount[i]/(ETETarget/(100-ETETarget))
            print('req', reqIST)
        else:
            reqIST = 0#empty - no recommendation for good condition
        defaultDefectnum=ISTCount[i]+reqIST
        print('Required total Defect',defaultDefectnum)
        #---- HTML/AngularJs for interactive defect management----
        html="""
        <!DOCTYPE html>
        <html>
        <head>
        <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.6.4/angular.min.js"></script>
        <style>
        table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
        }
        th, td {
            padding: 5px;
            text-align: left;
        }
        table#t01 {
            width: 100%;    
            background-color: #f1f1c1;
        }
        </style>
        </head>
        <body>
        <h1>AppName</h1>
        <table id="t01">
          <tr>
            <th>Current Metrics</th>
            <th>Target</th>
            <th>Actual Number</th>
            <th>Actual Phase Containment</th>
            <th>Difference with Target</th>
          </tr>
          <tr>
            <th>IST Defects</th>
            <td>ISTTarget</td>
            <td>ISTActualNum</td>
            <td>ISTActualPercent</td>
            <td>ISTDiff</td>
          </tr>
          <tr>
            <th>ETE Defects</th>
            <td>ETETarget</td>
            <td>ETEActualNum</td>
            <td>ETEActualPercent</td>
            <td>ETEDiff</td>
          </tr>
          <tr>
            <th>PVT Defects</th>
            <td>PVTTarget</td>
            <td>PVTActualNum</td>
            <td>PVTActualPercent</td>
            <td>PVTDiff</td>
          </tr>
          <tr>
            <th>Defect Density</th>
            <td>DDTarget</td>
            <td>DDActual</td>
            <td></td>
            <td>DefectDiff</td>
          </tr>
        </table>
        <br>
        Total FTP for AppName FTPActualTotal
        <br>
        <div align='right'>Defect Management : (Please stick to Tower and Application guidelines)</div>
        <br>
        <br>
        <img src="figure.png" alt="AppName NGA Metrics" style="float:left;width:60%;height:60%;">
        <div ng-app="myApp" ng-controller="myCtrl">
        No. of IST Defects:     <input type="number" ng-model="ist"><br>
        No. of ETE defects:     <input type="number" ng-model="ete"><br>
        Total FTP under AppName:     <input type="number" ng-model="ftp"><br>
        <h3>IST Containment:   {{(100*ist/(ist--ete)) | number : 2}}%<br>
        ETE Containment:   {{(100*ete/(ist--ete)) | number : 2}}%<br>
        PVT Containment:   {{(100*PVTActualNum/(ist--ete--PVTActualNum)) | number : 2}}%<br>
        <br>Defect Density:{{((ist--ete)/(ftp*158/1000)) | number : 2}}<br>
        <br>{{((ist--ete)/(ftp*158/1000)) >= 3.4 ? (((ist -- ete) - (3.4*(ftp*158/1000)))|number:0)+" defects impacting Defect Density to cross limit." : "  "}}</h3>
        </div>
            
        <script>
         
        var app = angular.module('myApp', []);
        app.controller('myCtrl', function($scope) {
            $scope.ist = ISTActualNum;
            $scope.ete = ETEActualNum;
            $scope.ftp = FTPActualTotal;
        });
        </script>
        </body>
        </html>
        """
        html=html.replace("AppName", Apps[i]).replace("ISTTarget", ">"+repr(ISTTarget)+"%").replace("ISTActualNum", repr(ISTCount[i])).replace("ISTActualPercent", repr(y4Graph[i])[:5]+'%').replace("ISTDiff",repr((y4Graph[i]-ISTTarget))[:4])
        html=html.replace("ETETarget", "<"+repr(ETETarget)+"%").replace("ETEActualNum", repr(ETECount[i])).replace("ETEActualPercent", repr(yGraph[i])[:5]+'%').replace("ETEDiff",repr(ETETarget-yGraph[i])[:4])
        html=html.replace("PVTTarget", "<"+repr(PVTtarget)+"%").replace("PVTActualNum", repr(PVTCount[i])).replace("PVTActualPercent", repr(y2Graph[i])[:4]+'%').replace("PVTDiff",repr(PVTtarget-y2Graph[i])[:4])
        html=html.replace("DDTarget", "<"+repr(DDTarget)).replace("DDActual",repr(y3Graph[i])[:4]).replace("FTPActualTotal",repr(FTPTotal[i])).replace("defaultDefectnum",repr(defaultDefectnum)).replace('DefectDiff', repr(DDTarget-y3Graph[i])[:4] )
#        DDCrossPlaceHolder="<br>{{((ist -- ete) - (3.4*(ftp*158/1000))) | number : 0}} defects impacting Defect Density to crosss limit."
#        if y3Graph[i]>=3.4:
#            html=html.replace("DDCrossPlaceHolder",DDCrossPlaceHolder)
#        else:
#            html=html.replace("DDCrossPlaceHolder","")
#        print(html)
        f = open('UserNGA.html','w')
        f.write(html)
        f.close()
        webbrowser.open("UserNGA.html")
        
#---------------------Plotting the primary graph including all apps---------------------------->        
fig = plt.figure(0)
ax = fig.add_subplot(111)
ax.set_title("Click on App Bar for More Details")
bars3 = ax.bar(x=x-1, height=y4Graph, align='edge', width=1, label='IST Phase Containment', color='y', alpha=0.8)
bars1 = ax.bar(x=x, align='edge', width=1, height=yGraph, label ='ETE Phase Containment', color='b', alpha=0.8)
bars2 = ax.bar(x=x+1, height=y2Graph, align='edge', width=1, label='PVT Phase Containment', color='g', alpha=0.8)
ax2 = ax.twinx()     # Creating Secondary Axis
points = ax2.plot(x+1.5, y3Graph, 'o', color='k')
print("App", Apps, "ETE", yGraph, "PVT", y2Graph, "DD", y3Graph, "IST", y4Graph)

ax.legend(bbox_to_anchor=(0.77, 1.15))
ax.axhline(y=ISTTarget, xmax=3, linewidth = 2, color='y', alpha = 0.6)
ax.text(-15, ISTTarget+2,'Target of\n IST PC > '+repr(ISTTarget)+'%', color='k')
ax.axhline(y=ETETarget, xmax=52, linewidth = 2, color='b', alpha = 0.6)
ax.text(-15, ETETarget-2,' Target ETE\n PC < '+repr(ETETarget)+'%', color='k')
ax.axhline(y=PVTtarget, xmax=52, linewidth = 2, color='g', alpha = 0.6)
ax.text(-15, PVTtarget-2,' Target PVT\n PC < '+repr(PVTtarget)+'%', color='k')
ax2.axhline(y=DDTarget-0.1, xmax=52, linewidth = 2, color='k', alpha = 0.6, label='Defect Density')
ax2.text(num*5+7, DDTarget-0.1,' Target DD \n <'+repr(DDTarget)+' K Hrs', color='k')
ax2.set_ylabel("Defect Density")
ax2.legend(bbox_to_anchor=(1.1, 1.1))

ax2.set_ylim([0,5])
ax.set_ylabel("Defect Metrics")
#ax.set_xlabel("Applications", color='b')
ax.set_xticks(x)
ax.set_xticklabels(Apps, rotation=90)
ax.set_yticks(y)
ax.set_yticklabels(yTicks)
#ax.text()
drs = []
brs=[]
for bar1 in bars1:
    dr = DraggableRectangle(bar1)
    dr.connect()
    drs.append(dr)
for bar2 in bars2:
    dr = DraggableRectangle(bar2)
    dr.connect()
    drs.append(dr)
for bar3 in bars3:
    dr = DraggableRectangle(bar3)
    dr.connect()
    drs.append(dr)
for point in points:
    dr = DraggableRectangle(point)
    dr.connect()
    drs.append(dr)
    
plt.show()