#!/usr/bin/python

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import bootstrap
import sys
### Configuration

inputfile=sys.argv[-1];
data=[]

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


# Create a Pandas dataframe to keep the collected data
df=pd.DataFrame(data, columns=['numbytes', 'mbps'])

# Plot the data

# Group around the number of bytes, and produce the mean 
means=df.groupby('numbytes').mean()

# Calculate confidence intervals (via bootstrapping)
ci=[]
for n in df['numbytes'].unique():
    ci.append(bootstrap.bootstrap(df[df.numbytes == n].mbps.values, 100000, np.mean, 0.05))

# Do the plotting
fig=plt.figure()
ax=fig.add_subplot(111)

ax.set_title(inputfile)
ax.set_ylabel('Mean throughput (Mbps)')
ax.set_xlabel('Bytes per message')

# Create the plot, with lines and error bars
ax.errorbar(means.index,means.mbps.values,yerr=np.array(ci).T)

# Plot individual data points
ax.plot(df.numbytes.values, df.mbps.values, linestyle='', marker='+', color='r' )
#ax.set_ylim([0,100])
# For interactive plotting
# plt.show()

# Save output to PDF
plt.savefig("fig-{0}.pdf".format(inputfile))