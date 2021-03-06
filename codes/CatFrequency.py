import matplotlib.pyplot as plot
import datetime
from dateutil.parser import parse





################## function 7 -Identify the frequency of each request from each category###############################
# Done by: <Ivan Goh Jun Hao> <1700103>
global feedbackinfo_list
feedbackinfo_list = []
numberofrows = 1

freqofFeedback = float(0)
freqofComplaints = float(0)
freqofcompliments = float(0)
freqofOthers = float(0)

def get_category_total(datadict, category):
        """Method to return total items of a category regardless of date"""
        total = 0
        if category not in datadict:
            return total
        cat_dict = datadict[category]

        for day in cat_dict['ack'].keys():
            total = total + int(cat_dict['ack'][day])
        return total
    #Method to get acknowledgement/completion request of a specific day

# Loop thru csv rows
def set_data(feedbackinfo):
    # This is a global dictionary to store accumulated data for the frequency and average request analysis
    global datadict
    datadict = {
        'Feedback': {},
        'Complaints': {},
        'Others/Request for Information': {},
        'Compliment': {},
        'total': len(feedbackinfo),
        'total_feedback': 0,
        'total_compliments': 0,
        'total_complaints': 0,
        'total_others': 0,
        'average_request_time': 0
    }
    total_report_time = datetime.datetime.now() - datetime.datetime.now()
    feedbackinfo_list = feedbackinfo
    for row in range(0, len(feedbackinfo_list)):
            # 1)Obtain category, ack datetime, comp datetime from each row
            category = feedbackinfo_list[row].category
            ack_date = feedbackinfo_list[row].acknowledge_date_time
            comp_date = feedbackinfo_list[row].completed_date_time
            report_date = feedbackinfo_list[row].report_date_time
            ack_dt = None
            comp_dt = None
            report_dt = None

            # 2) check if ack date is not None
            if len(ack_date) != 0 and not (ack_date == 'NA' or ack_date == 'in progress'):
                # if not None or not NA
                # convert datetime to date
                ack_dt = parse(ack_date)

                ack_date = ack_dt.strftime("%d/%m/%Y")

            if len(ack_date) == 0:
                ack_date = 'blank'
            elif (ack_date == 'in progress'):
                ack_date = 'progress'
            elif len(ack_date) == 2:
                ack_date = 'not_applicable'

            if 'ack' not in datadict[category]:
                datadict[category]['ack'] = {
                    'blank': 0,
                    'progress': 0,
                    'not_applicable': 0
                }
            # print(ack_date)
            # check if date is alrd in datadict
            if ack_date not in datadict[category]['ack']:
                # if not yet added, initialize entry
                datadict[category]['ack'][ack_date] = 1
            else:
                # else increment counter
                datadict[category]['ack'][ack_date] = datadict[category]['ack'][ack_date] + 1

            # 3 check if comp date is not None
            if len(comp_date) != 0 and not (comp_date == 'NA' or comp_date == 'in progress'):
                # if not None
                # convert
                comp_dt = parse(comp_date)
                # print comp_dt
                comp_date = comp_dt.strftime("%d/%m/%Y")

                # print(comp_date=='in progress')
            # check if comp is alrd in datadict
            if 'comp' not in datadict[category]:
                datadict[category]['comp'] = {
                    'blank': 0,
                    'progress': 0,
                    'not_applicable': 0
                }

            if len(comp_date) == 0:
                # if date is None, set it to 'blank'
                comp_date = 'blank'
            elif comp_date == 'in progress':
                comp_date = 'progress'
            elif len(comp_date) == 2:
                comp_date = 'not_applicable'

            if comp_date not in datadict[category]['comp']:
                # if not yet added, initialize entry
                datadict[category]['comp'][comp_date] = 1
            else:
                # else increment counter
                datadict[category]['comp'][comp_date] = datadict[category]['comp'][comp_date] + 1

            # 4 compare ack_dt and comp_dt to find avg time against report_dt
            if not ack_dt and not comp_dt:
                continue
            else:
                report_dt = parse(report_date)
                if not ack_dt:
                    total_report_time = total_report_time + (comp_dt - report_dt)
                elif not comp_dt:
                    total_report_time = total_report_time + (ack_dt - report_dt)
                else:
                    dt_list = []
                    dt_list.append(comp_dt)
                    dt_list.append(ack_dt)
                    min_dt = min(dt_list)
                    total_report_time = total_report_time + (min_dt - report_dt)
        #set the reporting total time in seconds
    total_time_in_sec = total_report_time.total_seconds()

    datadict['average_request_time'] = total_time_in_sec / datadict.get('total')

    datadict['total_feedback'] = get_category_total(datadict, 'Feedback')
    datadict['total_compliments'] = get_category_total(datadict, "Compliment")
    datadict['total_complaints'] = get_category_total(datadict, "Complaints")
    datadict['total_others'] = get_category_total(datadict, "Others/Request for Information")


