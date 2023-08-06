import pytest

import verbecc
import voseador

cj = verbecc.Conjugator(lang="es")
vs = voseador.Voseador()

# -er tests
def test_verbecc_comer():
    conj = cj.conjugate("comer")

    assert vs.add_vos_to_verbecc_conjugation(conj)["moods"] == {
            "indicativo": {
                "presente": [
                    "yo como",
                    "tú comes",
                    "vos comés",
                    "él come",
                    "nosotros comemos",
                    "vosotros coméis",
                    "ellos comen"
                ],
                "pretérito-imperfecto": [
                    "yo comía",
                    "tú comías",
                    "vos comías",
                    "él comía",
                    "nosotros comíamos",
                    "vosotros comíais",
                    "ellos comían"
                ],
                "pretérito-perfecto-simple": [
                    "yo comí",
                    "tú comiste",
                    "vos comiste",
                    "él comió",
                    "nosotros comimos",
                    "vosotros comisteis",
                    "ellos comieron"
                ],
                "futuro": [
                    "yo comeré",
                    "tú comerás",
                    "vos comerás",
                    "él comerá",
                    "nosotros comeremos",
                    "vosotros comeréis",
                    "ellos comerán"
                ],
                "pretérito-perfecto-compuesto": [
                    "yo he comido",
                    "tú has comido",
                    "vos has comido",
                    "él ha comido",
                    "nosotros hemos comido",
                    "vosotros habéis comido",
                    "ellos han comido"
                ],
                "pretérito-pluscuamperfecto": [
                    "yo había comido",
                    "tú habías comido",
                    "vos habías comido",
                    "él había comido",
                    "nosotros habíamos comido",
                    "vosotros habíais comido",
                    "ellos habían comido"
                ],
                "pretérito-anterior": [
                    "yo hube comido",
                    "tú hubiste comido",
                    "vos hubiste comido",
                    "él hubo comido",
                    "nosotros hubimos comido",
                    "vosotros hubisteis comido",
                    "ellos hubieron comido"
                ],
                "futuro-perfecto": [
                    "yo habré comido",
                    "tú habrás comido",
                    "vos habrás comido",
                    "él habrá comido",
                    "nosotros habremos comido",
                    "vosotros habréis comido",
                    "ellos habrán comido"
                ]
            },
            "subjuntivo": {
                "presente": [
                    "yo coma",
                    "tú comas",
                    "vos comás",
                    "él coma",
                    "nosotros comamos",
                    "vosotros comáis",
                    "ellos coman"
                ],
                "pretérito-imperfecto-1": [
                    "yo comiera",
                    "tú comieras",
                    "vos comieras",
                    "él comiera",
                    "nosotros comiéramos",
                    "vosotros comierais",
                    "ellos comieran"
                ],
                "pretérito-imperfecto-2": [
                    "yo comiese",
                    "tú comieses",
                    "vos comieses",
                    "él comiese",
                    "nosotros comiésemos",
                    "vosotros comieseis",
                    "ellos comiesen"
                ],
                "futuro": [
                    "yo comiere",
                    "tú comieres",
                    "vos comieres",
                    "él comiere",
                    "nosotros comiéremos",
                    "vosotros comiereis",
                    "ellos comieren"
                ],
                "pretérito-perfecto": [
                    "yo haya comido",
                    "tú hayas comido",
                    "vos hayás comido",
                    "él haya comido",
                    "nosotros hayamos comido",
                    "vosotros hayáis comido",
                    "ellos hayan comido"
                ],
                "pretérito-pluscuamperfecto-1": [
                    "yo hubiera comido",
                    "tú hubieras comido",
                    "vos hubieras comido",
                    "él hubiera comido",
                    "nosotros hubiéramos comido",
                    "vosotros hubierais comido",
                    "ellos hubieran comido"
                ],
                "pretérito-pluscuamperfecto-2": [
                    "yo hubiese comido",
                    "tú hubieses comido",
                    "vos hubieses comido",
                    "él hubiese comido",
                    "nosotros hubiésemos comido",
                    "vosotros hubieseis comido",
                    "ellos hubiesen comido"
                ],
                "futuro-perfecto": [
                    "yo hubiere comido",
                    "tú hubieres comido",
                    "vos hubieres comido",
                    "él hubiere comido",
                    "nosotros hubiéremos comido",
                    "vosotros hubiereis comido",
                    "ellos hubieren comido"
                ]
            },
            "imperativo": {
                "afirmativo": [
                    "come",
                    "comé",
                    "coma",
                    "comamos",
                    "comed",
                    "coman"
                ],
                "negativo": [
                    "no comas",
                    "no comás",
                    "no coma",
                    "no comamos",
                    "no comáis",
                    "no coman"
                ]
            },
            "condicional": {
                "presente": [
                    "yo comería",
                    "tú comerías",
                    "vos comerías",
                    "él comería",
                    "nosotros comeríamos",
                    "vosotros comeríais",
                    "ellos comerían"
                ],
                "perfecto": [
                    "yo habría comido",
                    "tú habrías comido",
                    "vos habrías comido",
                    "él habría comido",
                    "nosotros habríamos comido",
                    "vosotros habríais comido",
                    "ellos habrían comido"
                ]
            },
            "infinitivo": {
                "infinitivo": [
                    "comer",
                    "comido"
                ]
            },
            "gerundio": {
                "gerundio": [
                    "comiendo",
                    "comido"
                ]
            },
            "participo": {
                "participo": [
                    "comido"
                ]
            }
        }

