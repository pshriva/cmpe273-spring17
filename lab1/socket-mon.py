import psutil
def main():
    tcpConnections = []
    groupedConnections = []
    processCount = []
    sortedConnections = []
    tcpConnections = get_tcp_Connections ('tcp') # stores all the tcp connections with process id, local and remote addresses and status
    groupedConnections = sorted(tcpConnections, key = lambda cc: cc[0], reverse = True) #stores tcp connections grouped by process id
    processCount = get_ProcessCount(groupedConnections) # stores number of connections per process along with process id
    sortedConnections = get_grouped_sorted_Connections(processCount,groupedConnections)  #stores tcp connections sorted according to number of occurances and grouped by process id
    display(sortedConnections) #displays the process id, laddr, raddr and status for all tcp connections as arranged in sortedConnections
def get_tcp_Connections(type):    #returns a list of process id, local and remote addresses and status for all tcp connections
    myConnections = []
    for c in psutil.net_connections(kind=type):
        laddr = "%s@%s" % (c.laddr)
        raddr = ""
        if c.raddr: #looks for all the processes with remote address present
            raddr = "%s@%s" % (c.raddr)
        if raddr and c.pid:    # checks if remote address is present or not
            myConn = (c.pid, laddr,raddr,c.status)
            myConnections.append(myConn) #stores values of process id, addresses and status for each tcp connection
    return myConnections
def get_ProcessCount(sortedlist = []):  #returns the count of each process along with process id arranged in decreasing order of occurances
    processCount = []
    sortedCount = []
    listsize = len(sortedlist)
    flag = 0
    count = 0
    prev_key = 0
    length = 0
    for s in sortedlist:
        length = length + 1
        key = s[0]
        if flag == 0:
            count = count + 1
            flag = 1
        elif prev_key == key and length != listsize:
            count = count + 1
        elif length == listsize:
            if prev_key == key:
                count = count +1
                currcount = (count,prev_key)
                processCount.append(currcount)
            else:
                currcount = (count,prev_key)
                processCount.append(currcount)
                currcount = (1, key)
                processCount.append(currcount)
        else:
            currcount = (count,prev_key)
            processCount.append(currcount)
            count = 1
        prev_key = key
    sortedCount = sorted(processCount, key = lambda cc: cc[0], reverse = True) # sorts
    return sortedCount
def get_grouped_sorted_Connections(processCount = [],groupedConnections = []): #returns tcp connection values grouped by process id and sorted according to number of connections
    groupedItems = []
    for pc in processCount:
        for gc in groupedConnections:
            if pc[1] == gc[0]:
                groupedItems.append(gc)
    return groupedItems
def display(sortedProcesses): #displays tcp connection values arranged by get_grouped_sorted_Connections()
    print "\"pid\",\"laddr\",\"raddr\",\"status\""
    for sp in sortedProcesses:
        print "\"%s\", \"%s\", \"%s\", \"%s\"" %(sp[0],sp[1],sp[2],sp[3])
if __name__ == '__main__':
    main()
