# DSP(Digital Signal Processing)

Digital Signal Processing (DSP) refers to the use of digital processing techniques to manipulate and analyze signals. DSP involves the use of mathematical algorithms to analyze, filter, and transform these signals.

## Final Project- DTMF

The final project was centered around the application of Dual Tone Multi Frequency (DTMF). 

![table 1](finalLab/image (1).png)
Table 1 displays the frequencies and corresponding symbols utilized in the Dual Tone Multi Frequency (DTMF) system. When a user presses a button on a phone keypad, two tones are generated, with one tone representing the row and the other representing the column. These two tones together define a symbol. The receiver continuously attempts to identify the correct symbol as it processes the incoming signal. During digital communication, errors in symbol identification occur during the transition from one symbol to the next, which is referred to as inter-symbol interference (ISI). Reducing ISI is crucial in improving data communication rates, as quickly detecting a symbol enables the time allotted to each symbol to be shorter.

My solution to this final project problem resulted in a mean inter-symbol interference (ISI) error rate of only 6%. This was achieved by implementing the appropriate filter and continuously processing the signal to obtain the desired output. Notably, errors tended to occur during the transition between frequencies. Minimizing ISI is critical to improving data communication rates, as it enables symbols to be detected more quickly and reduces the time associated with each symbol.

![Mean error](finalLab/image (2).png)

The detected symbol, envelope of the common frequencies, and the corresponding errors related to transitions are shown below.

![envolope graph](finalLab/image (3).png)
