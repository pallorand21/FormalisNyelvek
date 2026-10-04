from project.problem import Problem
import argparse

class dfafeladat(Problem):

    def initialize_parser(self, parser: argparse.ArgumentParser):
        parser.add_argument('--check', type=str, help='szo ellenorzes')

    def is_chosen_problem(self, args):
        return bool(args.check)

    def run(self, args):
        be = args.input
        ki = args.output
        szavak = args.check

        teszszavak = szavak.split(",") if szavak else []
        kezdo, veg, atmenet = self.dfa_beolvasas(be)

        eredmenyek = []
        for szo in teszszavak:
            eredmenyek.append(self.ellenorzes(szo, kezdo, veg, atmenet))

        with open(ki, "w") as f:
            for eredmeny in eredmenyek:
                f.write(eredmeny + "\n")

    def dfa_beolvasas(self, filenev):
        with open(filenev, "r") as f:
            sorok = [sor.strip() for sor in f if sor.strip()]

        kezdo = sorok[2]
        veg = set(sorok[3].split())

        atmenet = {}
        for sor in sorok[4:]:
            reszek = sor.split()
            if len(reszek) == 3:
                honnan, betu, hova = reszek
                atmenet[(honnan, betu)] = hova
        return kezdo, veg, atmenet

    def ellenorzes(self, szo, kezdo, veg, atmenet):
        aktualis = kezdo
        for betu in szo:
            kulcs = (aktualis, betu)
            if kulcs in atmenet:
                aktualis = atmenet[kulcs]
            else:
                return "NEM"
        return "IGEN" if aktualis in veg else "NEM"