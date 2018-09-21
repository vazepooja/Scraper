
# Keep required webdriver in the env PATH (or in cwd)
def get_flight_details(details):

    ###Creating variable for Capture Date
    now = datetime.datetime.now()
    CaptString_date=now.strftime("%m-%d-%Y")
    
    CaptTime=now.strftime('%H:%M:%S')
    Timeslot=now.strftime('%H')
    [org, dest, String_date,String_date_new,orgfull,destfull,countryo,countryd,fclist,fidlist,jlist,orlist,destlist,datelist,dtlist,atlist,plist,bflist,tflist,captdatelist,stoplist,captimelist,distlist,Distance,timeslot] = details
    url="https://flight.easemytrip.com/FlightList/Index?org="+org+"-"+orgfull+",%20"+countryo+"&dept="+dest+"-"+destfull+",%20"+countryd+"&adt=1&chd=0&inf=0&cabin=0&airline=undefined&deptDT="+String_date+"&arrDT=undefined&isOneway=true&isDomestic=false"

    driver.get("https://flight.easemytrip.com/FlightList/Index?org="+org+"-"+orgfull+",%20"+countryo+"&dept="+dest+"-"+destfull+",%20"+countryd+"&adt=1&chd=0&inf=0&cabin=0&airline=undefined&deptDT="+String_date+"&arrDT=undefined&isOneway=true&isDomestic=false")
    print(org+dest)
    try:
        WebDriverWait(driver, 70).until(EC.presence_of_element_located((By.XPATH,'//*[@id="ResultDiv"]/div/div/div[3]/div[1]/div[1]/div[1]/div[1]/div/div[2]/span[1]')))
    except:
        print("Took long to load!")
        pass
        
    ###print("https://flight.easemytrip.com/FlightList/Index?org="+org+"-"+orgfull+",%20"+countryo+"&dept="+dest+"-"+destfull+",%20"+countryd+"&adt=1&chd=0&inf=0&cabin=0&airline=undefined&deptDT="+String_date+"&arrDT=undefined&isOneway=true&isDomestic=false")
    
    try:
        driver.find_element_by_xpath('//*[@id="chkNonStop"]').click()
        ##Uncomment for applying G8 filter
        #driver.find_element_by_xpath('//*[@id="GoAir"]').click()
    except:
        pass
    
    b=0
    Flight_company=driver.find_elements_by_xpath('//*[@id="ResultDiv"]/div/div/div[3]/div/div/div/div/div/div[2]/span[1]')
    for fc in Flight_company:
        b=b+1
        fclist.append(fc.text)
    #print("Frame fetched :"+str(b))
    
    FlightID=driver.find_elements_by_xpath('//*[@id="ResultDiv"]/div/div/div[3]/div/div/div/div/div/div[2]/span[2]')
    for fid in FlightID:
        fidlist.append(fid.text)  
    

    Dept=driver.find_elements_by_xpath('//*[@id="ResultDiv"]/div/div/div[3]/div/div/div/div[2]/span[1]')
    for dep in Dept:
        dtlist.append(dep.text)    

    Arr=driver.find_elements_by_xpath('//*[@id="ResultDiv"]/div/div/div[3]/div/div/div/div[4]/span[1]')
    for arr in Arr:
        atlist.append(arr.text) 
            
    Total_fare=driver.find_elements_by_xpath('//*[@id="ResultDiv"]/div/div/div[3]/div/div/div/div[5]/div/div[2]')
    for td in Total_fare:
        td2=td.text
        td3=td2.replace(',','')
        plist.append(td3)
    
    Dur=driver.find_elements_by_xpath('//*[@id="ResultDiv"]/div/div/div[3]/div/div/div/div[3]/span[1]')
    for du in Dur:
        jlist.append(du.text)
    
    for o in range(0,b):
        orlist.append(org)
    
    for d in range(0,b):
        destlist.append(dest)
    
    
    for d1 in range(0,b):
        datelist.append(String_date_new)

    for cd in range(0,b):
        captdatelist.append(CaptString_date)
        
    
    for c in range(0,b):
        driver.find_element_by_xpath('//*[@id="'+str(c)+'"]').click()
        driver.find_element_by_xpath('//*[@id="divFlightDetailSec'+str(c)+'"]/ul/li[2]').click()
        bf=driver.find_element_by_xpath('//*[@id="fr'+str(c)+'"]/div[2]/div/div[2]/div/span[2]')
        bflist.append(bf.text)
        tf=driver.find_element_by_xpath('//*[@id="fr'+str(c)+'"]/div[2]/div/div[3]/div[2]/span[2]')
        tflist.append(tf.text)
        
    for cdd in range(0,b):
        captimelist.append(CaptTime)
    
    for ts in range(0,b):
        timeslot.append(Timeslot)
        
    
    Stp=driver.find_elements_by_xpath('//*[@id="ResultDiv"]/div/div/div[3]/div/div[1]/div[1]/div[3]/span[2]')
    for s in Stp:
        stoplist.append(s.text)
    
    for dt in range(0,b):
        distlist.append(Distance)
        
        
    
    return fclist,fidlist,jlist,orlist,destlist,datelist,dtlist,atlist,plist,bflist,tflist,captdatelist,stoplist,captimelist,distlist,timeslot
    
