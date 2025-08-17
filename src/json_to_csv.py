import os
import json
import csv

files = ['card_data.json', 'dl_al.json', 'dungeon_data.json', 'enemy_skill_data.json', 'limited_bonus_data.json', 'shop_items.json', 'skill_data.json']

cwd = os.getcwd()

def skill_filter(list):
    new_list = []
    for word in list:
        new_word = word
        if isinstance(word, str):
            if ';\n' in word:
                new_word = word.replace(';\n', '; ')
                pass
            else:
                new_word = word.replace('\n', ' ')
        new_list.append(new_word)
    return new_list

def main():
    for dirpath, subdirs, files in os.walk(cwd):
        files = [ file for file in files if file.endswith('.json') ]
        for file in files:
            full_path = os.path.join(dirpath, file)
            with open(full_path) as json_data:
                data = json.load(json_data)
                print(file)
                if file == 'card_data.json':
                    with open('csv/card_data.csv', 'w', newline='', encoding='utf8') as out:
                        writer = csv.writer(out)
                        writer.writerows(data['card'])
                if file == 'skill_data.json':
                    with open('csv/skill_data.csv', 'w', newline='', encoding='utf8') as out:
                        writer = csv.writer(out)
                        skills = data['skill']
                        for skill in skills:
                            skill = skill_filter(skill) 
                            writer.writerow(skill)
                if file == 'enemy_skill_data.json':
                    with open('csv/enemy_skill_data.csv', 'w', newline='', encoding='utf8') as out:
                        to_list = ''.join(data['enemy_skills'])
                        out.write(to_list)

if __name__ == "__main__":
    main()