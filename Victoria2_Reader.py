import re
import csv

############################################################################################################################################################
# Created By Robert Milligan 2021 You may use and change this tool for any project you wish but please credit me in any produced works/progams/videos/posts#
############################################################################################################################################################
#you must check and change the following things for the program to work#
########################################################################
# 1. find the countryfile for vanilla or the mod you are using
        #it will be in Victoria 2/common/countries.txt
        #or if using a mod which overides it use Victoria 2/*modname*/common/countries.txt
countryfile_location = "C:/Program Files (x86)/Steam/steamapps/common/Victoria 2/mod/HPM/common/countries.txt"

# 2. Find the savegame locations
    #saves must be named 1.v2, 2.v2, 3.v2, 4.v2 etc..
save_game_folder = "C:/Users/granc/Documents/Paradox Interactive/Victoria II/HPM/save games"

# 3. Length of Game Saves
    #these 2 numbers must multiply together to make the total number of saves
saves_per_year = 2
years_of_game = 100
start_year = 1836

#4. Optionals
divide_all_results_by = 1 #set 1 for units, 1000 for thousands, 1000000 for millions etc.
remove_0_tags = True #removes tags from output if all results 0 meaning tag was never on the map or created
output_file_name = "output" #change this to whatever you want the output you want the csv file to be

#5. Type of data to grab
#you can only set one of the functions to True at once
Population_Reader_Bool = False
GDP_Reader_Bool = True
Culture_Religion_Reader_Bool = False

#6. Optionals for Culture_Religion_Reader
Use_All_Tags = False #set to False if you want to use "Use_Only_These_Tags" otherwise if it is True it will not care about the tag
Use_Only_These_Tags = ["USA"] #can be 1 tag or a list of them e.g. ["ENG,"FRA","USA"]

##############################################
year_list = ["blah","blah"]
country_list = [["XXX","Indigenous People"]]

def read_in_countries():
    for line in open(countryfile_location):
        firstsplit = line.split("=")

        if len(firstsplit) != 2:
            continue

        tag = firstsplit[0][:3]

        if firstsplit[0] == "dynamic_tags  ":
            continue

        secondsplit = re.split("/|\"",firstsplit[1])
        english_name = secondsplit[2].split(".")[0]
        country_list.append([tag,english_name])

    for i in range(years_of_game):
        for i in range(saves_per_year):
            year_list.append(start_year+i)
        for i in range(len(country_list)):
            for j in range(saves_per_year):
                country_list[i].append(0)

def Population_Reader():
    for l in range(1, 1 + (saves_per_year*years_of_game)):
        print(str(int(100*l/(saves_per_year*years_of_game)))+"%")
        filename = save_game_folder + "/" + str(l) + ".v2"
        province_end_tag = True
        savefile = open(filename, encoding='ISO-8859-1')
        current_tag = "REB"
        i = 0
        current_province = 1
        for line in savefile:
            i += 1
            if province_end_tag:

                if line[1:6] == "owner":
                    current_tag = line[8:11]
                    for k in range(len(country_list)):
                        if current_tag == country_list[k][0]:
                            current_tag_index = k

                elif line == "REB=\n":
                    province_end_tag = False

                elif line == str(current_province) + "=\n":
                    current_tag = "XXX"
                    current_tag_index = 0
                    current_province += 1

                if line[2:7] == "size=":
                    pop_size = int(line[7:-1]) * 4 / divide_all_results_by
                    country_list[current_tag_index][l + 1] += pop_size



        savefile = open(filename, encoding='ISO-8859-1')
        last_vassal = -5
        p = 0
        for line in savefile:

            p += 1
            if line[1:8] == "vassal=" or line[1:10] == "substate=":
                last_vassal = p

            if p == last_vassal + 2:
                master_tag = line[9:12]

            if p == last_vassal + 3:
                vassal_tag = line[10:13]
                master_index = None
                vassal_index = None
                for m in range(len(country_list)):
                    if country_list[m][0] == master_tag:
                        master_index = m
                    if country_list[m][0] == vassal_tag:
                        vassal_index = m

                if master_index == None:
                    print(master_tag)
                if vassal_index == None:
                    print(vassal_tag)

                country_list[master_index][l + 1] += country_list[vassal_index][l + 1]
                country_list[vassal_index][l + 1] = 0

                master_tag = None
                vassal_tag = None