def exceptnDiff(data):
    exceptns=pd.DataFrame(columns=["Sector","Lowest_Fare_Airline","Comepetitor_Dept_Time","G8_Dept_Date","G8_Dept_Time","G8_Flight_No","G8_Fare","Day_Lowest","Day_Diff","TimeBand_Lowest","TimeBand_Diff",])    
    data['Sector']=data[['Origin','Destination']].sum(axis=1)
    data['Time_min']=[(float(str(t).split(':')[0])*float(60))+float(str(t).split(':')[1]) for t in data['Dept_Time']]
    for i in data.Sector.unique():
        #print(i)
        for j in data.Dept_Date.unique():
            #print(j)
            df=data.query('Sector==@i & Dept_Date==@j')
            df1=data.query('Sector==@i & Dept_Date==@j & Airline!="GoAir"')
            #print(df)
            df.Total_Price=df.Total_Price.astype(float)
            minimum=float(df['Total_Price'].min())
            fare=df.query('Airline=="GoAir"')
            fare.reset_index(drop=True, inplace=True)
            flights=pd.DataFrame(columns=df1.columns)
            #["Dept_Date","Airline","Flight_Code","Dept_Time",'Total_Price',"Sector",'Time_min']
            for t in fare['Time_min']:
                #print(t)
                t1=t-90
                t2=t+90
                ind=fare.index[fare['Time_min']==t]
                flights=df.query('Time_min>=@t1 & Time_min<=@t2')
                f=fare.loc[ind]
                f.reset_index(drop=True, inplace=True)
                if len(flights)==0:
                    continue
                flights.reset_index(drop=True, inplace=True)
                flights.Total_Price=flights.Total_Price.astype(float)
                mini=float(flights['Total_Price'].min())
                #air_ind=flights.index[flights['Total_Price']==float(mini)]
                Airline=flights.loc[flights['Total_Price']==mini]
                Airline.reset_index(drop=True, inplace=True)
                
                
                diff=fare.loc[ind]['Total_Price']-mini
                diff.reset_index(drop=True, inplace=True)
                diff1=fare.loc[ind]['Total_Price']-minimum
                diff1.reset_index(drop=True, inplace=True)
                exceptns=exceptns.append({'Sector': i,
                                          "Lowest_Fare_Airline":Airline['Airline'][0],
                                          "G8_Dept_Date":j,
                                          "G8_Dept_Time":f['Dept_Time'][0],
                                          "G8_Flight_No":f['Flight_Code'][0],
                                          "TimeBand_Lowest":mini,
                                          "Day_Lowest":minimum,
                                          "G8_Fare":float(fare['Total_Price'][ind]),
                                          "TimeBand_Diff":diff[0],
                                          "Day_Diff":diff1[0],
                                          "Comepetitor_Dept_Time":Airline['Dept_Time'][0]
                             }, ignore_index=True)
            
                    
            
    return exceptns



###Importing Packages
from selenium import webdriver
import numpy as np
import time
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import pandas as pd
import yaml 
conf=open(r"D:\Scrappers\Run_Daily\Scrapper_emt_Domestic_CONF.json").read()
config=yaml.load(conf)
print(config)

