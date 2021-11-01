from pathlib import Path

playerdata_path = Path('mymodules', 'playerdata.txt')
leaderboard_path = Path('leaderboard.txt')


def getdata():
    """
    Получает данные об игроках и их лучших результатах из файла playerdata
    :return:
    backup_count: количество сделанных сохранений файла playerdata
    current: имя текущего игрока
    top_count: количество призовых мест, отображающихся в таблице
    topnames: список имён игроков, имеющих лучшие результаты
    records: список лучших результатов игроков
    score_count: количество лучших результатов для каждого игрока, хранящееся в памяти
    player_count: общее количество игроков, чьи лучшие результаты записаны в файл
    regularnames: список имён всех игроков, чьи лучшие результаты записаны в файл
    scores: список из списков лучших результатов для каждого игрока
    """
    regularnames = []
    scores = []
    topnames = []
    records = []
    with open(playerdata_path, 'r') as file:
        backup_count = int(file.readline())
        current = file.readline().rstrip()
        top_count = int(file.readline())
        for i in range(0, top_count, 1):
            name = file.readline().rstrip()
            record = float(file.readline())
            if int(record) == record:
                record = int(record)
            topnames.append(name)
            records.append(record)
        score_count = int(file.readline())
        player_count = int(file.readline())
        for i in range(0, player_count, 1):
            name = file.readline().rstrip()
            regularnames.append(name)
            scores.append([])
            for j in range(0, score_count, 1):
                score = float(file.readline())
                if int(score) == score:
                    score = int(score)
                scores[i].append(score)
    return backup_count, current, top_count, topnames, records, score_count, player_count, regularnames, scores


def шаблон():  # вспомогательный шаблон написания функции, сама функция не вызывается
    (backup_count, current, top_count, topnames, records, score_count, player_count, regularnames, scores) = getdata()
    with open(playerdata_path, 'w') as file:
        print(backup_count, file=file)
        print(current, file=file)
        print(top_count, file=file)
        for i in range(0, top_count, 1):
            print(topnames[i], file=file)
            print(records[i], file=file)
        print(score_count, file=file)
        print(player_count, file=file)
        for i in range(0, player_count, 1):
            print(regularnames[i], file=file)
            for j in range(0, score_count, 1):
                print(scores[i][j], file=file)


def new(new_name, new_score):
    """
    Фиксирует набранные игроком очки в фале playerdata,
    сравнивает количество очков с лучшими и добавляет его в списки лучших результатов в случае необходимости
    :param new_name: имя игрока
    :param new_score: набранные очки
    """
    (backup_count, current, top_count, topnames, records, score_count, player_count, regularnames, scores) = getdata()
    is_new = True
    for i in range(0, player_count, 1):
        if new_name == regularnames[i]:
            is_new = False
            new_scores = scores[i]
            new_scores.append(new_score)
            new_scores.sort(reverse=True)
            if new_scores[-1] < new_score:
                new_scores.pop()
                scores[i] = new_scores
            is_recordholder = False
            for j in range(0, top_count, 1):
                if topnames[j] == new_name:
                    is_recordholder = True
                    if records[j] < new_score:
                        for k in range(0, top_count, 1):
                            if records[k] < new_score:
                                for h in range(j, k, -1):
                                    topnames[h] = topnames[h - 1]
                                topnames[k] = new_name
                                break
                        records[j] = new_score
                        records.sort(reverse=True)
                        break
            if not is_recordholder:
                for j in range(0, top_count, 1):
                    if new_score > records[j]:
                        records.append(new_score)
                        records.sort(reverse=True)
                        records.pop()
                        for k in range(len(topnames) - 1, j, -1):
                            topnames[k] = topnames[k - 1]
                        topnames[j] = new_name
                        break
            break
    if is_new:
        player_count += 1
        regularnames.append(new_name)
        scores.append([])
        if score_count >= 1:
            scores[-1].append(new_score)
        if score_count > 1:
            for j in range(1, score_count, 1):
                scores[-1].append(0)
        for j in range(0, top_count, 1):
            if new_score > records[j]:
                records.append(new_score)
                records.sort(reverse=True)
                records.pop()
                for k in range(len(topnames) - 1, j, -1):
                    topnames[k] = topnames[k - 1]
                topnames[j] = new_name
                break
    current = new_name
    with open(playerdata_path, 'w') as file:
        print(backup_count, file=file)
        print(current, file=file)
        print(top_count, file=file)
        for i in range(0, top_count, 1):
            print(topnames[i], file=file)
            print(records[i], file=file)
        print(score_count, file=file)
        print(player_count, file=file)
        for i in range(0, player_count, 1):
            print(regularnames[i], file=file)
            for j in range(0, score_count, 1):
                print(scores[i][j], file=file)


