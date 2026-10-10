from gilded_rose import *

test_cases = {
    'обычный товар: качество -1, sell_in -1': (
        Item('+5 Dexterity Vest', 10, 20),
        Item('+5 Dexterity Vest', 9, 19),
    ),

    'обычный товар: качество не уходит ниже 0': (
        Item('+5 Dexterity Vest', 10, 0),
        Item('+5 Dexterity Vest', 9, 0),
    ),

    'обычный товар: срок истёк, качество -2': (
        Item('+5 Dexterity Vest', 0, 10),
        Item('+5 Dexterity Vest', -1, 8),
    ),

    'обычный товар: срок истёк, качество не ниже 0': (
        Item('+5 Dexterity Vest', 0, 1),
        Item('+5 Dexterity Vest', -1, 0),
    ),

    'Aged Brie: качество +1': (
        Item('Aged Brie', 2, 0),
        Item('Aged Brie', 1, 1),
    ),

    'Aged Brie: качество не выше 50': (
        Item('Aged Brie', 2, 50),
        Item('Aged Brie', 1, 50),
    ),

    'Aged Brie: срок истёк, качество +2': (
        Item('Aged Brie', 0, 10),
        Item('Aged Brie', -1, 12),
    ),

    'Aged Brie: срок истёк, качество не выше 50': (
        Item('Aged Brie', 0, 49),
        Item('Aged Brie', -1, 50),
    ),

    'Sulfuras: ничего не меняется': (
        Item('Sulfuras, Hand of Ragnaros', 0, 80),
        Item('Sulfuras, Hand of Ragnaros', 0, 80),
    ),

    'Backstage passes: >10 дней, качество +1': (
        Item('Backstage passes to a TAFKAL80ETC concert', 15, 20),
        Item('Backstage passes to a TAFKAL80ETC concert', 14, 21),
    ),

    'Backstage passes: <=10 дней, качество +2': (
        Item('Backstage passes to a TAFKAL80ETC concert', 10, 20),
        Item('Backstage passes to a TAFKAL80ETC concert', 9, 22),
    ),

    'Backstage passes: <=5 дней, качество +3': (
        Item('Backstage passes to a TAFKAL80ETC concert', 5, 20),
        Item('Backstage passes to a TAFKAL80ETC concert', 4, 23),
    ),

    'Backstage passes: после концерта, качество 0': (
        Item('Backstage passes to a TAFKAL80ETC concert', 0, 20),
        Item('Backstage passes to a TAFKAL80ETC concert', -1, 0),
    ),

    'Backstage passes: качество не выше 50': (
        Item('Backstage passes to a TAFKAL80ETC concert', 5, 49),
        Item('Backstage passes to a TAFKAL80ETC concert', 4, 50),
    ),

    'Conjured: качество -2': (
        Item('Conjured Mana Cake', 10, 20),
        Item('Conjured Mana Cake', 9, 18),
    ),

    'Conjured: качество не ниже 0': (
        Item('Conjured Mana Cake', 10, 1),
        Item('Conjured Mana Cake', 9, 0),
    ),

    'Conjured: срок истёк, качество -4': (
        Item('Conjured Mana Cake', 0, 10),
        Item('Conjured Mana Cake', -1, 6),
    ),
}

def compare_items(item1: Item, item2: Item) -> bool:
    return (
        item1.quality == item2.quality
        and item1.sell_in == item2.sell_in
        and item1.name == item2.name
    )

for test_name, (item, expected) in test_cases.items():
        GildedRose([item]).update_quality()
        status = 'PASSED' if compare_items(item, expected) else 'FAILED'
        print(f'[{test_name}]: {status}')
        if status == 'FAILED':
            print(f'Ожидалось: {expected}')
            print(f'Получено: {item}')
        print('-' * 20)