###Creating Chrome driver element
url=config.get("chrome_driver_path")
chrome_options = Options()
chrome_options.add_argument("--disable-javascript")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--incognito")
#chrome_options.add_argument("--headless")
driver = webdriver.Chrome(url,chrome_options=chrome_options) 
def main():
    ###Fetching start time
    start_time= time.time()
    
    ###Reading Paths and DeptDate from Config file 
    data = pd.read_csv(config.get("sectors_csv_path"), encoding = "ISO-8859-1")
    date_data=pd.read_csv(config.get("date_csv_path"))
    Origin=data['Org']
    Destination=data['Des']
    OriginFull=data['OrgFull']
    DestinationFull=data['DesFull']
    Countryo=data['Countryo']
    Countryd=data['Countryd']
    Sd=date_data['Date']
    distance=data['Distance']
    ###looping over Sectors
    for j in range(0,len(Sd)):
        ###Creating Lists for columns in dataframe
        orlist=[]
        destlist=[]
        datelist=[]
        dtlist=[]   
        atlist=[] 
        jtlist=[] 
        plist=[]  
        fidlist=[]
        captdatelist=[]
        fclist=[]
        jlist=[]
        bflist=[]
        tflist=[]
        stoplist=[]
        captimelist=[]
        distlist=[]
        timeslot=[]
        ###Inserting Headers for Columns lists
        fclist.append('Airline')
        orlist.append('Origin')
        destlist.append('Destination')
        datelist.append('Dept_Date')
        dtlist.append('Dept_Time')
        atlist.append('Arr_Time')   
        jtlist.append('Duration')
        plist.append('Total_Price')
        captdatelist.append('Cap_Date')
        fidlist.append('Flight_Code')
        jlist.append('Duration')
        bflist.append('Base')
        tflist.append('Fuel_Tax')
        stoplist.append('Stop')
        captimelist.append('Cap_Time')
        distlist.append('Distance')
        timeslot.append('Time_Slot')
        String_date_new=Sd[j]
        Sd1=String_date_new.split('/')
        String_date=Sd1[1]+'/'+Sd1[0]+'/'+Sd1[2]
        print(String_date)
        for i in range(0,len(Origin)):
            org=Origin[i]
            dest=Destination[i]
            orgfull=OriginFull[i]
            destfull=DestinationFull[i]
            countryo=Countryo[i]
            countryd=Countryd[i]
            Distance=distance[i]
            ###String_date=config.get("data_extract_date")

            fclist,fidlist,jlist,orlist,destlist,datelist,dtlist,atlist,plist,bflist,tflist,captdatelist,stoplist,captimelist,distlist,timeslot=get_flight_details([org, dest, String_date,String_date_new,orgfull,destfull,countryo,countryd,fclist,fidlist,jlist,orlist,destlist,datelist,dtlist,atlist,plist,bflist,tflist,captdatelist,stoplist,captimelist,distlist,Distance,timeslot])                                                                                            
            
        captdatelist=list(map(lambda x: str.replace(x, "/", "-"), captdatelist))
        ###Saving List-Dataframe-csv
        ##Cap_Date|Cap_Time|Time_Slot|Origin|Destination|Distance|Dept_Date|Airline|Flight_ID|Dept_Time|Arr_Time|Duration|Stop|Base|Fuel_Tax|Total_Price
        list1=[captdatelist,captimelist,timeslot,orlist,destlist,distlist,datelist,fclist,fidlist,dtlist,atlist,jlist,stoplist,bflist,tflist,plist]
        dicttodf = {}
        for l2 in list1:
            dicttodf[l2[0]] = l2[1:]

        dataframeasemytrip = pd.DataFrame(dicttodf) 
        
        String_date_new = String_date.replace('/', '-')
        now = datetime.datetime.now()
        CaptString_date=now.strftime("%m-%d-%Y")
        Timeslot=now.strftime('%H')
    
        #dataframeasemytrip.to_csv(r'E:\Drive\Scrapped data\Ad-Hoc Scrape\2 PM\Output\Scrapped\Scrapped_'+CaptString_date+"_"+Timeslot+"_"+String_date_new+'.csv',index=False)
        exe = exceptnDiff(dataframeasemytrip)
        exe.to_csv(r'D:\Scrappers\Run_Daily\Output\Price_Diff_'+CaptString_date+"_"+Timeslot+"_"+String_date_new+'.csv',index=False)

        print("Data Saved")
    print("---Script took %s seconds --- : " % (time.time() - start_time))

    
main()
    
