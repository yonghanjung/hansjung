from AI_fight.src.main.Strategy import Strategy
from AI_fight.src.main.BattleField import BattleField

__author__ = 'jeong-yonghan'
__package__ = 'AI_fight'

def main(myField=None):
    myField = BattleField(10,10)
    print myField.field()
    print myField.myship(3,'side',[2,2])


if __name__ == "__main__":
    main()