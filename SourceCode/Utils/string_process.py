import re
import os
from Config.config import BASE_DIR
from Entities.ingredients import Ingredient


def pre_process(string, s_type=''):
    if not s_type:
        return ' '.join([s.strip() for s in string.split(' ') if s])
    if s_type == 'title':
        string = re.sub(r'[~`!@$#%&^*,.(){}\[\];"+\\/]', ' ', string)
        return ' '.join([s.strip() for s in string.split(' ') if s]).title()
    if s_type == 'search':
        string = re.sub(r'[~!@#$%^&*.(){}\[\]+\\/]', ' ', string)
        return [s.strip().lower() for s in string.split(',') if s.strip()]
    if s_type == 'comment':
        # filter dirty words in comments
        with open(os.path.join(BASE_DIR, 'DAO/data/dirt_words.txt'), 'r') as f:
            dirt_word = [line.strip() for line in f.readlines()]
        string = re.sub(r'[&*(){}\[\]+\\/]', ' ', string)
        return ' '.join([s for s in string.split(' ') if re.sub(r'[!?,.~@#$%]', '', s).strip().lower()
                         not in dirt_word])
    if s_type == 'describe':
        with open(os.path.join(BASE_DIR, 'DAO/data/dirt_words.txt'), 'r') as f:
            dirt_word = [line.strip() for line in f.readlines()]
        res_s = []
        for s in string.split('\n'):
            if re.sub(r'[!?,.~@#$%]', '', s).strip().lower() not in dirt_word:
                res_s.append(s)
        return '\n'.join(res_s)
    if s_type == 'ingredient':
        with open(os.path.join(BASE_DIR, 'DAO/data/ingredients_data.txt'), 'r') as f:
            ing_dict = [line.strip() for line in f.readlines()]
        string = string.strip().lower()
        temp_s = re.sub(r'[!?,.~@#$%\\\[\]{}<>]', '', string)
        return '' if temp_s not in ing_dict and temp_s not in [ing.name for ing in Ingredient.query.all()] else string
    return string


def get_num(string):
    return int(re.findall('[0-9]+', string)[0])


def cut_length(string, length):
    if len(string) <= length:
        return string
    for i in range(length, 0, -1):
        if string[i] == ' ':
            return string[:i] + ' ...'
    return string[:length] + ' ...'


if __name__ == '__main__':
    s1 = pre_process('egg,milk ,chicken-breast  ', 'search')
    s2 = cut_length("We've all found ourselves making French Onion Soup or another recipe that calls for caramelizing onions but what exactly does that mean? Caramelized onions are cooked low and slow until they are deeply golden and sweet. The onions will get jammy and become so addicting you'll be snacking right out of the pan. Here's a few things to always keep in my mind when perfectly caramelizing onions: Go low and slowIt might feel unnecessary to cook the onions at such a low temp for such a long time, but it's the only way to truly achieve caramelized onions. The point is to slowly draw out the natural sugar in onions which causes them to caramelize, not to simply brown the onions. Cooking the onions on a higher heat would cook off the moisture too quickly and the onions would burn before any true flavor could develop. Don't rush itEven if a recipe doesn't call for it, don't expect a shorter cook time than 40 minutes. Caramelizing onions takes time and will often take up to an hour to do properly. Don't try to rush it by turning up the heat because that simply won't work. It's important to work slowly. It will pay off. We promise. Don't walk awayUgh, not being able to walk away is never what we want to hear. Your onions won't burn if you take your eyes off of them, but you don't want to neglect them for too long. Stir them around every couple of minutes so they don't stick to the bottom of the pan. If a lot of fond (those sticky brown bits) starts forming on the bottom of the pan you can deglaze with a little bit of water so that nothing burns and you can keep on caramelizing.  ", 200)
    s3 = pre_process('this is a comment, we can see. wow! good!', 'comment')
    pass
