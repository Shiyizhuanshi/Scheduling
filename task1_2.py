import numpy as np

JOB_NUM=31

G=np.zeros((JOB_NUM,JOB_NUM)) 
# G is the array that contains all the verticies

G[0, 30]=1;
G[1, 0]=1;
G[2, 7]=1;
G[3, 2]=1;
G[4, 1]=1;
G[5, 15]=1;
G[6, 5]=1;
G[7, 6]=1;
G[8, 7]=1;
G[9, 8]=1;
G[10, 0]=1;
G[11, 4]=1;
G[12, 11]=1;
G[13, 12]=1;
G[16, 14]=1;
G[14, 10]=1;
G[15, 4]=1;
G[16, 15]=1;
G[17, 16]=1;
G[18, 17]=1;
G[19, 18]=1;
G[20, 17]=1;
G[21, 20]=1;
G[22, 21]=1;
G[23, 4]=1;
G[24, 23]=1;
G[25, 24]=1;
G[26, 25]=1;
G[27, 25]=1;
G[28, 26]=1;
G[28, 27]=1;
G[29, 3]=1;
G[29, 9]=1;
G[29, 13]=1;
G[29, 19]=1;
G[29, 22]=1;
G[29, 28]=1

# processing times
p=[3,10,2,2,5,2,14,5,6,5,5,2,3,3,5,6,6,6,2,3,2,3,14,5,18,10,2,3,6,2,10] 
# due dates
d=[172,82,18,61,93,71,217,295,290,287,253,307,279,73,355,34,
 233,77,88,122,71,181,340,141,209,217,256,144,307,329,269]


class job():
    def __init__(self,id,processing_time,due_date,next_job=None):
        self.id=id
        self.processing_time=processing_time
        self.due_date=due_date
        self.next_job=next_job
        self.start_time=None
        self.completion_time=None



def init_jobs(G,p,d):
    job_num=len(p)
    jobs=[]
    for i in range(job_num):
        j=job(i,p[i],d[i],np.nonzero(G[i])[0])
        jobs.append(j)
    return jobs

# Function to calculate the lateness of a schedule
def calculate_lateness(schedule):
    max_lateness = 0
    total_lateness=0
    for job in schedule:
        job.lateness = max(0, job.completion_time - job.due_date)
        total_lateness+=job.lateness
        max_lateness = max(max_lateness, job.lateness)
    return max_lateness,total_lateness

def update_L(jobs,jobs_allocated,schedule):
    jobs_av=[]
    for job in jobs:
        if not (job in jobs_allocated):
            if not job.next_job.any() :
                    # print(job.id)
                    jobs_av.append(job)
            else:
                all_in_list = all(elem in schedule for elem in job.next_job)
                if all_in_list:
                    jobs_av.append(job)
    return jobs_av
        
def find_latest_d_j(jobs):
    """ this function finds the job with the largest due date
    the largest due date has the least cost as cost is calculated as max(0,(finish_time-duedate))s """
    latestjob=jobs[0]
    for job in jobs:
        if job.due_date > latestjob.due_date:
            latestjob=job
    return latestjob



def lcl_scheduling(G,p,d):
    # we select the job with earliest due date
    jobs=init_jobs(G,p,d)
    jobs_av=[]
    jobs_allocated=[]
    schedule=[]
    end_time=sum(p)
    i=0
    while len(jobs_allocated) <len(jobs):
        i+=1
        print("iteration "+str(i))
        jobs_av=update_L(jobs,jobs_allocated,schedule)
        # print("jobs available ")
        # print(jobs_av)
        lc_job=find_latest_d_j(jobs_av)
        print("available job with least cost "+str(lc_job.id))
        lc_job.completion_time=end_time
        lc_job.start_time=end_time-lc_job.processing_time
        end_time-=lc_job.processing_time

        jobs_allocated.append(lc_job)
        schedule.insert(0,lc_job.id)
        
        print("schedule ")
        print(schedule)
    # print(sum(p))
    print("the final job sequence is: ")
    print (schedule)
    max_late,total_late=calculate_lateness(jobs_allocated)
    print("total lateness is: ")
    print(total_late)
    print("max lateness is: ")
    print(max_late)
def main():
    lcl_scheduling(G,p,d)

main()