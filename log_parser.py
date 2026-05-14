import re
from collections import Counter, defaultdict


class BioSeqLogParser:

    def __init__(self, logfile):
        self.logfile = logfile
        self.logs = []

    def parse(self):

        with open(self.logfile, "r") as file:

            for line in file:

                line = line.strip()

                match = re.match(
                    r"^(.*?) (INFO|WARNING|ERROR) (.*)$",
                    line
                )

                if not match:
                    continue

                timestamp, level, message = match.groups()

                self.logs.append({
                    "timestamp": timestamp,
                    "level": level,
                    "message": message
                })

    def count_errors(self):

        return len([
            log for log in self.logs
            if log["level"] == "ERROR"
        ])

    def alignment_stats(self):

        scores = []

        for log in self.logs:

            if "ALIGNMENT" in log["message"]:

                score_match = re.search(
                    r"score=(\d+)",
                    log["message"]
                )

                if score_match:
                    scores.append(int(score_match.group(1)))

        if not scores:
            return None

        return {
            "count": len(scores),
            "max": max(scores),
            "min": min(scores),
            "average": sum(scores) / len(scores)
        }

    def most_common_errors(self):

        errors = []

        for log in self.logs:

            if log["level"] == "ERROR":

                reason_match = re.search(
                    r"reason=([a-zA-Z_]+)",
                    log["message"]
                )

                if reason_match:
                    errors.append(reason_match.group(1))

        return Counter(errors)

    def motif_statistics(self):

        motifs = defaultdict(int)

        for log in self.logs:

            if "MOTIF" in log["message"]:

                motif_match = re.search(
                    r"motif=([A-Z]+)",
                    log["message"]
                )

                if motif_match:
                    motifs[motif_match.group(1)] += 1

        return dict(motifs)