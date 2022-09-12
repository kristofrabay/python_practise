def get_2022_data():
    
    from bs4 import BeautifulSoup
    import requests
    from functools import reduce

    import pandas as pd
    import numpy as np

    import warnings
    warnings.filterwarnings('ignore')
    
    seasons = [2022]

    data_type = {'offense' : ['total', 'passing', 'rushing', 'receiving', 'downs'],
                 'defense' : ['total', 'passing', 'rushing', 'receiving', 'downs'],
                 'special' : ['kicking', 'punting', 'returning']}
    
    # collect data
    
    tables = []

    for season in seasons:

        for game_type in data_type.keys():        
            possible_play_types = data_type[game_type]

            for play_type in possible_play_types:

                url = 'https://www.espn.com/nfl/stats/team/_/view/' + game_type + '/stat/' + play_type + '/season/' + str(season) + '/seasontype/2'
                page = requests.get(url)
                soup = BeautifulSoup(page.text)

                table_div = soup.find('div', class_='ResponsiveTable ResponsiveTable--fixed-left mt4 Table2__title--remove-capitalization')

                teams = table_div.find('table', class_ = 'Table Table--align-right Table--fixed Table--fixed-left')
                teams = pd.read_html(teams.prettify(), flavor = 'bs4')[0]

                if len(teams) == 31:
                    teams.loc[-1] = teams.columns
                    teams.index = teams.index + 1  
                    teams.sort_index(inplace=True) 
                    teams.columns = ['Teams']

                data = table_div.find('table', class_ = 'Table Table--align-right')
                data = pd.read_html(data.prettify(), flavor = 'bs4')[0]

                #print(link)

                if 'downs' in url:   
                    data.columns = data.columns.map('_'.join).tolist()

                if 'kicking' in url: 
                    data.columns = data.columns.map('_'.join).tolist()

                if 'returning' in url: 
                    data.columns = data.columns.map('_'.join).tolist()

                if 'total' in url: 
                    data.columns = data.columns.map('_'.join).tolist()


                data.columns = [str(game_type) + '_' + str(play_type) + '_' + i for i in data.columns]

                table = pd.concat([teams, data], 1)
                table['season'] = season
                tables.append(table)
                
                
    for table in tables:
        if table.columns[0] != 'Team':
            table.rename(columns = {table.columns[0]: 'Team'} , inplace = True)
            
            
    # merge
    data = reduce(lambda  a,b: pd.merge(a,b,on = ['Team', 'season'], how='outer'),tables)
    
    # clean up
    data.rename(columns = {'offense_downs_Unnamed: 0_level_0_GP' : 'games_played',
                       'offense_total_Points_PTS/G' : 'offense_points_per_game',
                       'defense_total_Points_PTS/G' : 'defense_points_per_game',
                       'special_punting_AVG.1' : 'special_punting_avg_return_yds'}, inplace = True)
    drop_totals = data.filter(like = 'total').columns
    data.drop(drop_totals, 1, inplace = True)

    drop_gp_cols = data.filter(like = 'GP').columns

    drop_field_goal_range_data = [ 'special_kicking_Field Goals_1-19',
                                   'special_kicking_Field Goals_20-29',
                                   'special_kicking_Field Goals_30-39',
                                   'special_kicking_Field Goals_40-49',
                                   'special_kicking_Field Goals_50+']

    drop_totals = ['offense_passing_YDS', 'defense_passing_YDS',
                   'offense_passing_CMP', 'defense_passing_CMP', 
                   'offense_receiving_YDS', 'defense_receiving_YDS', 
                   'offense_rushing_YDS', 'defense_rushing_YDS',
                   'special_kicking_Extra Points_XPM', 'special_kicking_Extra Points_XPA',
                   'special_kicking_Field Goals_FGM', 'special_punting_YDS',
                   'special_punting_TB', 'special_punting_FC', 'special_punting_BP',
                   'special_punting_RET', 'special_punting_RETY',
                   'special_returning_Kickoffs_YDS', 'special_returning_Kickoffs_TD',
                   'offense_downs_First Downs_PASS', 'defense_downs_First Downs_PASS', 'special_returning_Punts_ATT',
                   'offense_receiving_TD', 'defense_receiving_TD', 'special_returning_Punts_TD',
                   'special_returning_Punts_YDS', 'special_returning_Punts_FC']

    drop_longest_data = data.filter(like = 'LNG').columns.tolist()

    drop_game_avgs = ['offense_receiving_YDS/G', 'defense_receiving_YDS/G']

    data.drop(drop_gp_cols, 1, inplace = True)
    data.drop(drop_field_goal_range_data, 1, inplace = True)
    data.drop(drop_totals, 1, inplace = True)
    data.drop(drop_longest_data, 1, inplace = True)
    data.drop(drop_game_avgs, 1, inplace = True)

    data['punting_punts_per_game'] = data['special_punting_PUNTS'] / data['games_played']
    data['punting_punts_i20_ratio'] = data['special_punting_IN20'] / data['special_punting_PUNTS']

    data['special_kicking_FGA_per_game'] = data['special_kicking_Field Goals_FGA'] / data['games_played']
    data['special_returning_Kickoffs_att_per_game'] = data['special_returning_Kickoffs_ATT'] / data['games_played']

    data['offense_passing_SACK_per_game'] = data['offense_passing_SACK'] / data['games_played']
    data['defense_passing_SACK_per_game'] = data['defense_passing_SACK'] / data['games_played']

    data['offense_downs_Penalties_TOTAL_per_game'] = data['offense_downs_Penalties_TOTAL'] / data['games_played']
    data['offense_downs_Penalties_YDS_per_game'] = data['offense_downs_Penalties_YDS'] / data['games_played']
    data['defense_downs_Penalties_TOTAL_per_game'] = data['defense_downs_Penalties_TOTAL'] / data['games_played']
    data['defense_downs_Penalties_YDS_per_game'] = data['defense_downs_Penalties_YDS'] / data['games_played']
    data['offense_passing_SYL_per_game'] = data['offense_passing_SYL'] / data['games_played']
    data['defense_passing_SYL_per_game'] = data['defense_passing_SYL'] / data['games_played']

    data['offense_downs_Third Downs_ATT_per_game'] = data['offense_downs_Third Downs_ATT'] / data['games_played']
    data['offense_downs_Fourth Downs_ATT_per_game'] = data['offense_downs_Fourth Downs_ATT'] / data['games_played']
    data['defense_downs_Third Downs_ATT_per_game'] = data['defense_downs_Third Downs_ATT'] / data['games_played']
    data['defense_downs_Fourth Downs_ATT_per_game'] = data['defense_downs_Fourth Downs_ATT'] / data['games_played']

    # data['offense_passing_ATT_per_game'] = data['offense_passing_ATT'] / data['games_played']
    # data['offense_rushing_ATT_per_game'] = data['offense_rushing_ATT'] / data['games_played']
    # data['defense_passing_ATT_per_game'] = data['defense_passing_ATT'] / data['games_played']
    # data['defense_rushing_ATT_per_game'] = data['defense_rushing_ATT'] / data['games_played']
    # pass to rush ratio is better

    data['offense_pass_to_rush_ratio'] = data['offense_passing_ATT'] / data['offense_rushing_ATT']
    data['defense_pass_to_rush_ratio'] = data['defense_passing_ATT'] / data['defense_rushing_ATT']

    data['offense_downs_First Downs_rush_ratio'] = data['offense_downs_First Downs_RUSH'] / data['offense_downs_First Downs_TOTAL']
    data['offense_downs_First Downs_penalty_ratio'] = data['offense_downs_First Downs_PEN'] / data['offense_downs_First Downs_TOTAL']
    data['defense_downs_First Downs_rush_ratio'] = data['defense_downs_First Downs_RUSH'] / data['defense_downs_First Downs_TOTAL']
    data['defense_downs_First Downs_penalty_ratio'] = data['defense_downs_First Downs_PEN'] / data['defense_downs_First Downs_TOTAL']

    # data['offense_receiving_REC_per_game'] = data['offense_receiving_REC'] / data['games_played']
    # data['defense_receiving_REC_per_game'] = data['defense_receiving_REC'] / data['games_played']

    data['offense_passing_TD_per_game'] = data['offense_passing_TD'] / data['games_played']
    data['offense_rushing_TD_per_game'] = data['offense_rushing_TD'] / data['games_played']
    data['defense_passing_TD_per_game'] = data['defense_passing_TD'] / data['games_played']
    data['defense_rushing_TD_per_game'] = data['defense_rushing_TD'] / data['games_played']

    data['offense_pass_TD_per_rush_TD'] = data['offense_passing_TD'] / data['offense_rushing_TD']
    data['defense_pass_TD_per_rush_TD'] = data['defense_passing_TD'] / data['defense_rushing_TD']

    data['offense_passing_INT_per_game'] = data['offense_passing_INT'] / data['games_played']
    data['defense_passing_INT_per_game'] = data['defense_passing_INT'] / data['games_played']
    data['offense_pass_TD_to_INT'] = data['offense_passing_TD'] / data['offense_passing_INT']
    data['defense_pass_TD_to_INT'] = data['defense_passing_TD'] / data['defense_passing_INT']

    data['offense_receiving_FUM_per_game'] = data['offense_receiving_FUM'] / data['games_played']
    data['offense_rushing_FUM_per_game'] = data['offense_rushing_FUM'] / data['games_played']
    data['defense_receiving_FUM_per_game'] = data['defense_receiving_FUM'] / data['games_played']
    data['defense_rushing_FUM_per_game'] = data['defense_rushing_FUM'] / data['games_played']

    data['offense_receiving_LST_FUM_ratio'] = data['offense_receiving_LST'] / data['offense_receiving_FUM']
    data['offense_rushing_LST_FUM_ratio'] = data['offense_rushing_LST'] / data['offense_rushing_FUM']
    data['defense_receiving_LST_FUM_ratio'] = data['defense_receiving_LST'] / data['defense_receiving_FUM']
    data['defense_rushing_LST_FUM_ratio'] = data['defense_rushing_LST'] / data['defense_rushing_FUM']

    drop_after_calc = ['special_punting_PUNTS', 'special_punting_IN20', 
                       'special_kicking_Field Goals_FGA', 'special_returning_Kickoffs_ATT',
                       'offense_passing_SACK', 'defense_passing_SACK',
                       'offense_downs_Penalties_TOTAL', 'offense_downs_Penalties_YDS', 
                       'defense_downs_Penalties_TOTAL', 'defense_downs_Penalties_YDS',
                       'offense_passing_SYL', 'defense_passing_SYL', 
                       'defense_passing_SACK_per_game', 'offense_passing_SACK_per_game',
                       'defense_downs_Penalties_TOTAL_per_game', 'offense_downs_Penalties_TOTAL_per_game',
                       'offense_downs_Third Downs_ATT', 'offense_downs_Fourth Downs_ATT',
                       'defense_downs_Fourth Downs_ATT', 'defense_downs_Third Downs_ATT',
                       'offense_passing_ATT', 'offense_rushing_ATT', 
                       'defense_passing_ATT', 'defense_rushing_ATT', 
                       'offense_downs_First Downs_RUSH', 'offense_downs_First Downs_PEN',
                       'defense_downs_First Downs_RUSH', 'defense_downs_First Downs_PEN',
                       'offense_downs_First Downs_TOTAL', 'defense_downs_First Downs_TOTAL',
                       'offense_receiving_REC', 'defense_receiving_REC',
                       'offense_passing_TD', 'offense_rushing_TD', 'defense_passing_TD', 'defense_rushing_TD',
                       'offense_passing_INT', 'defense_passing_INT',
                       'offense_receiving_FUM', 'offense_rushing_FUM', 'defense_receiving_FUM', 'defense_rushing_FUM',
                       'offense_receiving_LST', 'offense_rushing_LST', 'defense_receiving_LST', 'defense_rushing_LST']

    drop_MADE_cols = data.filter(like = 'MADE').columns # att and pct cover thsi info

    data.drop(drop_after_calc, 1, inplace = True)
    data.drop(drop_MADE_cols, 1, inplace = True)
    
    return data