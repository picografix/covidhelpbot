from cowin_api import CoWinAPI
import pandas as pd
cowin = CoWinAPI()
def myprint(arr):
    an = ""
    mastercount=0
    for i in arr:
        an += "\nName:"+i['name']
        # an+= "\nSessions:"
        # print("Name:",i['name'])
        # print("Sessions:")
        count=0
        for j in i['sessions']:
            if(j['available_capacity']!=0):
                count+=1
                # an += "\nDate"+j['date']
                # print("Date",j['date'])
                an+= "\nAvailable: "+str(j['available_capacity'])
                # print("Available: ",j['available_capacity'])
                # print("Slots:")
                # an+="\nSlots:"
                # for k in j['slots']:
                   
                #     an+="\n"+k
            # print(an)    
            mastercount+=count
    
    if(mastercount==0):
        return "No Available slot for given day"
    
    return an
def driver(pin_code):
    # pin_code = "326001"
    # date = '08-05-2021'  # Optional. Default value is today's date
    # min_age_limit = 45
    try:
        available_centers = cowin.get_availability_by_pincode(pin_code)
    except:
        available_centers = cowin.get_availability_by_district(pin_code)
    
    return myprint(available_centers['centers'])


def states():
    myStates = cowin.get_states()
    ans=""
    for i in myStates['states']:
        ans+="\n"+str(i['state_id'])+" "+ i['state_name']
    return ans
def districts(id):
    ans=""
    state_id=id
    districts = cowin.get_districts(state_id)
    for i in districts['districts']:
        ans+="\n"+str(i["district_id"])+" "+i['district_name']
    return ans
# print(an)
# f = open("output.txt", "a")
# f.write("Now the file has more content!\n")
# f.close()

# #open and read the file after the appending:
# f = open("demofile2.txt", "r")
# print(f.read())