
from project.problem import Problem


class determinalizalas(Problem):


    def initialize_parser(self, parser):
        parser.add_argument(
        "--det",
        action="store_true",
        help="Determinizálási feladat jelezése"
    )

    def is_chosen_problem(self, args):
        return args.det 
        
    def run(self, args):
        if not args.det or not args.input or not args.output:
            return

        allapotok, abc, start, end, nfa_transition = self.nfa_read(args.input)

        dfa_allapotok, dfa_end, dfa_transition = self.determinalizalas(
            abc, start, end, nfa_transition
        )

        self.outwrite(args.output, dfa_allapotok, abc, dfa_end, dfa_transition)

    def nfa_read(self, file):
        with open(file, "r") as f:
            sorok = [sor.strip() for sor in f]

        allapotok = set(sorok[0].split())
        abc = sorok[1].split()
        start = sorok[2]
        end = set(sorok[3].split())

        nfa_transition = {}

        for sor in sorok[4:]:
            reszek = sor.split()

            if len(reszek) != 3:
                continue

            fromm, word, where = reszek

            if fromm in allapotok and where in allapotok and word in abc:
                key = (fromm, word)

                if key not in nfa_transition:
                    nfa_transition[key] = set()

                nfa_transition[key].add(where)

        return allapotok, abc, start, end, nfa_transition

    def determinalizalas(self, abc, start, end, nfa_transition):

        kezdohalmaz = frozenset([start])
        allapotnevek = {kezdohalmaz: "s0"}
        feldolgozando = [kezdohalmaz]

        dfa_transition = []
        dfa_end = set()

        if start in end:
            dfa_end.add("s0")

        i = 0
        while i < len(feldolgozando):
            aktualis = feldolgozando[i]
            aktualisnev = allapotnevek[aktualis]
            i += 1

            for betu in abc:
                ujhalmaz = set()

                for q in aktualis:
                    ujhalmaz.update(nfa_transition.get((q, betu), set()))

                if not ujhalmaz:
                    continue

                ujhalmaz = frozenset(ujhalmaz)

                if ujhalmaz not in allapotnevek:
                    ujnev = f"s{len(allapotnevek)}"
                    allapotnevek[ujhalmaz] = ujnev
                    feldolgozando.append(ujhalmaz)

                    if ujhalmaz & end:
                        dfa_end.add(ujnev)

                celnev = allapotnevek[ujhalmaz]
                dfa_transition.append((aktualisnev, betu, celnev))

        dfa_allapotok = list(allapotnevek.values())

        dfa_transition.sort(
            key=lambda t: (int(t[0][1:]), t[1], int(t[2][1:]))
        )

        dfa_end = sorted(dfa_end, key=lambda s: int(s[1:]))

        return dfa_allapotok, dfa_end, dfa_transition

    def outwrite(self, file, dfa_allapotok, abc, dfa_end, dfa_transition):
        with open(file, "w") as f:
            f.write(" ".join(dfa_allapotok) + "\n")
            f.write(" ".join(abc) + "\n")
            f.write("s0\n")
            f.write(" ".join(dfa_end) + "\n")

            for fromm, word, where in dfa_transition:
                f.write(f"{fromm} {word} {where}\n")
