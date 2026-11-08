from project.problem import Problem
import argparse


class minimalizalas(Problem):

    def initialize_parser(self, parser: argparse.ArgumentParser):
        parser.add_argument('--mini', action='store_true', help='automata minimalizálása')

    def is_chosen_problem(self, args):
        return bool(args.mini)

    def run(self, args):
        be = args.input
        ki = args.output

        allapotok, abc, kezdo, vegallapotok, atmenet = self.beolvasas(be)
        particio, index = self.minimalizal(allapotok, abc, kezdo, vegallapotok, atmenet)
        self.kiiras(ki, abc, kezdo, vegallapotok, atmenet, particio, index)

    def beolvasas(self, filenev):
        with open(filenev, 'r') as f:
            sorok = [sor.strip() for sor in f if sor.strip()]

        allapotok = sorok[0].split()
        abc = sorok[1].split()
        kezdo = sorok[2]
        vegallapotok = set(sorok[3].split())

        allapotok_halmaz = set(allapotok)
        abc_halmaz = set(abc)

        atmenet = {}
        for sor in sorok[4:]:
            reszek = sor.split()
            if len(reszek) != 3:
                continue
            honnan, betu, hova = reszek
            if honnan not in allapotok_halmaz or hova not in allapotok_halmaz or betu not in abc_halmaz:
                continue
            atmenet[(honnan, betu)] = hova

        return allapotok, abc, kezdo, vegallapotok, atmenet

    def minimalizal(self, allapotok, abc, kezdo, vegallapotok, atmenet):
        elerheto = {kezdo}
        stack = [kezdo]
        while stack:
            aktual = stack.pop()
            for betu in abc:
                cel = atmenet.get((aktual, betu))
                if cel and cel not in elerheto:
                    elerheto.add(cel)
                    stack.append(cel)

        index = {allapot: i for i, allapot in enumerate(allapotok)}

        particio = {a: (1 if a in vegallapotok else 0) for a in elerheto}

        while True:
            csoport_id = {}
            uj_cimke = {}
            for allapot in sorted(elerheto, key=lambda a: index[a]):
                szignatura = (particio[allapot],) + tuple(
                    particio.get(atmenet.get((allapot, betu)), -1) for betu in abc
                )
                if szignatura not in csoport_id:
                    csoport_id[szignatura] = len(csoport_id)
                uj_cimke[allapot] = csoport_id[szignatura]

            if len(set(uj_cimke.values())) == len(set(particio.values())):
                particio = uj_cimke
                break
            particio = uj_cimke

        return particio, index

    def kiiras(self, ki, abc, kezdo, vegallapotok, atmenet, particio, index):
        csoport_tagok = {}
        for allapot, cimke in particio.items():
            csoport_tagok.setdefault(cimke, []).append(allapot)

        csoport_nev = {
            cimke: f"s{index[min(tagok, key=lambda a: index[a])]}"
            for cimke, tagok in csoport_tagok.items()
        }

        uj_allapotok = sorted(set(csoport_nev.values()), key=lambda s: int(s[1:]))
        uj_kezdo = csoport_nev[particio[kezdo]]
        uj_vegallapotok = sorted(
            {csoport_nev[particio[a]] for a in vegallapotok if a in particio},
            key=lambda s: int(s[1:])
        )

        uj_atmenetek = {
            (csoport_nev[particio[honnan]], betu, csoport_nev[particio[hova]])
            for (honnan, betu), hova in atmenet.items()
            if honnan in particio and hova in particio
        }
        rendezett = sorted(uj_atmenetek, key=lambda t: (int(t[0][1:]), t[1], int(t[2][1:])))

        with open(ki, 'w') as f:
            f.write(' '.join(uj_allapotok) + '\n')
            f.write(' '.join(abc) + '\n')
            f.write(uj_kezdo + '\n')
            f.write(' '.join(uj_vegallapotok) + '\n')
            for honnan, betu, hova in rendezett:
                f.write(f"{honnan} {betu} {hova}\n")