import matplotlib.pyplot as plt
import numpy as np
import copy

def calculateLoanAndInterest(totalloan,months,interestRate,flag,runningloan=0,acc_loan=0,acc_inter=0,rounds=0,roundCount=1,step=0,stepOut=[]):
    #### in a recursive way and only return the acc_loan and interest of the 
    monthly_rate=interestRate/12/100
    stepOut=stepOut
    roundCount=roundCount
    if rounds:
        pass
    else:
        rounds=months
    if roundCount <=rounds:
        if flag:
            #等额本息
            if runningloan>0:
                dueInterest=runningloan*monthly_rate
                dueLoan=totalloan*monthly_rate*((1+monthly_rate)**months)/((1+monthly_rate)**(months)-1)-dueInterest
            else:
                #first run init
                dueInterest=totalloan*monthly_rate
                dueLoan=totalloan*monthly_rate*((1+monthly_rate)**months)/((1+monthly_rate)**(months)-1)-dueInterest
        else:
            #等额本金
            if runningloan >0:
                dueInterest=runningloan*monthly_rate
                dueLoan=totalloan/months
            else:
                dueInterest=totalloan*monthly_rate
                dueLoan=totalloan/months

        acc_loan+=dueLoan
        acc_inter+=dueInterest

        if step >0 and roundCount >0:
            if roundCount%step ==0:
                stepOut.append((acc_loan,acc_inter,dueLoan,dueInterest,dueLoan+dueInterest))
                print('Loan is:{:.3f},Int is {:.3f}, Sum is {:.3f}'.format(dueLoan,dueInterest,dueLoan+dueInterest))
                # print (roundCount)


        roundCount+=1
        return calculateLoanAndInterest(totalloan,int(months),interestRate,flag,totalloan-acc_loan,acc_loan,acc_inter,rounds,roundCount,step,stepOut)
    else:
        return (acc_loan,acc_inter,stepOut)