# -ar tests
def test_verbecc_amar():
    conj = cj.conjugate("amar")

    assert vs.add_vos_to_verbecc_conjugation(conj)["moods"] == {
        "indicativo": {
            "presente": [
                "yo amo",
                "tú amas",
                "vos amás",
                "él ama",
                "nosotros amamos",
                "vosotros amáis",
                "ellos aman"
            ],
            "pretérito-imperfecto": [
                "yo amaba",
                "tú amabas",
                "vos amabas",
                "él amaba",
                "nosotros amábamos",
                "vosotros amabais",
                "ellos amaban"
            ],
            "pretérito-perfecto-simple": [
                "yo amé",
                "tú amaste",
                "vos amaste",
                "él amó",
                "nosotros amamos",
                "vosotros amasteis",
                "ellos amaron"
            ],
            "futuro": [
                "yo amaré",
                "tú amarás",
                "vos amarás",
                "él amará",
                "nosotros amaremos",
                "vosotros amaréis",
                "ellos amarán"
            ],
            "pretérito-perfecto-compuesto": [
                "yo he amado",
                "tú has amado",
                "vos has amado",
                "él ha amado",
                "nosotros hemos amado",
                "vosotros habéis amado",
                "ellos han amado"
            ],
            "pretérito-pluscuamperfecto": [
                "yo había amado",
                "tú habías amado",
                "vos habías amado",
                "él había amado",
                "nosotros habíamos amado",
                "vosotros habíais amado",
                "ellos habían amado"
            ],
            "pretérito-anterior": [
                "yo hube amado",
                "tú hubiste amado",
                "vos hubiste amado",
                "él hubo amado",
                "nosotros hubimos amado",
                "vosotros hubisteis amado",
                "ellos hubieron amado"
            ],
            "futuro-perfecto": [
                "yo habré amado",
                "tú habrás amado",
                "vos habrás amado",
                "él habrá amado",
                "nosotros habremos amado",
                "vosotros habréis amado",
                "ellos habrán amado"
            ]
        },
        "subjuntivo": {
            "presente": [
                "yo ame",
                "tú ames",
                "vos amés",
                "él ame",
                "nosotros amemos",
                "vosotros améis",
                "ellos amen"
            ],
            "pretérito-imperfecto-1": [
                "yo amara",
                "tú amaras",
                "vos amaras",
                "él amara",
                "nosotros amáramos",
                "vosotros amarais",
                "ellos amaran"
            ],
            "pretérito-imperfecto-2": [
                "yo amase",
                "tú amases",
                "vos amases",
                "él amase",
                "nosotros amásemos",
                "vosotros amaseis",
                "ellos amasen"
            ],
            "futuro": [
                "yo amare",
                "tú amares",
                "vos amares",
                "él amare",
                "nosotros amáremos",
                "vosotros amareis",
                "ellos amaren"
            ],
            "pretérito-perfecto": [
                "yo haya amado",
                "tú hayas amado",
                "vos hayás amado",
                "él haya amado",
                "nosotros hayamos amado",
                "vosotros hayáis amado",
                "ellos hayan amado"
            ],
            "pretérito-pluscuamperfecto-1": [
                "yo hubiera amado",
                "tú hubieras amado",
                "vos hubieras amado",
                "él hubiera amado",
                "nosotros hubiéramos amado",
                "vosotros hubierais amado",
                "ellos hubieran amado"
            ],
            "pretérito-pluscuamperfecto-2": [
                "yo hubiese amado",
                "tú hubieses amado",
                "vos hubieses amado",
                "él hubiese amado",
                "nosotros hubiésemos amado",
                "vosotros hubieseis amado",
                "ellos hubiesen amado"
            ],
            "futuro-perfecto": [
                "yo hubiere amado",
                "tú hubieres amado",
                "vos hubieres amado",
                "él hubiere amado",
                "nosotros hubiéremos amado",
                "vosotros hubiereis amado",
                "ellos hubieren amado"
            ]
        },
        "imperativo": {
            "afirmativo": [
                "ama",
                "amá",
                "ame",
                "amemos",
                "amad",
                "amen"
            ],
            "negativo": [
                "no ames",
                "no amés",
                "no ame",
                "no amemos",
                "no améis",
                "no amen"
            ]
        },
        "condicional": {
            "presente": [
                "yo amaría",
                "tú amarías",
                "vos amarías",
                "él amaría",
                "nosotros amaríamos",
                "vosotros amaríais",
                "ellos amarían"
            ],
            "perfecto": [
                "yo habría amado",
                "tú habrías amado",
                "vos habrías amado",
                "él habría amado",
                "nosotros habríamos amado",
                "vosotros habríais amado",
                "ellos habrían amado"
            ]
        },
        "infinitivo": {
            "infinitivo": [
                "amar",
                "amado"
            ]
        },
        "gerundio": {
            "gerundio": [
                "amando",
                "amado"
            ]
        },
        "participo": {
            "participo": [
                "amado"
            ]
        }
    }

