from logic import *

"""
[문제 01]: 각각 주어진 sentence를 Propositional logic으로 변경한 것을 return 하시오.(10점)
HINT: sentences.py 내의 rainWet()을 참고할 것.
"""


## Sentence 01: "If it's summer and we're in California, then it doesn't rain."
def logic01_01():
    # Predicates to use:
    Summer = Atom('Summer')  # whether it's summer
    California = Atom('California')  # whether we're in California
    Rain = Atom('Rain')  # whether it's raining
    ################# Write Your Code Here #########################
    return Implies(And(Summer, California), Not(Rain))
    ################################################################


## Sentence 02: "It's wet if and only if it is raining or the sprinklers are on."
def logic01_02():
    # Predicates to use:
    Rain = Atom('Rain')  # whether it is raining
    Wet = Atom('Wet')  # whether it it wet
    Sprinklers = Atom('Sprinklers')  # whether the sprinklers are on
    ################# Write Your Code Here #########################
    return Equiv(Wet, Or(Rain, Sprinklers))
    ################################################################


## Sentence 03: "Either it's day or night (but not both)."
def logic01_03():
    # Predicates to use:
    Day = Atom('Day')  # whether it's day
    Night = Atom('Night')  # whether it's night
    ################# Write Your Code Here #########################
    return Xor(Day, Night)
    ################################################################


"""
[문제 02]: 각각 주어진 sentence를 First-order logic으로 변경한 것을 return 하시오.(15점)
02-01 HINT: Mother를 "person"이라고 강요할 필요는 없다. 
02-02 HINT: Child를 "person"이라고 강요할 필요는 없다.
02-03 HINT: sentences.py 내의 parentChild()을 참고할 것
02-04 HINT: It is ok for a person to be her own parent.
"""


## Sentence 01: "Every person has a mother."
def logic02_01():
    # Predicates to use:
    def Person(x): return Atom('Person', x)  # whether x is a person

    def Mother(x, y): return Atom('Mother', x, y)  # whether x's mother is y

    ################# Write Your Code Here #########################
    return Forall('$person', Exists('$mother', Implies(Person('$person'), Mother('$person', '$mother'))))
    ################################################################


## Sentence 02: "At least one person has no children."
def logic02_02():
    # Predicates to use:
    def Person(x): return Atom('Person', x)  # whether x is a person

    def Child(x, y): return Atom('Child', x, y)  # whether x has a child y

    ################# Write Your Code Here #########################
    return Exists("$person", And(Person("$person"), Not(Exists("$child", Child("$person", "$child")))))
    ################################################################


## Return a formula which defines Daughter in terms of Female and Child.
def logic02_03():
    # Predicates to use:
    def Female(x): return Atom('Female', x)  # whether x is female

    def Child(x, y): return Atom('Child', x, y)  # whether x has a child y

    def Daughter(x, y): return Atom('Daughter', x, y)  # whether x has a daughter y

    ################# Write Your Code Here #########################
    def FemaleChild(x, y): return And(Female(y), Child(x, y))

    return Forall('$person', Forall('$child', Equiv(FemaleChild('$person', '$child'), Daughter('$person', '$child'))))
    ################################################################


## Return a formula which defines Grandmother in terms of Female and Parent.
def logic02_04():
    # Predicates to use:
    def Female(x): return Atom('Female', x)  # whether x is female

    def Parent(x, y): return Atom('Parent', x, y)  # whether x has a parent y

    def Grandmother(x, y): return Atom('Grandmother', x, y)  # whether x has a grandmother y

    ################# Write Your Code Here #########################
    return Forall('$child',
                  Forall('$grand',
                         Equiv(Grandmother('$child', '$grand'),
                               And(Female('$grand'),
                                   Exists('$par', And(Parent('$child', '$par'), Parent('$par', '$grand'))))
                               )
                         )
                  )
    ################################################################


"""
[문제 03]: 문제 설명 파일에서 설명한 4개의 증언과 2개의 사실을 First-Order Logic으로 변경하여,차례대로 formula 리스트에 추가하시오.(25점)
HINT01: logic.py에서 정의된 Equals predicate를 사용할 수 있다. 참고로 Equals predicate는 두 개의 object가 같다고 주장할때 사용된다.
"""