def calculateLoadAndInterests(inputparameters,flag=False):
    parameters=copy.deepcopy(inputparameters)
    lowInterestMonthCount=parameters['lowInterestLoanLength']*12
    monthCount=parameters['loanLength']*12
    ##Interest rate Calculation
    monthlyRate_Business=(parameters['businessLoanBaseRate']+parameters['businessLoadfloatingRate'])/12/100
    monthlyRate_LowInterest=(parameters['lowInterestLoanRate'])/12/100
    if flag:
        # 1。等额本息贷款计算公式:
        # 每月还款金额 (简称每月本息) =
        # 贷款本金 X	月利率×[（1+月利率）^ 还款月数 ]
        # ----------------------------------
        # [（1+月利率）^ 还款月数 ] - 1
        ### Interest 等额本息
        if parameters["runningBusinessLoan"]*parameters['runningLowInterestLoan']:
            if parameters['runningBusinessLoan'] >0:

                dueBusinessInterest=parameters['runningBusinessLoan']*monthlyRate_Business
                dueBusinessLoan=parameters['businessLoan']*monthlyRate_Business*((1+monthlyRate_Business)**monthCount)/((1+monthlyRate_Business)**(monthCount)-1)-dueBusinessInterest

            else:
                dueBusinessInterest=0
                dueBusinessLoan=0


            if parameters['runningLowInterestLoan'] > 0:
                dueLowInterestInterest=parameters['runningLowInterestLoan']*monthlyRate_LowInterest
                dueLowInterestLoan=parameters['lowInterestLoan']*monthlyRate_LowInterest*((1+monthlyRate_LowInterest)**lowInterestMonthCount)/((1+monthlyRate_LowInterest)**(lowInterestMonthCount)-1)-dueLowInterestInterest
            else:
                dueLowInterestInterest=0
                dueLowInterestLoan=0

        else:
            #Interest calculated on first run when running number is 0
            dueBusinessInterest=parameters['businessLoan']*monthlyRate_Business
            dueBusinessLoan=parameters['businessLoan']*monthlyRate_Business*((1+monthlyRate_Business)**monthCount)/((1+monthlyRate_Business)**(monthCount)-1)-dueBusinessInterest

            dueLowInterestInterest=parameters['lowInterestLoan']*monthlyRate_LowInterest
            dueLowInterestLoan=parameters['lowInterestLoan']*monthlyRate_LowInterest*((1+monthlyRate_LowInterest)**lowInterestMonthCount)/((1+monthlyRate_LowInterest)**(lowInterestMonthCount)-1)-dueLowInterestInterest

        ##Due LoanCalculation 等额本息
        # dueBusinessLoan=parameters['businessLoan']*monthlyRate_Business*((1+monthlyRate_Business)**monthCount)/((1+monthlyRate_Business)**(monthCount)-1)-dueBusinessInterest
        # dueLowInterestLoan=parameters['lowInterestLoan']*monthlyRate_LowInterest*((1+monthlyRate_LowInterest)**lowInterestMonthCount)/((1+monthlyRate_LowInterest)**(lowInterestMonthCount)-1)-dueLowInterestInterest


    else:
        # 2。等额本金贷款计算公式:
        # 每月还款金额 (简称每月本息) =
        # （贷款本金 / 还款月数） + (本金 - 已归还本金累计额) X 每月利率
        #Due Interest  Calculation 等额本金
        if parameters["runningBusinessLoan"]*parameters['runningLowInterestLoan']:
            if parameters['runningBusinessLoan'] >0:

                dueBusinessInterest=parameters['runningBusinessLoan']*monthlyRate_Business
                dueBusinessLoan=parameters['businessLoan']/monthCount

            else:
                dueBusinessInterest=0
                dueBusinessLoan=0

            if parameters['runningLowInterestLoan'] >0:

                dueLowInterestInterest=parameters['runningLowInterestLoan']*monthlyRate_LowInterest
                dueLowInterestLoan=parameters['lowInterestLoan']/lowInterestMonthCount

            else:
                dueLowInterestInterest=0
                dueLowInterestLoan=0
        else:
            #Interest calculated on first run when running number is 0
            dueBusinessInterest=parameters['businessLoan']*monthlyRate_Business
            dueBusinessLoan=parameters['businessLoan']/monthCount

            dueLowInterestInterest=parameters['lowInterestLoan']*monthlyRate_LowInterest
            dueLowInterestLoan=parameters['lowInterestLoan']/lowInterestMonthCount

        #Due Loan Calculation 等额本金
        # dueBusinessLoan=parameters['businessLoan']/monthCount
        # dueLowInterestLoan=parameters['lowInterestLoan']/lowInterestMonthCount



    # print ('--------'*10)
    # print ('Business:{},lowInterest:{}'.format(dueBusinessInterest+dueBusinessLoan,dueLowInterestInterest+dueLowInterestLoan))
    # print ('========='*5)

    ##Remaining Loan calculation
    # remainingBusinessLoan=parameters['businessLoan']-dueBusinessLoan
    # remainingLowInterestLoan=parameters['lowInterestLoan']-dueLowInterestLoan

    ##assigning the value
    if parameters["runningBusinessLoan"]*parameters['runningLowInterestLoan']:
        parameters['runningBusinessLoan']=parameters['runningBusinessLoan']-dueBusinessLoan
        parameters['runningLowInterestLoan']=parameters['runningLowInterestLoan']-dueLowInterestLoan
    else:
        parameters['runningBusinessLoan']=parameters['businessLoan']-dueBusinessLoan
        parameters['runningLowInterestLoan']=parameters['lowInterestLoan']-dueLowInterestLoan


    ##Calculating Summary
    parameters['AccInterest']+=dueBusinessInterest+dueLowInterestInterest
    parameters['AccLoans']+=dueBusinessInterest+dueBusinessLoan+dueLowInterestInterest+dueLowInterestLoan

    return parameters


