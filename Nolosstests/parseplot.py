#!/usr/bin/python

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import bootstrap

### Configuration

inputfiles= ['S2-SCTP-new',
             'DTLS-over-SCTP',
             'TLS-over-SCTP',
             'SCTP']

data=[]

def readdatafile(inputfile):

    with open(inputfile) as f:
        numbytes = speed = 0

        # Process each line in the file
        for line in f:
            if 'bytes' in line:
                numbytes=int(line.split()[-1])
            if ' bps' in line:
                # convert to Mbps 
                speed=int(line.split()[1]) / 1e6
            # Next block; store previously extracted data
            if 'Time' in line:
                data.append((numbytes, speed))

        # Store data from last block
        data.append((numbytes, speed))
    return data


columnindex=0

df=pd.DataFrame()

count=0
for infile in inputfiles:
    print "doing " + infile
    data=readdatafile(infile)
    dfloop=pd.DataFrame(data, columns=['numbytes', 'curve'+str(count)])
    dfloop=dfloop.set_index('numbytes')

    if len(df) == 0:
        df=dfloop
    else:
        # Now join with "big" dataframe
        df=df.join(dfloop)
        
    count=count+1
    data=[]

# Create a column with the index, for the grouping
df['numbytes']=df.index
# Group around the number of bytes, and produce the mean 

means=df.groupby('numbytes').mean()

# Plot the data

# Calculate confidence intervals (via bootstrapping)
ci0=[]
ci1=[]
ci2=[]
ci3=[]
#for n in df['numbytes'].unique():
    #ci0.append(bootstrap.bootstrap(df[df.numbytes == n].curve0.values, 100000, np.mean, 0.05))
    #ci1.append(bootstrap.bootstrap(df[df.numbytes == n].curve1.values, 100000, np.mean, 0.05))
    #ci2.append(bootstrap.bootstrap(df[df.numbytes == n].curve2.values, 100000, np.mean, 0.05))

# Do the plotting
fig=plt.figure()
ax=fig.add_subplot(111)


ax.set_title("")
ax.set_ylabel('Mean throughput (Mbps)')
ax.set_xlabel('Bytes per message')

# Create the plot, with lines and error bars

# REMOVE SCALING FACTORS BELOW! 1.10, 1.25 - just for illustration
# when same dataset is used!
#ax.errorbar(means.index,means.curve1.values,yerr=np.array(ci0).T, label="S2SCTP")
#ax.errorbar(means.index,means.curve1.values*1.10,yerr=np.array(ci1).T, label="S2SCTP test2")
#ax.errorbar(means.index,means.curve2.values*1.25,yerr=np.array(ci2).T, label="S2SCTP with 25% extra")
ax.errorbar(means.index,means.curve3.values, label="SCTP")
ax.errorbar(means.index,means.curve0.values, label="S2-SCTP")
ax.errorbar(means.index,means.curve1.values, label="DTLS-over-SCTP")
ax.errorbar(means.index,means.curve2.values, label="TLS-over-SCTP")


# Plot individual data points
#ax.plot(df.numbytes.values, df.curve1.values, linestyle='', marker='+', color='r' )
#ax.plot(df.numbytes.values, df.curve2.values, linestyle='', marker='+', color='r' )

ax.legend(loc='lower right')
# For interactive plotting
# plt.show()

# Save output to PDF
plt.savefig("fig-{0}.pdf".format("figuren"))