#1) Get the frequency of each request and plot pie chart(Note: Function does not require inputs to be executed)
def getFrequency(feedbackinfo):

    set_data(feedbackinfo)
    """Plots a frequency graph for up to 4 labelled values"""
    def plot_graph(title, labels, values):
        def create_autopct(totalreq):
            def req_autopct(percent):
                total = sum(totalreq)
                percentile = int(round(percent * total / 100.0))
                return '{p:.2f}%  ({v:d})'.format(p=percent, v=percentile)

            return req_autopct

        explode = (0.1, 0.1, 0.1, 0.1)

        plot.figure("Frequency of each different category").add_axes(([0.1, 0.1, 0.8, 0.8]))
        totalreq = values
        plot.pie(totalreq, labels=labels, autopct=create_autopct(totalreq), explode=explode, startangle=90)
        plot.title(title, bbox={'facecolor': '0.8', 'pad': 2})
        plot.legend(labels, loc="best")


        return plot


    # Get Category Feedback Frequency Result
    feedbackcounter = datadict['total_feedback']
    complaincounter = datadict['total_complaints']
    otherreqcounter = datadict['total_others']
    complimentcounter = datadict['total_compliments']
    global totalfeedback,totalcomplaints,totalcompliments,totalothers
    totalfeedback= float(feedbackcounter)
    totalcomplaints = float(complaincounter)
    totalcompliments = float(complimentcounter)
    totalothers = float(otherreqcounter)


    labels = ["Complaints", "Feedback", "Compliment", "Others"]
    title = 'Frequency of Each Request from All Categories'
    values = [totalcomplaints, totalfeedback, totalcompliments, totalothers]
    return plot_graph(title=title,labels=labels,values=values)

    #Set Pie Chart data and generate pie chart of Frequency for each request


# 2)Function to call  when generating Histograph of specific request
# Requires users to select a string item "Feedback,Complaints,Compliment or Others" and string status "Completed or Acknowledged" in order for histogram to work
def GenerateHistograph(itemselect,status,feedbackinfo):
    set_data(feedbackinfo)
    avgreqtime = str(datetime.timedelta(seconds=datadict.get('average_request_time')))
    #Method to Create Histogram for Data Retrieval of
    def CreateHisto(data,label,title):
        plot.figure('Request_Analysis_Histogram')
        plot.rcParams['xtick.major.pad']='5'
        plot.bar(range(len(data)), data.values())
        plot.xticks(range(len(data)), data.keys(), rotation=50,fontsize=8,ha='right')
        plot.legend(label,loc='upper left', shadow=True, ncol=1,fontsize=12)
        plot.title(title, bbox={'facecolor': '0.8', 'pad': 2})
        plot.subplots_adjust(bottom=0.0)
        plot.tight_layout()
        return plot
    #Try catch user selection when running in the
    try:
        if itemselect=="Feedback":
            if status == "Completed":
                hislab="Feedback"
                histit="Average Request Response Time:{}".format(avgreqtime)
    # Generate Histogram for all completed request
                return CreateHisto(datadict['Feedback']['comp'],label=hislab,title=histit)
            elif status == "Acknowledged":
                hislab = "Feedback"
                histit = "Average Request Response Time:{}".format(avgreqtime)
                # Generate Histogram for all acknowledge request
                return CreateHisto(datadict['Feedback']['ack'], label=hislab, title=histit)
        elif itemselect=="Complaints":
            if status == "Completed":
                    hislab="Complaints"
                    histit="Average Request Response Time:{}".format(avgreqtime)
    # Generate Histogram for all completed request
                    return CreateHisto(datadict['Complaints']['comp'],label=hislab,title=histit)
            elif status == "Acknowledged":
                    hislab = "Complaints"
                    histit = "Average Request Response Time:{}".format(avgreqtime)
            # Generate Histogram for all completed request
                    return  CreateHisto(datadict['Complaints']['ack'], label=hislab, title=histit)
        elif itemselect=="Compliment":
            if status=="Completed":
                    hislab="Compliment"
                    histit="Average Request Response Time:{}".format(avgreqtime)
                    CreateHisto(datadict['Compliment']['comp'], label=hislab, title=histit)
            elif status=="Acknowledged":
                    hislab = "Compliment"
                    histit = "Average Request Response Time:{}".format(avgreqtime)
                    return CreateHisto(datadict['Compliment']['ack'], label=hislab, title=histit)
        elif itemselect=="Others/Request for Information":
            if status == "Completed":
                hislab = "Others/Request for Information"
                histit = "Average Request Response Time:{}".format(avgreqtime)
                return CreateHisto(datadict['Others/Request for Information']['comp'], label=hislab, title=histit)
            elif status == "Acknowledged":
                hislab = "Others/Request for Information"
                histit = "Average Request Response Time:{}".format(avgreqtime)
                return CreateHisto(datadict['Compliment']['ack'], label=hislab, title=histit)

    except ValueError:
        print "Invalid input please try again"