def suspect():
    def TellTruth(x): return Atom('TellTruth', x)

    def CrashedServer(x): return Atom('CrashedServer', x)

    john = Constant('john')
    susan = Constant('susan')
    nicole = Constant('nicole')
    mark = Constant('mark')
    formulas = []
    ## HINT02: 첫번째 증언 구현 예시 John: "it wasn't me!"
    formulas.append(Equiv(TellTruth(john), Not(CrashedServer(john))))
    """
    증언 (1)을 제외한 (2),(3),(4),(5),(6)을 구현하시오.
    """
    ################# Write Your Code Here #########################
    # Susan : "It was Nicole!"
    formulas.append(Equiv(TellTruth(susan), CrashedServer(nicole)))

    # Mark : "No, it was Susan!"
    formulas.append(Equiv(TellTruth(mark), CrashedServer(susan)))

    # Nicole : "Susan's a liar."
    formulas.append(Equiv(TellTruth(nicole), Not(TellTruth(susan))))

    # Exactly one person is telling the truth.
    formulas.append(Exists('$y', Forall('$x', Equiv(TellTruth('$x'), Equals('$x', '$y')))))

    # Exactly one person is crashed the server.
    formulas.append(Exists('$y', Forall('$x', Equiv(CrashedServer('$x'), Equals('$x', '$y')))))

    ################################################################
    # Query: Who did it?
    query = CrashedServer('$x')
    return (formulas, query)


"""
[문제 04]: 문제 설명 파일에서 설명한 6개의 theorem을 First-Order Logic으로 변경하여,차례대로 formula 리스트에 추가하시오.(30점)
HINT01: logic.py에서 정의된 Equals predicate를 사용할 수 있다. 참고로 Equals predicate는 두 개의 object가 같다고 주장할때 사용된다.
HINT02: 모든 object는 숫자이므로 숫자를 predicate로 정의할 필요가 없다. 
"""


def number_theorem():
    def Even(x): return Atom('Even', x)  # whether x is even

    def Odd(x): return Atom('Odd', x)  # whether x is odd

    def Successor(x, y): return Atom('Successor', x, y)  # whether x's successor is y

    def Larger(x, y): return Atom('Larger', x, y)  # whether x is larger than y

    formulas = []
    query = None
    ################# Write Your Code Here #########################
    # (1) 각각의 숫자 x에는 하나의 successor가 있으며, 이는 x와 같지 않다.
    formulas.append(Forall('$x', Exists('$y', And(Forall('$z', Equiv(Successor('$x', '$z'), Equals('$z', '$y'))), Not(Equals('$x', '$y'))))))

    # (2) 각각의 숫자는 홀수 혹은 짝수이며, 둘 다인 경우는 없다.
    formulas.append(Forall('$x', And(Or(Even('$x'), Odd('$x')), Not(And(Even('$x'), Odd('$x'))))))

    # (3) 짝수의 successor는 홀수이다.
    formulas.append(Forall('$x', Forall('$y', Implies(And(Even('$x'), Successor('$x', '$y')), Odd('$y')))))

    # (4) 홀수의 successor는 짝수이다.
    formulas.append(Forall('$x', Forall('$y', Implies(And(Odd('$x'), Successor('$x', '$y')), Even('$y')))))

    # (5) 모든 숫자 x에 대해서, x의 successor는 x보다 크다.
    formulas.append(Forall('$x', Forall('$y', Implies(Successor('$x', '$y'), Larger('$y', '$x')))))

    # (6) x가 y보다 크고, y가 z보다 크면, x는 z보다 크다.
    formulas.append(Forall('$x', Forall('$y', Forall('$z', Implies(And(Larger('$x', '$y'), Larger('$y', '$z')), Larger('$x', '$z'))))))

    ################################################################
    # Query: For each number, there exists an even number larger than it.
    query = Forall('$x', Exists('$y', And(Even('$y'), Larger('$y', '$x'))))
    return (formulas, query)
