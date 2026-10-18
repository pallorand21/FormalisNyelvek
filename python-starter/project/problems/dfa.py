from project.problem import Problem
import argparse

class dfafeladat(Problem):

    def initialize_parser(self, parser: argparse.ArgumentParser):
        parser.add_argument('--check', type=str, help='word check')

    def is_chosen_problem(self, args):
        return bool(args.check)

    def run(self, args):
        input = args.input
        out = args.output
        words = args.check

        testwords = words.split(",") if words else []
        start, end, transition = self.dfa_read(input)

        results = []
        for word in testwords:
            results.append(self.check(word, start, end, transition))

        with open(out, "w") as f:
            for res in results:
                f.write(res + "\n")

    def dfa_read(self, filename):
        with open(filename, "r") as f:
            #nem ures sorok beolvasasa
            rows = [row.strip() for row in f if row.strip()]

        
        start = rows[2]
        end = set(rows[3].split())

        transition = {}
        for sor in rows[4:]:
            parts = sor.split()
            if len(parts) == 3:
                fromm, word, where = parts
                transition[(fromm, word)] = where
        return start, end, transition

    def check(self, word, start, end, transition):
        #startallapot
        actually = start
        for wordd in word:
            key = (actually, word)
            if key in transition:
                actually = transition[key]
            else:
                return "NEM"
        return "IGEN" if actually in end else "NEM"