def GDP_Reader():
    for l in range(1, 1 + (saves_per_year * years_of_game)):
        print(str(int(100 * l / (saves_per_year * years_of_game))) + "%")
        filename = save_game_folder + "/" + str(l) + ".v2"
        province_end_tag = True
        savefile = open(filename, encoding='ISO-8859-1')
        current_tag = "REB"
        i = 0
        current_province = 1
        for line in savefile:
            i += 1
            if province_end_tag:

                if line[1:6] == "owner":
                    current_tag = line[8:11]
                    for k in range(len(country_list)):
                        if current_tag == country_list[k][0]:
                            current_tag_index = k
                # print(current_tag)

                elif line == "REB=\n":
                    province_end_tag = False

                elif line == str(current_province) + "=\n":
                    current_tag = "XXX"
                    current_tag_index = 0
                    current_province += 1

                # Artisans
                if line[2:16] == "last_spending=":
                    country_list[current_tag_index][l + 1] -= float(line[16:]) / 1000 * 365.25 / divide_all_results_by
                elif line[2:20] == "production_income=":

                    country_list[current_tag_index][l + 1] += float(line[20:]) / 1000 * 365.25 / divide_all_results_by

                # RGO
                if line[2:14] == "last_income=":
                    country_list[current_tag_index][l + 1] += float(line[14:]) / 1000 * 365.25 / divide_all_results_by

            else:
                if line[3:] == "=\n":
                    if ord(line[0]) >= 65 and ord(line[0]) <= 90 and ord(line[1]) >= 65 and ord(
                            line[1]) <= 90 and ord(line[2]) >= 65 and ord(line[2]) <= 90:
                        current_tag = line[0:3]
                        for k in range(len(country_list)):
                            if current_tag == country_list[k][0]:
                                current_tag_index = k

                # factory
                if line[3:17] == "last_spending=":
                    country_list[current_tag_index][l + 1] -= float(line[17:]) / 1000 * 365.25 / divide_all_results_by
                elif line[3:15] == "last_income=":
                    country_list[current_tag_index][l + 1] += float(line[15:]) / 1000 * 365.25 / divide_all_results_by


        savefile = open(filename, encoding='ISO-8859-1')
        last_vassal = -5
        p = 0
        for line in savefile:

            p += 1
            if line[1:8] == "vassal=" or line[1:10] == "substate=":
                last_vassal = p

            if p == last_vassal + 2:
                master_tag = line[9:12]

            if p == last_vassal + 3:
                vassal_tag = line[10:13]
                master_index = None
                vassal_index = None
                for m in range(len(country_list)):
                    if country_list[m][0] == master_tag:
                        master_index = m
                    if country_list[m][0] == vassal_tag:
                        vassal_index = m

                if master_index == None:
                    print(master_tag)
                if vassal_index == None:
                    print(vassal_tag)

                country_list[master_index][l + 1] += country_list[vassal_index][l + 1]
                country_list[vassal_index][l + 1] = 0

                master_tag = None
                vassal_tag = None

def Culture_Religion():
    for l in range(1, 1 + (saves_per_year * years_of_game)):
        print(str(int(100 * l / (saves_per_year * years_of_game))) + "%")
        filename = save_game_folder + "/" + str(l) + ".v2"
        province_end_tag = True
        savefile = open(filename, encoding='ISO-8859-1')
        current_tag = "REB"
        current_province = 1
        size_flag = False
        province_num = 0
        for line in savefile:

            if province_end_tag:

                if line[1:6] == "owner":
                    current_tag = line[8:11]

                if line[4:6] == "=\n" and line[3:4] != "o" and line[3:4] != "d":
                    current_province = line[0:4]
                    current_tag = "Null"
                    # print(current_province)

                elif line == "REB=\n":
                    province_end_tag = False

                if current_tag in Use_Only_These_Tags or Use_All_Tags:
                    if size_flag:
                        size_flag = False
                        current_culture = line[2:-1]
                        added_Flag = False
                        for j in range(len(country_list)):
                            if current_culture == country_list[j][0]:
                                country_list[j][l] += pop_size
                                added_Flag = True
                                break
                        if not added_Flag:
                            country_list.append([current_culture])
                            for i in range(saves_per_year * years_of_game):
                                country_list[-1].append(0)
                            country_list[-1][l] += pop_size

                    if line[2:7] == "size=":
                        pop_size = int(line[7:-1]) * 4 / divide_all_results_by
                        size_flag = True

if __name__ == "__main__":
    read_in_countries()

    if Population_Reader_Bool:
        Population_Reader()
        year_list = ["Code", "Name"]
    if GDP_Reader_Bool:
        GDP_Reader()
        year_list = ["Code", "Name"]
    if Culture_Religion_Reader_Bool:
        Culture_Religion()
        year_list = ["Culture"]

    for j in range(years_of_game):
        year_list.append(start_year + j)
        year_list.append(start_year + j)

    if remove_0_tags:
        country_list = [x for x in country_list if max(x[2:]) > 0]

    with open(output_file_name + ".csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(year_list)
        writer.writerows(country_list)
