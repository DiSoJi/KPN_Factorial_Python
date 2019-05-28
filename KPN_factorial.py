from threading import Thread #Import threading
from queue import Queue #Import queing
import sys #Import system related functionalities

#Queues definition
mult_queue_a = Queue()
mult_queue_b = Queue()
delay_queue_1 = Queue()
delay_queue_2 = Queue()
split_queue = Queue()
#################
#Define Counter
counter = 1 
#################


#Define multiplication worker
def mult_worker():
        while True:
                a = mult_queue_a.get() #Get value from queue a
                b = mult_queue_b.get() #Get value from queue b
                delay_queue_1.put(a * b) #Put result in delay queue 1 (queue from the multiplication side)
                mult_queue_a.task_done() #"Anounce" task completion
                mult_queue_b.task_done() #"Anounce" task completion
                
#Define split worker       
def split_worker():
        while True:
                element = split_queue.get() #Get value from split queue
                delay_queue_2.put(element) #Put that value in delay queue 2 (queue from the split side)
                mult_queue_b.put(element) #Put that value in the multiply queue b
                split_queue.task_done() #"Anounce" task completion
                print (element) #Print to show functionality
                if element > 100000000000000000000: #Limit to prevent crazy printing
                        break
        #return to stop thread
        return 
#Delay function
def delay_worker():
        split_queue.put(1) 
        while True:
                split_queue.put(delay_queue_1.get()) #Put value from delay queue 1 into split queue
                delay_queue_1.task_done() #"Anounce" task completion

#Counter function
def counter_worker():
        global counter
        mult_queue_a.put(counter) #Put new value into a values queue
        while True:
                delay_queue_2.get() #Get value from delay queue 2
                mult_queue_a.put(counter) #Add counter again to a queue
                delay_queue_2.task_done() #"Anounce" task completion
                counter  = counter + 1 #Increase counter

def main():
        #Thread creation
        split_thread = Thread(target=split_worker)
        mult_thread = Thread(target=mult_worker)
        delay_thread = Thread(target=delay_worker)
        counter_thread = Thread(target=counter_worker)
        
        #Threads start
        split_thread.start()
        mult_thread.start()
        delay_thread.start()
        counter_thread.start()

  
if __name__== "__main__":
        main()    