# -ir tests
def test_verbecc_morir():
    conj = cj.conjugate("morir")
    assert vs.add_vos_to_verbecc_conjugation(conj)["moods"] == {
            "indicativo": {
                "presente": [
                    "yo muero",
                    "tú mueres",
                    "vos morís",
                    "él muere",
                    "nosotros morimos",
                    "vosotros morís",
                    "ellos mueren"
                ],
                "pretérito-imperfecto": [
                    "yo moría",
                    "tú morías",
                    "vos morías",
                    "él moría",
                    "nosotros moríamos",
                    "vosotros moríais",
                    "ellos morían"
                ],
                "pretérito-perfecto-simple": [
                    "yo morí",
                    "tú moriste",
                    "vos moriste",
                    "él murió",
                    "nosotros morimos",
                    "vosotros moristeis",
                    "ellos murieron"
                ],
                "futuro": [
                    "yo moriré",
                    "tú morirás",
                    "vos morirás",
                    "él morirá",
                    "nosotros moriremos",
                    "vosotros moriréis",
                    "ellos morirán"
                ],
                "pretérito-perfecto-compuesto": [
                    "yo he muerto",
                    "tú has muerto",
                    "vos has muerto",
                    "él ha muerto",
                    "nosotros hemos muerto",
                    "vosotros habéis muerto",
                    "ellos han muerto"
                ],
                "pretérito-pluscuamperfecto": [
                    "yo había muerto",
                    "tú habías muerto",
                    "vos habías muerto",
                    "él había muerto",
                    "nosotros habíamos muerto",
                    "vosotros habíais muerto",
                    "ellos habían muerto"
                ],
                "pretérito-anterior": [
                    "yo hube muerto",
                    "tú hubiste muerto",
                    "vos hubiste muerto",
                    "él hubo muerto",
                    "nosotros hubimos muerto",
                    "vosotros hubisteis muerto",
                    "ellos hubieron muerto"
                ],
                "futuro-perfecto": [
                    "yo habré muerto",
                    "tú habrás muerto",
                    "vos habrás muerto",
                    "él habrá muerto",
                    "nosotros habremos muerto",
                    "vosotros habréis muerto",
                    "ellos habrán muerto"
                ]
            },
            "subjuntivo": {
                "presente": [
                    "yo muera",
                    "tú mueras",
                    "vos murás",
                    "él muera",
                    "nosotros muramos",
                    "vosotros muráis",
                    "ellos mueran"
                ],
                "pretérito-imperfecto-1": [
                    "yo muriera",
                    "tú murieras",
                    "vos murieras",
                    "él muriera",
                    "nosotros muriéramos",
                    "vosotros murierais",
                    "ellos murieran"
                ],
                "pretérito-imperfecto-2": [
                    "yo muriese",
                    "tú murieses",
                    "vos murieses",
                    "él muriese",
                    "nosotros muriésemos",
                    "vosotros murieseis",
                    "ellos muriesen"
                ],
                "futuro": [
                    "yo muriere",
                    "tú murieres",
                    "vos murieres",
                    "él muriere",
                    "nosotros muriéremos",
                    "vosotros muriereis",
                    "ellos murieren"
                ],
                "pretérito-perfecto": [
                    "yo haya muerto",
                    "tú hayas muerto",
                    "vos hayás muerto",
                    "él haya muerto",
                    "nosotros hayamos muerto",
                    "vosotros hayáis muerto",
                    "ellos hayan muerto"
                ],
                "pretérito-pluscuamperfecto-1": [
                    "yo hubiera muerto",
                    "tú hubieras muerto",
                    "vos hubieras muerto",
                    "él hubiera muerto",
                    "nosotros hubiéramos muerto",
                    "vosotros hubierais muerto",
                    "ellos hubieran muerto"
                ],
                "pretérito-pluscuamperfecto-2": [
                    "yo hubiese muerto",
                    "tú hubieses muerto",
                    "vos hubieses muerto",
                    "él hubiese muerto",
                    "nosotros hubiésemos muerto",
                    "vosotros hubieseis muerto",
                    "ellos hubiesen muerto"
                ],
                "futuro-perfecto": [
                    "yo hubiere muerto",
                    "tú hubieres muerto",
                    "vos hubieres muerto",
                    "él hubiere muerto",
                    "nosotros hubiéremos muerto",
                    "vosotros hubiereis muerto",
                    "ellos hubieren muerto"
                ]
            },
            "imperativo": {
                "afirmativo": [
                    "muere",
                    "morí",
                    "muera",
                    "muramos",
                    "morid",
                    "mueran"
                ],
                "negativo": [
                    "no mueras",
                    "no murás",
                    "no muera",
                    "no muramos",
                    "no muráis",
                    "no mueran"
                ]
            },
            "condicional": {
                "presente": [
                    "yo moriría",
                    "tú morirías",
                    "vos morirías",
                    "él moriría",
                    "nosotros moriríamos",
                    "vosotros moriríais",
                    "ellos morirían"
                ],
                "perfecto": [
                    "yo habría muerto",
                    "tú habrías muerto",
                    "vos habrías muerto",
                    "él habría muerto",
                    "nosotros habríamos muerto",
                    "vosotros habríais muerto",
                    "ellos habrían muerto"
                ]
            },
            "infinitivo": {
                "infinitivo": [
                    "morir",
                    "muerto"
                ]
            },
            "gerundio": {
                "gerundio": [
                    "muriendo",
                    "muerto"
                ]
            },
            "participo": {
                "participo": [
                    "muerto"
                ]
            }
        }