# -*- coding: utf-8 -*
r"""
analyze函数需要传入一个参数，是json文件，但要转换成字符串。可以将sb3文件转换成analyze参数输入的字符串的函数式unzip。详见DEMO.py
"""

author = ['吃书的熊']
__version__ = '1.0.0'


def unzip(path: str):
    from os.path import isfile
    from zipfile import ZipFile

    if isfile(path):
        return open(ZipFile(path, 'r').extract('project.json'), 'r').read()
    else:
        raise Exception('这不是一个目录。')


def analyze(file):
    from json import loads
    d = loads(file)
    r = [str(len(d["targets"]))]
    sprite_name = []
    for i in d["targets"]:
        sprite_name.append(i["name"])
    r.append(sprite_name)  # 添加所有精灵的名称

    variable_name = []
    for i in range(len(d["targets"])):  # ["variables"].keys():
        for i2 in d["targets"][i]["variables"].keys():
            variable_name.append(d["targets"][i]["variables"][i2][0])

    r.append(variable_name)

    list_name = []
    for i in range(len(d["targets"])):  # ["variables"].keys():
            for i2 in d["targets"][i]["lists"].keys():
                list_name.append(d["targets"][i]["lists"][i2][0])
    r.append(list_name)

    costumes = 0
    sounds = 0
    for i in range(len(d["targets"])):  # ["variables"].keys():
        costumes += len(d["targets"][i]["costumes"])
        sounds += len(d["targets"][i]["sounds"])
    r.append(costumes)
    r.append(sounds)

    blocks = 0
    motion_block = 0
    looks_block = 0
    sound_block = 0
    event_block = 0
    control_block = 0
    sensing_block = 0
    data_block = 0
    operator_block = 0
    procedures_block = 0
    other_block = 0

    useful_blocks = 0
    for i in range(len(d["targets"])):
        for i1 in d["targets"][i]["blocks"]:
            try:
                if not 'menu' in d["targets"][i]["blocks"][i1]["opcode"]:
                    opcode = d["targets"][i]["blocks"][i1]["opcode"]
                    if 'motion' in opcode:
                        motion_block += 1
                    elif 'looks' in opcode:
                        looks_block += 1
                    elif 'sound' in opcode:
                        sound_block += 1
                    elif 'control' in opcode:
                        control_block += 1
                    elif 'sensing' in opcode:
                        sensing_block += 1
                    elif 'data' in opcode:
                        data_block += 1
                    elif 'operator' in opcode:
                        operator_block += 1
                    elif 'event' in opcode:
                        event_block += 1
                    elif opcode == 'procedures_call':
                        procedures_block += 1
                    elif opcode == 'procedures_definition':
                        procedures_block += 1
                        useful_blocks += 1
                    elif opcode == 'procedures_prototype' or 'argument' in opcode:
                        pass
                    else:
                        other_block += 1

                    if 'event' in opcode and 'when' in opcode and not d["targets"][i]["blocks"][i1]["parent"] is None and not 'boardcast' in opcode and bool(d["targets"][i]["blocks"][i1]["next"]) == True:
                        if 'control_start_as_clone' in d["targets"][i]["blocks"][d["targets"][i]["blocks"][i1]["parent"]]["opcode"]:
                            useful_blocks += 1
                    elif not d["targets"][i]["blocks"][i1]["parent"] is None:
                        if 'when' in d["targets"][i]["blocks"][d["targets"][i]["blocks"][i1]["parent"]]["opcode"]:
                            useful_blocks += 1


                blocks += 1
            except Exception:
                import traceback
                traceback.print_exc()
    r.append(blocks);r.append(useful_blocks);r.append(motion_block);r.append(looks_block);r.append(sound_block);r.append(event_block);r.append(control_block);r.append(sensing_block);r.append(operator_block);r.append(procedures_block);r.append(other_block)
    return r
