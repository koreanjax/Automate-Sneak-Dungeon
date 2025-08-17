# Basic information about the card from card_data
# Need to figure out the unknowns

class Card:
    card_info = [
        'id',
        'name',
        'attr_1',
        'attr_2',
        'ult_evo',
        'type_1',
        'type_2',
        'rarity',
        'cost',
        'unknown_1',
        'max_level',
        'fuse_exp',
        'official',
        'coin_value',
        'hp_init',
        'hp_max',
        'hp_growth',
        'atk_init',
        'atk_max',
        'atk_growth',
        'rcv_init',
        'rcv_max',
        'rcv_growth',
        'exp_max',
        'exp_growth',
        'active_skill',
        'leader_skill',
        'enemy_turns',
        'enemy_hp_1',
        'enemy_hp_10',
        'enemy_hp_growth',
        'enemy_atk_1',
        'enemy_atk_10',
        'enemy_atk_growth',
        'enemy_def_1',
        'enemy_def_10',
        'enemy_def_growth',
        'unknown_3',
        'enemy_coin',
        'enemy_rank_exp',
        'evolved_from',
        'evolve_mat_1',
        'evolve_mat_2',
        'evolve_mat_3',
        'evolve_mat_4',
        'evolve_mat_5',
        'devolve_mat_1',
        'devolve_mat_2',
        'devolve_mat_3',
        'devolve_mat_4',
        'devolve_mat_5',
        'unknown_51',
        'unknown_52',
        'unknown_53',
        'unknown_54',
        'unknown_55',
        'unknown_56',
        'enemy_skill_count',
        'awakening_count',
        'super_awakenings',
        'base_id',
        'group_id',
        'type_3',
        'monster_points',
        'latent_awakening_id',
        'collab_id',
        'bit_flags',
        'search_keywords',
        'limit_break_percent',
        'voice_id',
        'orb_bgm_id',
        'always_empty',
        'unknown_72',
        'unknown_73',
        'unknown_74',
        'unknown_75',
        'attr_3',
        'unknown_76'
    ]

    optional_card_info = [
        'enemy_skill_list',
        'awakenings',
        'sync_awakening',
        'sync_materials'
    ]

    def __init__(self, card_data):
        card_info_idx = 0
        optional_idx = 0
        enemy_skill_pad = 0
        awakening_pad = 0

        setattr(self, 'sync_awakening', 0)
        setattr(self, 'sync_mats', [])
        
        for idx, data in enumerate(card_data):
            skip_data = False
            if idx < 57:
                if 'growth' in self.card_info[card_info_idx]:
                    data = round(float(data) * 10)
                elif self.card_info[card_info_idx] != 'name':
                    try:
                        data = int(data)
                    except ValueError:
                        data = -1
                setattr(self, self.card_info[card_info_idx], data)
                card_info_idx+=1
            elif idx == 57:
                setattr(self, 'enemy_skill_count', int(data))
                setattr(self, self.optional_card_info[optional_idx], [])
                for i in range(1, int(getattr(self, 'enemy_skill_count', lambda: 0))+1):
                    param1 = int(card_data[idx+(i-1)*3+1])
                    param2 = int(card_data[idx+(i-1)*3+2])
                    param3 = int(card_data[idx+(i-1)*3+3])

                    enemy_skill = [param1, param2, param3]

                    getattr(self, 'enemy_skill_list', []).append(enemy_skill)
                enemy_skill_pad = getattr(self, 'enemy_skill_count', 0)*3
                card_info_idx+=1
                optional_idx+=1
            elif idx <= (58 + enemy_skill_pad) and idx > 57:
                if idx < 58 + enemy_skill_pad:
                    continue

                setattr(self, self.card_info[card_info_idx], int(data))
                setattr(self, self.optional_card_info[optional_idx], [0, 0, 0, 0, 0, 0, 0, 0, 0])

                for i in range(1, int(data)+1):
                    awakening = int(card_data[idx+i])
                    temp = getattr(self, self.optional_card_info[optional_idx], [])
                    temp[i-1] = awakening
                    setattr(self, self.optional_card_info[optional_idx], temp)
                awakening_pad = getattr(self, self.card_info[card_info_idx], 0)
                card_info_idx+=1
                optional_idx+=1
            elif idx <= (59 + enemy_skill_pad + awakening_pad) and idx > (58 + enemy_skill_pad):
                if idx < (59 + enemy_skill_pad + awakening_pad):
                    continue
                try:
                    setattr(self, self.card_info[card_info_idx], [int(i) for i in data.split(',')])
                except:
                    setattr(self, self.card_info[card_info_idx], [])
                card_info_idx+=1
            elif idx <= (77 + enemy_skill_pad + awakening_pad) and idx > (59 + enemy_skill_pad + awakening_pad):
                if self.card_info[card_info_idx] != 'search_keywords':
                    try:
                        data = int(data)
                    except ValueError:
                        data = -1
                setattr(self, self.card_info[card_info_idx], data)
                card_info_idx+=1
            elif idx == (78 + enemy_skill_pad + awakening_pad):
                try:
                    setattr(self, self.optional_card_info[optional_idx], int(data))
                    setattr(self, self.optional_card_info[optional_idx+1], [])
                    sync_material_count = int(card_data[idx+1])
                    temp_idx = idx+1
                    for i in range(0, sync_material_count):
                        mat_id = int(card_data[temp_idx+(i*3)+1])
                        mat_level = int(card_data[temp_idx+(i*3)+2])
                        mat_skill_level = int(card_data[temp_idx+(i*3)+3])
                        mat = [mat_id, mat_level, mat_skill_level]

                        getattr(self, self.optional_card_info[optional_idx+1], []).append(mat)
                    break
                except:
                    setattr(self, self.optional_card_info[optional_idx], 0)
                    setattr(self, self.optional_card_info[optional_idx+1], [])

        attr_1 = str(getattr(self, 'attr_1', 0))
        attr_2 = str(getattr(self, 'attr_2', 0))
        attr_3 = str(getattr(self, 'attr_3', 0))

        attrs = '|'.join([attr_1, attr_2, attr_3])
        setattr(self, 'attrs', attrs)

        type_1 = str(getattr(self, 'type_1', 0))
        type_2 = str(getattr(self, 'type_2', 0))
        type_3 = str(getattr(self, 'type_3', 0))

        types = '|'.join([type_1, type_2, type_3])
        setattr(self, 'types', types)

        hp_init = str(getattr(self, 'hp_init', 0))
        hp_max = str(getattr(self, 'hp_max', 0))
        hp_growth = str(getattr(self, 'hp_growth', 0))

        hpVals = '|'.join([hp_init, hp_max, hp_growth])
        setattr(self, 'hp_vals', hpVals)
        
        atk_init = str(getattr(self, 'atk_init', 0))
        atk_max = str(getattr(self, 'atk_max', 0))
        atk_growth = str(getattr(self, 'atk_growth', 0))

        atkVals = '|'.join([atk_init, atk_max, atk_growth])
        setattr(self, 'atk_vals', atkVals)
        
        rcv_init = str(getattr(self, 'rcv_init', 0))
        rcv_max = str(getattr(self, 'rcv_max', 0))
        rcv_growth = str(getattr(self, 'rcv_growth', 0))

        rcvVals = '|'.join([rcv_init, rcv_max, rcv_growth])
        setattr(self, 'rcv_vals', rcvVals)

        exp_max = str(getattr(self, 'exp_max', 0))
        exp_growth = str(getattr(self, 'exp_growth', 0))

        expVals = '|'.join([exp_max, exp_growth])
        setattr(self, 'exp_vals', expVals)

        e_mat_1 = str(getattr(self, 'evolve_mat_1', 0))
        e_mat_2 = str(getattr(self, 'evolve_mat_2', 0))
        e_mat_3 = str(getattr(self, 'evolve_mat_3', 0))
        e_mat_4 = str(getattr(self, 'evolve_mat_4', 0))
        e_mat_5 = str(getattr(self, 'evolve_mat_5', 0))
        
        evolve_mats = '|'.join([e_mat_1, e_mat_2, e_mat_3, e_mat_4, e_mat_5])
        setattr(self, 'evolve_mats', evolve_mats)

        de_mat_1 = str(getattr(self, 'devolve_mat_1', 0))
        de_mat_2 = str(getattr(self, 'devolve_mat_2', 0))
        de_mat_3 = str(getattr(self, 'devolve_mat_3', 0))
        de_mat_4 = str(getattr(self, 'devolve_mat_4', 0))
        de_mat_5 = str(getattr(self, 'devolve_mat_5', 0))
        
        devolve_mats = '|'.join([de_mat_1, de_mat_2, de_mat_3, de_mat_4, de_mat_5])
        setattr(self, 'devolve_mats', devolve_mats)

        awkns = []

        awakenings = getattr(self, 'awakenings', [])
        
        for awkn in awakenings:
            if awkn != 0:
                awkns.append(str(awkn))

        awkns_str = '|'.join(awkns)
        setattr(self, 'awakenings', awkns_str)

        s_awkns = []

        s_awakenings = getattr(self, 'super_awakenings', [])
        
        for awkn in s_awakenings:
            if awkn != 0:
                s_awkns.append(str(awkn))

        s_awkns_str = '|'.join(s_awkns)
        setattr(self, 'super_awakenings', s_awkns_str)

        sync_mats = []

        sync_materials = getattr(self, 'sync_materials', [])

        for material in sync_materials:
            mat_id = str(material[0])
            mat_level = str(material[1])
            mat_skill_level = str(material[2])

            mat_str = ','.join([mat_id, mat_level, mat_skill_level])
            sync_mats.append(mat_str)

        sync_mats_str = '|'.join(sync_mats)
        setattr(self, 'sync_mats', sync_mats_str)

        bit_flags = int(getattr(self, 'bit_flags', 0))
        bit_0 = 0
        bit_5 = 0
        bit_0 = bit_flags & 0b0000001
        bit_5 = bit_flags & 0b0100000

        setattr(self, 'assist', bit_0)
        setattr(self, 'expand', bit_5)

        adjusted_id = self.adjust_id(self.id)

        setattr(self, 'adjusted_id', adjusted_id)
    
    def adjust_id(self, id: int) -> int:
        if id >= 9900:
            return id - 100
        else:
            return id