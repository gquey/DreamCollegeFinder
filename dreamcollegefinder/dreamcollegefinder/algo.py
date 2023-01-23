import pandas as pd
from .models import SchoolInfo, Rankings

def recommend(preferences):
    print("prefs:", preferences)

    print(Rankings.objects.all()[0].name)
    rankings = pd.DataFrame(list(Rankings.objects.all().values()))
    schoolinfo = pd.DataFrame(list(SchoolInfo.objects.all().values()))

    zerocount = 0 #variable to keep track of the number of NAN information for each college (if it is >=7, that college will be dropped as there is not sufficient information)

    #create a column with the state info
    states = []
    for i, elem in schoolinfo.iterrows(): 
        states.append(elem['location'][-2:])
    schoolinfo['State'] = states
    #merge data
    merged = pd.merge(schoolinfo, rankings, how='left', left_on='name', right_on='name')

    location_pref = preferences['question_1']
    location = preferences['question_2']
    acceptance_pref = preferences['question_3']
    price = preferences['question_4']
    price_pref = preferences['question_5']
    sat = preferences['question_6']
    sat_pref = preferences['question_7']

    prefs = []

    stlife_pref = preferences['question_8']
    if stlife_pref != '':
        prefs.append('SL')
    else:
        stlife_pref = '0'

    academics_pref = preferences['question_9'] 
    if academics_pref != '':
        prefs.append('AC')
    else:
        academics_pref = '0'

    ath_pref = preferences['question_10'] 
    if ath_pref != '':
        prefs.append('AT')
    else:
        ath_pref = '0'

    div_pref = preferences['question_11'] 
    if div_pref != '':
        prefs.append('DI')
    else:
        div_pref = '0'

    prof_pref = preferences['question_12'] 
    if prof_pref != '':
        prefs.append('PR')
    else:
        prof_pref = '0'

    safe_pref = preferences['question_13'] 
    if safe_pref != '':
        prefs.append('SA')
    else:
        safe_pref = '0'

    val_pref = preferences['question_14'] 
    if val_pref != '':
        prefs.append('VA')
    else:
        val_pref = '0'

    ranks = {'SL' : 'collegeLife', 'AC' : 'academics', 'AT' : 'athletics', 'DI' : 'diversity', 'PR' : 'professors', 'SA' : 'safety', 'VA' : 'rank'}

    for i, elem in rankings.iterrows():
        for col in rankings.columns:
            if elem[col] == 0:
                rankings.at[i, col] = 25.01 #Assign the mean to fields NAN
                zerocount += 1

        if zerocount > 5: #We want to drop those college with information for only one characteristic, but we will keep it if that characteristic is important for the user
            for key in ranks:
                if (key not in prefs and elem[ranks[key]] == 25.01):
                    rankings = rankings.drop(i, axis=0)
                    break
        zerocount = 0


    denominator = int(location_pref) + int(acceptance_pref) + int(price_pref) + int(stlife_pref) + int(academics_pref) + int(ath_pref) + int(div_pref) + int(prof_pref) + int(safe_pref) + int(val_pref)
    prices = {0 : 0, 1 : 15000, 2 : 25000, 3 : 35000, 4 : 35000.1 }
    weights = [0] * len(merged['name'])
    for index, college in merged.iterrows():

        if college['State'] == location: 
            weights[index] += int(location_pref)/denominator #if college is from preferred state, sum the weight

        weights[index] += int(college['acceptanceRate'][:-1])*0.01*int(acceptance_pref)/denominator #add the acceptance rate with the corresponding weight

        pr = int(college['netPrice'].replace(',', '')[1:]) #format net price to integer
        if pr >= prices[int(price)-1] and pr <= prices[int(price)]: #if price lies between range, add it with its weight
            weights[index] += int(price_pref)/denominator

        if college['rangeSAT'] != 'nan':
            minsat = int(college['rangeSAT'].split('-')[0])
            if int(sat) <= minsat and sat_pref == 'Y': #if option has been selected, rule out colleges with higher SAT scores
                weights[index] = -999999

        if ('SL' in prefs): weights[index] -= college['collegeLife']*0.02*int(stlife_pref)/denominator
        
        if ('AC' in prefs): weights[index] -= college['academics']*0.02*int(academics_pref)/denominator

        if ('DI' in prefs): weights[index] -= college['diversity']*0.02*int(div_pref)/denominator

        if ('PR' in prefs): weights[index] -= college['professors']*0.02*int(prof_pref)/denominator

        if ('VA' in prefs): weights[index] -= college['rank']*0.02*int(val_pref)/denominator

    merged['Ranking'] = weights
    sorted = merged.sort_values(by = ['Ranking'], ascending=False)
    return sorted[:10]