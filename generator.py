import argparse
import datetime
import logging
import random
import sys
from itertools import accumulate
from operator import add

import pandas as pd
import rstr

PATTERN_REGEX_DIC = {
    "Response": "[^{0}]*({0}[^{1}]*{1}[^{0}]*)*",
    "Alternating": "[^{0}{1}]*({0}[^{0}{1}]*{1}[^{0}{1}]*)*",
    "Multieffect": "[^{0}{1}]*({0}[^{0}{1}]*{1}[^{0}]*)*",
    "Multicause": "[^{0}{1}]*({0}[^{1}]*{1}[^{0}{1}]*)*"
}


class SyntheticTraceGenerator:
    def __init__(self, regex=None, temporalPattern=None, alpbhabetLen=0, traceLength=1000):
        self.regexPattern = regex
        self.temporalPattern = temporalPattern
        self.alphabetLen = max(2, min(26, alpbhabetLen))
        self.traceLength = max(1000, traceLength)

        if temporalPattern != None:
            self.regexPattern = PATTERN_REGEX_DIC[self.temporalPattern].format("a", "b")

    def __getTime(self, deltaDistribution):
        """
            Add delta to timestamp epoch

            :param deltaDistribution:
            :return: Timestamp formated as datetime
        """
        current_time_sec = datetime.datetime.now().timestamp()
        dateTime = [current_time_sec] * len(deltaDistribution)
        for i, ele in enumerate(dateTime):
            dateTime[i] = datetime.datetime.now() + datetime.timedelta(seconds=deltaDistribution[i])

        return dateTime

    def __getFrame(self, trace, time):
        """
            Convert into a valid pandas dataframe

            :param trace:
            :param time:

            :return: pandas dataframe
        """
        traceFrameDF = pd.DataFrame([time, trace]).T
        traceFrameDF.columns = ["Timestamp", "Event"]
        traceFrameDF['Timestamp'] = pd.to_datetime(traceFrameDF['Timestamp'])
        traceFrameDF['Timestamp'] = traceFrameDF['Timestamp'].apply(lambda x: x.strftime("%B %d, %Y %I:%M:%S"))

        return traceFrameDF

    def __getTrace(self, pattern='ab+ac', windowTimeLengthVariability=5):
        """
            Functionality to generate the trace using the pattern
            It then creates the appropriate timestamp with random time delta

            :param pattern:
            :param windowTimeLengthVariability:

            :return: Trace Data Frame
        """
        deltaDistribution = []

        trace = ""
        while len(trace) < self.traceLength:
            trace += rstr.xeger(pattern)

        deltaDistribution.extend(
            list((random.randint(1, max(1, windowTimeLengthVariability)) for e in range(1, len(trace) + 1))))
        time = list(accumulate(deltaDistribution, add))
        time = self.__getTime(time)

        syntheticDF = self.__getFrame(trace, time)

        return syntheticDF

    def save(self, traceFrameDF):
        """
            Functionilty to save the synthetic trace

            :param traceFrameDF:
        """
        try:
            traceFrameDF.to_csv("synthetic_trace.csv", index=False)
            logging.info("Synthetic trace saved successfully.")
        except:
            logging.error("Can't save trace file")
            sys.exit(1)

    def generate(self):
        """
            Generate the synthetic trace
        """
        traceFrame = self.__getTrace(self.regexPattern)
        logging.info("Synthetic Trace generated")
        self.save(traceFrame)

def main():
    logging.basicConfig(
        filename='generator.log',
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    logging.getLogger('').addHandler(console)

    logging.debug("Enter either of the temporal pattern (Response/Alternate/MutliCause/MultiEffect) or regex pattern")
    parser = argparse.ArgumentParser(description="Synthetic trace generator")
    parser.add_argument('--regex', help="A valid regex pattern")
    parser.add_argument('--alphabetLen', help="Length of alphabet (max 26)", type=int, default=2)
    parser.add_argument('--temporalPattern', help="Temporal pattern")
    parser.add_argument('--traceLength', type=int, default=100)
    args = parser.parse_args()

    if args.regex == None and args.temporalPattern == None:
        logging.error("Either regex pattern or temporalPattern is required. None found")
        sys.exit(0)

    if args.temporalPattern and args.temporalPattern not in PATTERN_REGEX_DIC.keys():
        logging.error("temporalPattern must be valid")
        sys.exit(0)

    syntheticGen = SyntheticTraceGenerator(args.regex, args.temporalPattern, args.alphabetLen, args.traceLength)
    syntheticGen.generate()


if __name__ == "__main__":
    main()