def renew(top_count, score_count):
    """
    Обновляет файл leaderboard.txt с таблицей лучших результатов
    :param top_count: количество призовых мест, отображающееся в таблице лучших результатов
    :param score_count: количество лучших результатов, отображающееся в таблице личных рекордов
    """
    (backup_count, current, topcount, topnames, records, scorecount, player_count, regularnames, scores) = getdata()
    top_count = min(topcount, top_count)
    score_count = min(scorecount, score_count)
    with open(leaderboard_path, 'w') as file:
        print('Топ лучших игроков:', '\n', file=file, sep='')
        for i in range(0, top_count, 1):
            if records[i] > 0:
                print(i + 1, ': ', topnames[i], ' - ', records[i], ' очков', '\n', file=file, sep='')
        print('\n', file=file, end='')
        print('Личные рекорды:', '\n', file=file, sep='', end='')
        for i in range(0, player_count, 1):
            print('\n', regularnames[i], ':', file=file, sep='')
            for j in range(0, score_count, 1):
                if scores[i][j] > 0:
                    print(j + 1, ': ', scores[i][j], file=file, sep='')


def reset_leaders(top_count, score_count, def_top_count, def_score_count):
    """
    Сбрасывает таблицы лучших результатов, добавляет резервную копию таблицы в папку backups
    :param top_count: новое количество призовых мест, отображающееся в таблице лучших результатов
    :param score_count: новое количество лучших результатов, отображающееся в таблице личных рекордов
    :param def_top_count: новое количество лучших результатов, хранимое в памяти
    :param def_score_count: новое количество личных рекордов, хранимое в памяти
    """
    (backup_count, current, topCount, topnames, records, scoreCount, player_count, regularnames, scores) = getdata()
    topcount = min(topCount, top_count)
    scorecount = min(scoreCount, score_count)
    top_count = max(def_top_count, top_count)
    score_count = max(def_score_count, score_count)
    if records[0] != 0:
        backup_count += 1
        namestr = 'leaderboar_backup_' + str(backup_count) + '.txt'
        with open(Path('backups', namestr), 'w') as file:
            print('Топ лучших игроков:', '\n', file=file, sep='')
            for i in range(0, topcount, 1):
                if records[i] > 0:
                    print(i + 1, ': ', topnames[i], ' - ', records[i], ' очков', '\n', file=file, sep='')
            print('\n', file=file, end='')
            print('Личные рекорды:', '\n', file=file, sep='', end='')
            for i in range(0, player_count, 1):
                print('\n', regularnames[i], ':', file=file, sep='')
                for j in range(0, scorecount, 1):
                    if scores[i][j] > 0:
                        print(j + 1, ': ', scores[i][j], file=file, sep='')
    with open(playerdata_path, 'w') as file:
        print(backup_count, file=file)
        print(current, file=file)
        print(top_count, file=file)
        for i in range(0, top_count, 1):
            print('\\empty', file=file)
            print(0, file=file)
        print(score_count, file=file)
        print(0, file=file)