# parameters1= {
#     "runningBusinessLoan":0,
#     'runningLowInterestLoan':0,
#     "baseLoan":190,
#     "lowInterestLoan":60,
#     "businessLoan":130,
#     "lowInterestLoanRate":3.25,
#     "businessLoanBaseRate":4.25,
#     "businessLoadfloatingRate":0.4,
#     "loanLength":15,
#     "lowInterestLoanLength":30,
#     "AccInterest":0,
#     "AccLoans":0,
#     # "AccBusinessLoan"
# }
# parameters2= {
#     "runningBusinessLoan":0,
#     'runningLowInterestLoan':0,
#     "baseLoan":190,
#     "lowInterestLoan":60,
#     "businessLoan":130,
#     "lowInterestLoanRate":3.25,
#     "businessLoanBaseRate":4.25,
#     "businessLoadfloatingRate":0.4,
#     "loanLength":15,
#     "lowInterestLoanLength":30,
#     "AccInterest":0,
#     "AccLoans":0,
#     # "AccBusinessLoan"
# }

# accumulatedLoad=[]
# accumulatedInterest=[]
# accumulatedLoad1=[]
# accumulatedInterest1=[]
# sum1=[]
# sum2=[]
# for i in range(1,361): 
#     parameters2=calculateLoadAndInterests(parameters1,False)
#     accumulatedLoad.append(parameters2['AccLoans'])
#     accumulatedInterest.append(parameters2['AccInterest'])
#     sum1.append(parameters2['AccLoans']-parameters2['AccInterest'])



# for i in range(1,361): 
#     parameters3=calculateLoadAndInterests(parameters1,True)
#     accumulatedLoad1.append(parameters3['AccLoans'])
#     accumulatedInterest1.append(parameters3['AccInterest'])
#     sum2.append(parameters3['AccLoans']-parameters3['AccInterest'])


# print (parameters1)
# print (parameters2)


# acc_loan=[]
# acc_inter=[]
# acc_loan1=[]
# acc_inter1=[]
# for i in range (12,361,12):
#     # print (calculateLoanAndInterest(130,i,4.65,False))
#     acc_loan.append(calculateLoanAndInterest(130,i,4.65,False)[0])
#     acc_inter.append(calculateLoanAndInterest(130,i,4.65,False)[1])
#     acc_loan1.append(calculateLoanAndInterest(130,i,4.65,True)[0])
#     acc_inter1.append(calculateLoanAndInterest(130,i,4.65,True)[1])


# print (axis_x)
# print (acc_loan)

loan=145
monthsCount=240
interestRate=4.65

axis_x=np.arange(1,361,12)
result=calculateLoanAndInterest(loan,monthsCount,interestRate,True,step=12,stepOut=[])
result1=calculateLoanAndInterest(loan,monthsCount,interestRate,False,step=12,stepOut=[])
print(result[0],result[1],result[0]+result[1])
print (result1[0],result1[1],result1[0]+result1[1])

print (result[2])
# sum1=[]
# sum2=[]
# print (result)
# for i in range(1,len(result[2])+1):
#     sum1.append(result[2][i-1][0]+result[2][i-1][1])
#     sum2.append(result1[2][i-1][0]+result1[2][i-1][1])
# # print ([item[0] for item in result[2]])

# plt.plot(axis_x,[item[0] for item in result[2]],'r-.',axis_x,[item[1] for item in result[2]],'r--',axis_x,sum1,'r-',axis_x,[item[0] for item in result1[2]],'g-.',axis_x,[item[1] for item in result1[2]],'g--',axis_x,sum2,'g-')

# plt.annotate(u'Red：Ben Jin',(300,1))

# # plt.text(1,250,"BusLoanLength:"+str(parameters1['loanLength']))

# # for x,y in zip(axis_x,accumulatedLoad1):
# #     if x%30 ==0:
# #         plt.text(x,y,round(y))

# # for x,y in zip(axis_x,accumulatedInterest1):
# #     if x%30 ==0:
# #         plt.text(x,y,round(y))

# plt.show()



