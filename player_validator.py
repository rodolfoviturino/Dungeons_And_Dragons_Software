import logging
import json
import tkinter as tk
from logging.handlers import RotatingFileHandler
from math import floor
from functools import partial
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename, asksaveasfilename

import pandas as pd
import pygame


def save_character(*args):
    logger.debug('Save character option was called.')
    player_character = {"name":name_display['text'],
                        "alignment":alignment_value_inside.get(),
                        "background":background_value_inside.get(),
                        "race":race_value_inside.get(),
                        "subrace":subrace_value_inside.get(),
                        "class":class_value_inside.get(),
                        "level":level_value_inside.get(),
                        "str_ability_score":str_attributes_inside.get(),
                        "dex_ability_score":dex_attributes_inside.get(),
                        "con_ability_score":con_attributes_inside.get(),
                        "int_ability_score":int_attributes_inside.get(),
                        "wis_ability_score":wis_attributes_inside.get(),
                        "cha_ability_score":cha_attributes_inside.get(),
                        "available_skills":available_skills_list,
                        "restore_skills":restore_skills_list,
                        "background_skills_proficiencies_dict":background_skill_proficiencies_dict,
                        "class_skills_proficiencies_dict":class_skill_proficiencies_dict,
                        "selected_class_dict":selected_class_dict
                        }
    filename = asksaveasfilename()
    if filename:
        with open(f'{filename}.JSON', 'w') as json_file:
            json.dump(player_character, json_file)
            logger.debug(f'Character saved into {filename}.')
    else:
        logger.debug('Save character operation was cancelled.')


def open_character(*args):
    global available_skills_list
    global background_skill_proficiencies_dict
    global class_skill_proficiencies_dict
    global proficiencies_skills_dict
    global restore_skills_list
    global selected_class_dict

    logger.debug('Open character option was called.')
    character_reseter()
    filename = askopenfilename()
    if filename:
        if filename.endswith('.JSON'):
            logger.debug(f'Opening character from file: {filename}')
            with open(filename) as json_file:
                player_character = json.load(json_file)
                name_display.config(text=player_character['name'])
                alignment_value_inside.set(player_character['alignment'])
                background_value_inside.set(player_character['background'])
                race_value_inside.set(player_character['race'])
                subrace_value_inside.set(player_character['subrace'])
                class_value_inside.set(player_character['class'])
                level_value_inside.set(player_character['level'])
                str_attributes_inside.set(player_character['str_ability_score'])
                dex_attributes_inside.set(player_character['dex_ability_score'])
                con_attributes_inside.set(player_character['con_ability_score'])
                int_attributes_inside.set(player_character['int_ability_score'])
                wis_attributes_inside.set(player_character['wis_ability_score'])
                cha_attributes_inside.set(player_character['cha_ability_score'])
                # Recreates the options in the skills options menu buttons.
                available_skills_list = player_character['available_skills']
                logger.debug(f'Available skills: {available_skills_list}')
                if isinstance(available_skills_list, list):
                    print('recreating button available')
                    menu = choose_skills_menu['menu']
                    menu.delete(0, 'end')
                    for skill in available_skills_list:
                        menu.add_command(label=skill, 
                                        command=lambda skill_options=skill: choose_skills_value_inside.set(skill_options))
                else:
                    available_skills_list = list()
                    logger.debug(f'Available skills is not a list, which means no previous option has been selected before')
                restore_skills_list = player_character['restore_skills']
                logger.debug(f'Restore skills: {restore_skills_list}')
                if isinstance(restore_skills_list, list):
                    print('recreating button restore')
                    menu = restore_skills_menu['menu']
                    menu.delete(0, 'end')
                    for skill in restore_skills_list:
                        menu.add_command(label=skill, 
                                        command=lambda restore_skill_options=skill: restore_skills_value_inside.set(restore_skill_options))
                else:
                    restore_skills_list = list()
                    logger.debug(f'Restore skills is not a list, which means no previous option has been selected before')
                background_skill_proficiencies_dict = player_character['background_skills_proficiencies_dict']
                class_skill_proficiencies_dict = player_character['class_skills_proficiencies_dict']
                selected_class_dict = player_character['selected_class_dict']
                number_of_skills_to_restore = len(restore_skills_list)
                if number_of_skills_to_restore > 0:
                    restore_skills_menu['state'] = 'normal'
                    number_of_skills_to_display = int(selected_class_dict['choose_skills_number']) - number_of_skills_to_restore
                    number_of_skills_display.config(text=number_of_skills_to_display)
                else:
                    restore_skills_menu['state'] = 'disabled'
                    number_of_skills_display.config(text=selected_class_dict['choose_skills_number'])
            display_updater()
        else:
            logger.debug('The file selected was not a .JSON extension.')
    else:
        logger.debug('Open character operation was cancelled by the user.')


def new_character(*args):
    logger.debug('New character option was called.')
    character_reseter()
    with open('player_characters/new_player_character.JSON') as json_file:
        player_character = json.load(json_file)
        name_display.config(text=player_character['name'])
        alignment_value_inside.set(player_character['alignment'])
        background_value_inside.set(player_character['background'])
        race_value_inside.set(player_character['race'])
        subrace_value_inside.set(player_character['subrace'])
        class_value_inside.set(player_character['class'])
        level_value_inside.set(player_character['level'])
        str_attributes_inside.set(player_character['str_ability_score'])
        dex_attributes_inside.set(player_character['dex_ability_score'])
        con_attributes_inside.set(player_character['con_ability_score'])
        int_attributes_inside.set(player_character['int_ability_score'])
        wis_attributes_inside.set(player_character['wis_ability_score'])
        cha_attributes_inside.set(player_character['cha_ability_score'])
        choose_skills_value_inside.set(player_character['available_skills'])
        restore_skills_value_inside.set(player_character['restore_skills'])
        logger.debug('Cleared the older options and reseted the buttons.')
    display_updater()


def play_music(*args):
    logger.debug('Play music button was called.')
    pygame.mixer.music.play(loops=-1) # Infinite loop


def stop_music(*args):
    logger.debug('Stop music button was called.')
    pygame.mixer.music.stop()


def music_volume(*args):
    global volume_slider
    global volume_window

    logger.debug('Music volume button was called.')
    if tk.Toplevel.winfo_exists(volume_window):
        logger.debug('Another window volume slider was already oppened.')
    else:
        logger.debug('Openning music volume slider window.')
        volume_window = tk.Toplevel(window)
        volume_window.title('Music Options')
        volume_window.geometry('250x300')
        volume_window_icon_path = f'{icons_path}/volume.ico'
        volume_window.iconbitmap(volume_window_icon_path)
        volume_window.resizable(width=False, height=False)
        volume_frame = tk.LabelFrame(volume_window, text="Volume")
        volume_frame.pack(pady=20)
        volume_slider = tk.Scale(volume_frame)
        volume_slider.config(from_=100,
                            to=0,
                            orient=tk.VERTICAL,
                            command=volume_adjustment,
                            length=200)
        # Sets the volume starting as 100, which is the maximum in the scale I created.
        volume_slider.set(100)
        volume_slider.pack(pady=10)


def volume_adjustment(*args):
    global volume_slider

    volume = float(volume_slider.get()) / 100
    pygame.mixer.music.set_volume(volume)


def name_selector(*args):
    logger.debug('Name submit button was called.')
    choosen_name = name_entry.get().title()
    name_display.config(text=choosen_name)
    logger.info(f'Name: {choosen_name}')


def alignment_selector(*args):
    logger.debug('Alignment button was called.')
    choosen_alignment= alignment_value_inside.get()
    logger.info(f'Alignment: {choosen_alignment}')


def background_selector(*args):
    global available_skills_list
    global background_skill_proficiencies_dict
    global class_skill_proficiencies_dict
    global removed_background_skill_from_class_list_memory
    global restore_skills_list

    logger.debug('Background button was called.')
    choosen_background= background_value_inside.get()
    logger.info(f'Background: {choosen_background}')
    # Resets old background values because a new background was selected.
    for skill in removed_background_skill_from_class_list_memory:
        available_skills_list.append(skill)
    for proficiency_skill in background_skill_proficiencies_dict.keys():
        background_skill_proficiencies_dict[proficiency_skill] = 0
    if choosen_background != 'Choose': 
        # Condition for preventing that when a new character is selected the program breaks.
        character_characteristics_df = pd.ExcelFile('datasets/character_characteristics.xlsx')
        background_df = character_characteristics_df.parse('backgrounds')
        choosen_background_df = background_df[background_df['background'] == choosen_background]
        proficiencies_of_choosen_background_df = choosen_background_df['skill_proficiencies']
        proficiencies_of_choosen_background = choosen_background_df.at[proficiencies_of_choosen_background_df.first_valid_index(), 'skill_proficiencies']
        skill_proficiencies_from_background = proficiencies_of_choosen_background.split(';')
        for proficiency_skill in skill_proficiencies_from_background:
            proficiency_skill = proficiency_skill.replace(' ', '')
            background_skill_proficiencies_dict[proficiency_skill] = 1
        removed_background_skill_from_class_list_memory = list()
        choosen_class= class_value_inside.get()
        if choosen_class != 'Choose':
            for proficiency_skill in skill_proficiencies_from_background:
                proficiency_skill = proficiency_skill.replace(' ', '')
                if proficiency_skill in restore_skills_list:
                    number_of_skills = int(number_of_skills_display['text'])
                    number_of_skills += 1
                    number_of_skills_display.config(text=number_of_skills)
                    restore_skills_list.remove(proficiency_skill)
                    removed_background_skill_from_class_list_memory.append(proficiency_skill)
                    class_skill_proficiencies_dict[proficiency_skill] = 0
                    restore_skills_list.sort()
                else:
                    pass
                if proficiency_skill in available_skills_list:
                    available_skills_list.remove(proficiency_skill)
                    available_skills_list.sort()
                    if proficiency_skill in removed_background_skill_from_class_list_memory:
                        # Condition to avoids skills duplication.
                        pass
                    else:
                        removed_background_skill_from_class_list_memory.append(proficiency_skill)
                else:
                    pass
            # Recreates the options in the options menu buttons.
            menu = choose_skills_menu['menu']
            menu.delete(0, 'end')
            for skill in available_skills_list:
                menu.add_command(label=skill, 
                                command=lambda skill_options=skill: choose_skills_value_inside.set(skill_options))
            menu = restore_skills_menu['menu']
            menu.delete(0, 'end')
            for skill in restore_skills_list:
                menu.add_command(label=skill, 
                                command=lambda restore_skill_options=skill: restore_skills_value_inside.set(restore_skill_options))
            current_number_of_skills_for_restauration = len(restore_skills_list)
            if current_number_of_skills_for_restauration == 0:
                restore_skills_value_inside.set('Choose')
                restore_skills_menu['state'] = 'disabled'
            else:
                pass
            if int(number_of_skills_display['text']) > 0:
                choose_skills_menu['state'] = 'normal'
            else:
                pass
        else:
            pass
        display_updater()
    else:
        pass


def race_selector(*args):
    global attributes_list
    global racial_bonuses_df
    global races_and_subraces_dict
    global selected_race_modifiers_dict
    global selected_subrace_modifiers_dict

    logger.debug('Race button was called.')
    choosen_race = race_value_inside.get()
    logger.info(f'Race: {choosen_race}')
    # Because the subrace depends exclusively on the previously choosen race,
    # when a new race is selected, the old subrace must also be reseted.
    for attribute in attributes_list:
        selected_subrace_modifiers_dict[attribute] = 0
    if choosen_race != 'Choose': 
        # This condition prevents that when the new_character button is called, the system breaks.
        choosen_race_df = racial_bonuses_df.parse(choosen_race)
        for attribute in attributes_list:
            modifier = choosen_race_df.at[0, attribute]
            selected_race_modifiers_dict[attribute] = modifier
        optional_points = choosen_race_df.at[0, 'optional_point']
        optional_points_display.config(text=optional_points)
        # If any optional point is available, enables the + and - buttons for selection.
        if optional_points > 0:
            str_plus_button['state'] = 'normal'
            str_minus_button['state'] = 'normal'
            dex_plus_button['state'] = 'normal'
            dex_minus_button['state'] = 'normal'
            con_plus_button['state'] = 'normal'
            con_minus_button['state'] = 'normal'
            int_plus_button['state'] = 'normal'
            int_minus_button['state'] = 'normal'
            wis_plus_button['state'] = 'normal'
            wis_minus_button['state'] = 'normal'
            cha_plus_button['state'] = 'normal'
            cha_minus_button['state'] = 'normal'
        else:
            str_plus_button['state'] = 'disabled'
            str_minus_button['state'] = 'disabled'
            dex_plus_button['state'] = 'disabled'
            dex_minus_button['state'] = 'disabled'
            con_plus_button['state'] = 'disabled'
            con_minus_button['state'] = 'disabled'
            int_plus_button['state'] = 'disabled'
            int_minus_button['state'] = 'disabled'
            wis_plus_button['state'] = 'disabled'
            wis_minus_button['state'] = 'disabled'
            cha_plus_button['state'] = 'disabled'
            cha_minus_button['state'] = 'disabled'
        base_speed = choosen_race_df.at[0, 'speed']
        speed_display.config(text=base_speed)
        display_updater()
        # Verifies if there is any subrace available for selection. If there is, enables the subrace button.
        subrace_value_inside.set('Choose') # Sets the name "Choose" as default.
        subraces = races_and_subraces_dict[choosen_race]
        if subraces[0] is not None: # A subrace from the choosen race exist.
            subrace_menu['state'] = 'normal' # Enables the subrace button for selection.
            menu = subrace_menu['menu']
            menu.delete(0, 'end')
            for subrace in subraces: # Adds the list of options from subraces variable for possible selection.
                menu.add_command(label=subrace, 
                                command=lambda subrace_options=subrace: subrace_value_inside.set(subrace_options))
        else:
            subrace_menu['state'] = 'disable' # A subrace from the choosen race does not exist.
    else:
        pass


def subrace_selector(*args):
    # The button that calls this function may be enabled after the button that 
    # points to race_selector function is pressed.
    global attributes_list
    global racial_bonuses_df

    logger.debug('Subrace button was called.')
    if race_value_inside.get() != 'Choose':
        # This condition prevents that when the new_character button is called, the system breaks.
        choosen_subrace= subrace_value_inside.get()
        if choosen_subrace != 'Choose' and choosen_subrace != 'None': 
            logger.info(f'Subrace: {choosen_subrace}')
            choosen_race_df = racial_bonuses_df.parse(race_value_inside.get())
            choosen_subrace_df = choosen_race_df[choosen_race_df['race_and_subraces'] == choosen_subrace]
            for attribute in attributes_list:   # Resets the old subrace values.
                subrace_modifier = choosen_race_df.at[choosen_subrace_df.first_valid_index(), attribute]
                selected_subrace_modifiers_dict[attribute] = subrace_modifier
            speed = choosen_race_df.at[choosen_subrace_df.first_valid_index(), 'speed']
            speed_display.config(text=speed)
        elif races_and_subraces_dict[race_value_inside.get()][0] is None:
            logger.debug('No subrace available.')
        else:
            logger.debug('No subrace was choosen yet.')
        display_updater()
    else:
        logger.debug('No subrace was selected due to the race still being in the "Choose" mode.')


def class_selector(*args):
    # Class influences saving throws and skills. Note that skills are 
    # also influenced by the background as well.
    global available_skills_list
    global classes_df
    global class_skill_proficiencies_dict
    global restore_skills_list
    global saving_throws_dict
    global selected_class_dict

    logger.debug('Class button was called.')
    choosen_class= class_value_inside.get()
    logger.info(f'Class: {choosen_class}')
    # Resets old stored saving throws values when a new class is selected.
    for saving_throw in saving_throws_dict.keys():
        saving_throws_dict[saving_throw] = 0
    # Also resets the old choosen skills from the class.
    choose_skills_value_inside.set('Choose')
    choose_skills_menu['state'] = 'disabled'
    restore_skills_list = list() # Remakes the choices as a clean list.
    restore_skills_value_inside.set('Choose')
    restore_skills_menu['state'] = 'disabled'
    for proficiency_skill in class_skill_proficiencies_dict.keys():
        class_skill_proficiencies_dict[proficiency_skill] = 0
    if choosen_class != 'Choose':
        choosen_class_df = classes_df.parse(choosen_class)
        # Updates the class modifiers dictionary based on which class was selected.
        for key in selected_class_dict.keys():
            modifier = str(choosen_class_df.at[0, key])
            selected_class_dict[key] = modifier
            if key == 'saving_throws_proficies':
                saving_throws = modifier.split(';')
                for saving_throw in saving_throws:
                    saving_throw = saving_throw.replace(' ', '')
                    saving_throws_dict[saving_throw] = 1
        # Updating skills
        number_of_skills = selected_class_dict['choose_skills_number']
        if number_of_skills != '0':
            number_of_skills_display.config(text=number_of_skills)
            choose_skills_menu['state'] = 'normal'
            available_skills_from_class = str(choosen_class_df.at[0, 'choose_skills_list'])
            available_list_of_skills_from_class = available_skills_from_class.split(';')
            in_use_list_of_skills_from_background = [key for key, value in background_skill_proficiencies_dict.items() if value == 1]
            available_skills_list = list(set(available_list_of_skills_from_class) - set(in_use_list_of_skills_from_background))
            available_skills_list.sort()
            # Constructing the available options in the button.
            # Note that if a new background is selected, this button will need
            # to be remade once again.
            menu = choose_skills_menu['menu']
            menu.delete(0, 'end')
            for skill in available_skills_list:
                menu.add_command(label=skill, 
                                command=lambda skill_options=skill: choose_skills_value_inside.set(skill_options))
        else:
            pass
        display_updater()
    else:
        pass


def proficiency_skills_selector(*args):
    global available_skills_list
    global class_skill_proficiencies_dict
    global restore_skills_list

    logger.debug('Proficiency skill button was called.')
    choosen_proficiency_skill = choose_skills_value_inside.get()
    current_number_of_skills = int(number_of_skills_display['text'])
    if current_number_of_skills > 0 and choosen_proficiency_skill != 'Choose':
        logger.info(f'Choosen proficiency: {choosen_proficiency_skill}')
        restore_skills_menu['state'] = 'normal'
        current_number_of_skills -= 1
        number_of_skills_display.config(text=current_number_of_skills)
        available_skills_list.remove(choosen_proficiency_skill)
        logger.debug('Appending the choosen proficiency into the removed list.')
        restore_skills_list.append(choosen_proficiency_skill)
        restore_skills_list.sort()
        class_skill_proficiencies_dict[choosen_proficiency_skill] = 1
        # Reconstruct the options button but this time without the selected option.
        # The selected option will then be displayed on the removed options.
        menu = choose_skills_menu['menu']
        menu.delete(0, 'end')
        for skill in available_skills_list:
            menu.add_command(label=skill, 
                            command=lambda skill_options=skill: choose_skills_value_inside.set(skill_options))
        # Also reconstructs the options for the removed skills.
        menu = restore_skills_menu['menu']
        menu.delete(0, 'end')
        for skill in restore_skills_list:
            menu.add_command(label=skill, 
                            command=lambda restore_skill_options=skill: restore_skills_value_inside.set(restore_skill_options))
        if current_number_of_skills == 0:
            choose_skills_menu['state'] = 'disabled'
        else:
            pass
    else:
        choose_skills_menu['state'] = 'disabled'
        logger.debug(f'Choosen proficiency: {choosen_proficiency_skill}')
    display_updater()


def restore_proficiency_skills_selector(*args):
    # This button acts mainly as the inverse of the "proficiency_skills_selector".
    # Stacks the selected options from proficiency_skills_selector to this button,
    # and sends back to that button the selected options in here.
    global available_skills_list
    global class_skill_proficiencies_dict
    global restore_skills_list

    logger.debug('Restore proficiency button was called.')
    restore_choosen_proficiency_skill = restore_skills_value_inside.get()
    current_number_of_skills_for_restauration = len(restore_skills_list)
    if current_number_of_skills_for_restauration > 0:
        logger.info(f'Selected proficiency for restauration: {restore_choosen_proficiency_skill}')
        current_number_of_skills_for_restauration -=1
        choose_skills_menu['state'] = 'normal'
        current_number_of_skills = int(number_of_skills_display['text'])
        current_number_of_skills += 1
        number_of_skills_display.config(text=current_number_of_skills)
        restore_skills_list.remove(restore_choosen_proficiency_skill)
        available_skills_list.append(restore_choosen_proficiency_skill)
        available_skills_list.sort()
        class_skill_proficiencies_dict[restore_choosen_proficiency_skill] = 0
        menu = choose_skills_menu['menu']
        menu.delete(0, 'end')
        for skill in available_skills_list:
            menu.add_command(label=skill, 
                            command=lambda skill_options=skill: choose_skills_value_inside.set(skill_options))
        menu = restore_skills_menu['menu']
        menu.delete(0, 'end')
        for skill in restore_skills_list:
            menu.add_command(label=skill, 
                            command=lambda restore_skill_options=skill: restore_skills_value_inside.set(restore_skill_options))
        if current_number_of_skills_for_restauration == 0:
            restore_skills_value_inside.set('Choose')
            restore_skills_menu['state'] = 'disabled'
    else:
        logger.debug(f'Selected proficiency for restauration: {restore_choosen_proficiency_skill}')
    display_updater()


def level_selector(*args):
    logger.debug('Level button was called.')
    choosen_level = int(level_value_inside.get())
    logger.info(f'Level: {choosen_level}')
    if 1 <= choosen_level <= 4:
        proficiency_bonus = 2
    elif 5 <= choosen_level <= 8:
        proficiency_bonus = 3
    elif 9 <= choosen_level <= 12:
        proficiency_bonus = 4
    elif 13 <= choosen_level <= 16:
        proficiency_bonus = 5
    elif 17 <= choosen_level <= 20:
        proficiency_bonus = 6
    proficiency_bonus_display.config(text=proficiency_bonus)
    display_updater()


def attributes_selector(*args):
    global attributes_available_options_list
    global attributes_inside_list
    global standard_attributes_list

    logger.debug('Attributes button was called.')
    already_in_use_attributes = list()
    # Loop in order to get all "already in use" attributes. Also updates the modifiers
    for attribute in attributes_inside_list:
        attribute = attribute.get()
        if attribute.isnumeric():
            used_option = int(attribute)
            already_in_use_attributes.append(used_option)
    attributes_available_options_list = list(set(standard_attributes_list) - set(already_in_use_attributes))
    menu = str_attributes_option_menu['menu']
    menu.delete(0, 'end')
    for attribute in reversed(attributes_available_options_list):
        menu.add_command(label=attribute, 
                        command=lambda attribute_options=attribute: str_attributes_inside.set(attribute_options))
    menu = dex_attributes_option_menu['menu']
    menu.delete(0, 'end')
    for attribute in reversed(attributes_available_options_list):
        menu.add_command(label=attribute, 
                        command=lambda attribute_options=attribute: dex_attributes_inside.set(attribute_options))
    menu = con_attributes_option_menu['menu']
    menu.delete(0, 'end')
    for attribute in reversed(attributes_available_options_list):
        menu.add_command(label=attribute, 
                        command=lambda attribute_options=attribute: con_attributes_inside.set(attribute_options))
    menu = int_attributes_option_menu['menu']
    menu.delete(0, 'end')
    for attribute in reversed(attributes_available_options_list):
        menu.add_command(label=attribute, 
                        command=lambda attribute_options=attribute: int_attributes_inside.set(attribute_options))
    menu = wis_attributes_option_menu['menu']
    menu.delete(0, 'end')
    for attribute in reversed(attributes_available_options_list):
        menu.add_command(label=attribute, 
                        command=lambda attribute_options=attribute: wis_attributes_inside.set(attribute_options))
    menu = cha_attributes_option_menu['menu']
    menu.delete(0, 'end')
    for attribute in reversed(attributes_available_options_list):
        menu.add_command(label=attribute, 
                        command=lambda attribute_options=attribute: cha_attributes_inside.set(attribute_options))
    display_updater()


def attributes_reseter():
    global attributes_inside_list

    logger.debug('Attributes reseter button was called.')
    for attribute in attributes_inside_list:
        attribute.set('Choose')
    logger.info('Attributes reseted.')
    display_updater()


def character_reseter():
    global available_skills_list
    global background_skill_proficiencies_dict
    global class_skill_proficiencies_dict
    global proficiencies_skills_attribute_type_dict
    global proficiencies_skills_dict
    global restore_skills_list
    global saving_throws_dict
    global selected_class_dict
    global selected_race_modifiers_dict
    global selected_subrace_modifiers_dict

    logger.debug('Character reseter function was called.')
    for key in saving_throws_dict.keys():
        saving_throws_dict[key] = 0
    selected_race_modifiers_dict = saving_throws_dict.copy()
    selected_subrace_modifiers_dict = saving_throws_dict.copy()
    for key in proficiencies_skills_dict.keys():
        proficiencies_skills_dict[key] = 0
    background_skill_proficiencies_dict = proficiencies_skills_dict.copy()
    class_skill_proficiencies_dict = proficiencies_skills_dict.copy()
    for key in selected_class_dict.keys():
        selected_class_dict[key] = 0
    available_skills_list = list()
    restore_skills_list = list()
    number_of_skills_display.config(text=0)
    speed_display.config(text=0)
    subrace_menu['state'] = 'disabled'


def attributes_modifiers_display_updater():
    global attributes_list
    global attributes_inside_list
    global selected_race_modifiers_dict
    global selected_subrace_modifiers_dict

    logger.debug('Attributes modifiers display updater was called.')
    # Re-calculates the modifiers.
    for idx, attribute in enumerate(attributes_list):
        race_modifier = selected_race_modifiers_dict[attribute]
        subrace_modifier = selected_subrace_modifiers_dict[attribute]
        attribute_modifier = attributes_inside_list[idx].get()
        if attribute_modifier.isnumeric():
            attribute_modifier = int(attribute_modifier)
            attribute_modifier = floor((attribute_modifier-10)/2)
            attribute_value = race_modifier + subrace_modifier + attribute_modifier
        else: # The attribute was not choosen yet.
            attribute_value = race_modifier + subrace_modifier
        attributes_modifiers_display_variables_list[idx].configure(text=attribute_value)


def optional_points_updater(attribute_name, operation):
    # The only race that have optional distribution points is the "half-elf", and this
    # logic works perfectly fine for it. But, if a new race or subrace also
    # happens to have optional distribution points, this logic may need some
    # modifications.
    global selected_race_modifiers_dict

    logger.debug('Race optional points modifiers display updater was called.')
    remaining_distribution_points = int(optional_points_display["text"])
    current_mod = selected_race_modifiers_dict[attribute_name]
    if remaining_distribution_points > 0:
        if current_mod == 0 and operation == '+':
            remaining_distribution_points -= 1
            selected_race_modifiers_dict[attribute_name] += 1
            optional_points_display.config(text=remaining_distribution_points)
        elif current_mod == 1 and operation == '-':
            remaining_distribution_points += 1
            selected_race_modifiers_dict[attribute_name] -= 1
            optional_points_display.config(text=remaining_distribution_points)
        else:
            pass
    elif current_mod == 1 and operation == '-':
        remaining_distribution_points += 1
        selected_race_modifiers_dict[attribute_name] -= 1
        optional_points_display.config(text=remaining_distribution_points)
    else:
        pass
    display_updater()


def armor_class_display_updater():
    logger.debug('Armor class modifiers display updater was called.')
    dex_modifier = int(dex_modifier_display["text"])
    armor_class_base = 10
    armor_class_value = armor_class_base + dex_modifier
    armor_class_display.config(text=armor_class_value)
    logger.debug(f'Armor Class: {armor_class_value}')


def initiative_display_updater():
    logger.debug('Initiative display updater was called.')
    initiative_modifier = int(dex_modifier_display["text"])
    initiative_display.config(text=initiative_modifier)
    logger.debug(f'Initiative: {initiative_modifier}')


def saving_throw_display_updater():
    global attributes_list
    global attributes_modifiers_display_variables_list
    global saving_throws_dict
    global saving_throws_variables_display_list

    logger.debug('Saving throw modifiers display updater was called.')
    # Gets the current attributes modifiers values and updates the saving throw based on them.
    for idx, attribute_variables in enumerate(attributes_modifiers_display_variables_list):
        attribute = attribute_variables["text"]
        if saving_throws_dict[attributes_list[idx]] == 1:
            saving_throw = int(attribute) + int(proficiency_bonus_display["text"])
            saving_throws_variables_display_list[idx].config(text=saving_throw)
        else: 
            # There is no saving throw proficiency in this attribute, 
            # so the final attribute will the the raw attribute modifier.
            saving_throws_variables_display_list[idx].config(text=attribute)


def proficiencies_skills_display_updater():
    global attributes_list
    global attributes_modifiers_display_variables_list
    global proficiencies_skills_attribute_type_dict
    global proficiencies_skills_dict
    global proficiencies_skills_variables_display_list

    logger.debug('Proficiencies skills modifiers display updater was called.')
    for idx, proficiency_skill in enumerate(proficiencies_skills_dict.keys()):
        attribute_type = proficiencies_skills_attribute_type_dict[proficiency_skill]
        attribute_type_index_location = attributes_list.index(attribute_type)
        attribute_modifier = int(attributes_modifiers_display_variables_list[attribute_type_index_location]["text"])
        if proficiencies_skills_dict[proficiency_skill] == 0: # There is not any proficiency.
            proficiencies_skills_variables_display_list[idx].config(text=attribute_modifier)
        else: # The value is 1, which means that there is a proficiency bonus to apply.
            proficiency_bonus_modifier = int(proficiency_bonus_display["text"])
            value = attribute_modifier + proficiency_bonus_modifier
            proficiencies_skills_variables_display_list[idx].config(text=value)
    choosen_class= class_value_inside.get()
    if choosen_class == 'Choose':
        number_of_skills_display.config(text=0)
    else:
        pass


def dice_display_updater():
    global selected_class_dict

    logger.debug('Dice display updater was called.')
    dice_number = level_value_inside.get()
    dice_value = 'd' + str(selected_class_dict['hit_die'])
    dice = dice_number + dice_value
    dice_display.config(text=dice)
    logger.debug(f'Dice: {dice}')


def hit_points_display_updater():
    global selected_class_dict

    logger.debug('Hit points display updater was called.')
    level = int(level_value_inside.get())
    constitution_modifier = int(con_modifier_display['text'])
    initial_hit_die = int(selected_class_dict['hit_die'])
    initial_hit_points = initial_hit_die + constitution_modifier
    if level == 1:
        hit_points_display.config(text=initial_hit_points)
        logger.debug(f'Initial Hit points: {initial_hit_points}.')
    else:
        mean_hit_points = int(selected_class_dict['mean_hit_die'])
        hit_points = initial_hit_points + (mean_hit_points + constitution_modifier)*(level-1)
        hit_points_display.config(text=hit_points)
        logger.debug(f'Hit points: {hit_points}.')


def proficiencies_skills_dictionary_updater():
    global background_skill_proficiencies_dict
    global class_skill_proficiencies_dict
    global proficiencies_skills_dict

    logger.debug('Proficiencies skills dictionary updater was called.')
    # Joining class and background proficiency skills dicitionaries.
    for proficiency_skill in proficiencies_skills_dict.keys():
        background_proficiency_skill = background_skill_proficiencies_dict[proficiency_skill]
        class_proficiency_skill = class_skill_proficiencies_dict[proficiency_skill]
        if background_proficiency_skill == 1 or class_proficiency_skill == 1:
            proficiencies_skills_dict[proficiency_skill] = 1
        else:
            proficiencies_skills_dict[proficiency_skill] = 0


def display_updater():
    logger.debug('Display updater (main) was called.')
    attributes_modifiers_display_updater()
    saving_throw_display_updater()
    armor_class_display_updater()
    initiative_display_updater()
    dice_display_updater()
    hit_points_display_updater()
    proficiencies_skills_dictionary_updater()
    proficiencies_skills_display_updater()
    logger.debug('Display updater (main) finished its calling.')


log_directory_path = 'logs'
log_filename = f'player_validator.log'
handler = [RotatingFileHandler(log_directory_path+'/'+log_filename, 
                                maxBytes=1048576, # 1048576 bytes = 1 Mbyte
                                backupCount=5)
            ]
logging.basicConfig(handlers=handler,
                    level=logging.DEBUG,
                    format="[{asctime}] {levelname:8s} - {message}", 
                    style='{',
                    datefmt="%d/%m/%Y %H:%M:%S")
# # The below code is done so that the message logged is also displayed on the console.
logger = logging.getLogger()
logger.setLevel(logging.DEBUG) # Logs debug and upper to the log file.
# Defines a Handler which writes DEBUG messages or higher to the sys.stderr.
console = logging.StreamHandler()
console.setLevel(logging.INFO) # Only displays info and upper to the console.
# Sets a format that is simpler for console display.
formatter = logging.Formatter('{levelname:8s} - {message}',
                                style='{')
# Tell the handler to use this format.
console.setFormatter(formatter)
logger.addHandler(console)


if __name__ == '__main__':
    # DATASETS LOADINGS
    racial_bonuses_df = pd.ExcelFile('datasets/racial_bonuses.xlsx')
    race_options = racial_bonuses_df.sheet_names
    races_and_subraces_dict = dict()
    for race in race_options:
        try:
            if 'yes' in racial_bonuses_df.parse(race)['subrace'].unique():
                race_subraces_list = list(racial_bonuses_df.parse(race)['race_and_subraces'].unique())
                race_subrace = {race_subraces_list[0]: race_subraces_list[1:]}
                races_and_subraces_dict = {**races_and_subraces_dict, **race_subrace}
            else:
                race_subrace = {race: [None]}
                races_and_subraces_dict = {**races_and_subraces_dict, **race_subrace}
        except Exception as err:
            logging.warning(f'The selected race: "{race}" may have some problems in the dataset.')
            logging.warning(f'Error: {err}')

    character_characteristics_df = pd.ExcelFile('datasets/character_characteristics.xlsx')
    alignment_options = character_characteristics_df.parse('alignments')['alignment'].unique()
    backgorund_options_list = character_characteristics_df.parse('backgrounds')['background'].unique()
    classes_df = pd.ExcelFile('datasets/classes.xlsx')
    classes_options = classes_df.sheet_names
    level_options = [level+1 for level in range(20)]
    standard_attributes_list = [15, 14, 13, 12, 10, 8]
    attributes_available_options_list = standard_attributes_list.copy()

    # MUSIC
    pygame.mixer.init()
    pygame.mixer.music.load("music/lament_of_the_war.mp3")
    pygame.mixer.music.play(loops=-1) # Infinite loop

    # APP DECLARATION
    window = tk.Tk()
    window.title('5e PLAYER VALIDATOR - Developed by Rodolfo Viturino')
    window.geometry("900x600")
    window.resizable(width=True, height=True)

    # ICONS
    icons_path = 'icons'
    # Window
    window_icon_path = f'{icons_path}/dragon_claw.ico'
    window.iconbitmap(window_icon_path)
    # Buttons
    plus_button_icon_size = minus_button_icon_size = confirm_button_icon_size = (15, 15)
    plus_button_img_path = f'{icons_path}/plus_button.png'
    plus_button_img = Image.open(plus_button_img_path).resize(plus_button_icon_size, Image.ANTIALIAS)
    plus_button_img = ImageTk.PhotoImage(plus_button_img)
    minus_button_img_path = f'{icons_path}/minus_button.png'
    minus_button_img = Image.open(minus_button_img_path).resize(minus_button_icon_size, Image.ANTIALIAS)
    minus_button_img = ImageTk.PhotoImage(minus_button_img)
    confirm_button_img_path = f'{icons_path}/confirm_button.png'
    confirm_button_img = Image.open(confirm_button_img_path).resize(confirm_button_icon_size, Image.ANTIALIAS)
    confirm_button_img = ImageTk.PhotoImage(confirm_button_img)
    # Background
    window_background_path = f'{icons_path}/dragon_claw.png'
    window_background = Image.open(window_background_path).resize((150,150), Image.ANTIALIAS)
    window_background = ImageTk.PhotoImage(window_background)
    canvas = tk.Canvas(window, width = 400,
                 height = 450)
    canvas.create_image(0, 0, 
                        image=window_background, 
                        anchor="nw")
    canvas.grid(row=1, rowspan=20, column=4, columnspan=8)

    # MENUs CREATION.
    window_menu = tk.Menu(window)
    window.config(menu=window_menu)
    # Add character menu options.
    file_menu = tk.Menu(window_menu, tearoff=False)
    window_menu.add_cascade(label='Player Character', menu=file_menu)
    file_menu.add_command(label="New", command=new_character)
    file_menu.add_separator()
    file_menu.add_command(label="Save", command=save_character)
    file_menu.add_separator()
    file_menu.add_command(label="Open", command=open_character)
    # Music menu
    music_menu = tk.Menu(window_menu, tearoff=False)
    window_menu.add_cascade(label='Music', menu=music_menu)
    music_menu.add_command(label="Play", command=play_music)
    music_menu.add_separator()
    music_menu.add_command(label="Stop", command=stop_music)
    music_menu.add_separator()
    music_menu.add_command(label="Volume", command=music_volume)
    # At this moment, I just want the window to be declared, and if it is not
    # destroyed, a window of the TopLevel will popout at the program start.
    # It will only be packed when the music_volume option is properly selected.
    volume_window = tk.Toplevel(window)
    volume_window.destroy()

    # DISPLAY
    standard_text = '0'
    standard_display_font = ("Helvetica", 14)
    # Name
    name_label = tk.Label(window, text="Enter your name:")
    name_label.grid(row=0, column=0)
    name_entry = tk.Entry(window)
    name_entry.grid(row=0, column=1)
    name_submit_button = tk.Button(window, 
                                    image=confirm_button_img, 
                                    command=name_selector)
    name_submit_button.grid(row=0, column=2, sticky=tk.W)
    name_display = tk.Label(window)
    name_display.config(text="NAME NOT SUBMITED", fg='#9B470A', font=("Helvetica", 14))
    name_display.grid(row=0, column=3, columnspan=4)
    # Alignment
    alignment_label = tk.Label(window, text="Alignment:")
    alignment_label.grid(row=1, column=0)
    alignment_value_inside = tk.StringVar(window)
    alignment_value_inside.set('Choose')
    alignment_value_inside.trace('w', alignment_selector)
    alignment_menu = tk.OptionMenu(window, 
                                    alignment_value_inside, 
                                    *alignment_options)
    alignment_menu.config(width=12)
    alignment_menu.grid(row=1, column=1)
    # Background 
    background_label = tk.Label(window, text="Background:")
    background_label.grid(row=1, column=2)
    background_value_inside = tk.StringVar(window)
    background_value_inside.set('Choose')
    background_value_inside.trace('w', background_selector)
    background_menu = tk.OptionMenu(window, 
                                    background_value_inside, 
                                    *backgorund_options_list)
    background_menu.config(width=12, anchor='w')
    background_menu.grid(row=1, column=3)
    # Race
    race_label = tk.Label(window, text="Race:")
    race_label.grid(row=2, column=0)
    race_value_inside = tk.StringVar(window)
    race_value_inside.set('Choose')
    race_value_inside.trace('w', race_selector)
    race_menu = tk.OptionMenu(window, 
                            race_value_inside, 
                            *races_and_subraces_dict.keys())
    race_menu.config(width=12)
    race_menu.grid(row=2, column=1)
    # Subrace
    subrace_label = tk.Label(window, text="Subrace:")
    subrace_label.grid(row=2, column=2)
    subrace_value_inside = tk.StringVar(window)
    subrace_value_inside.set('Choose')
    subrace_value_inside.trace('w', subrace_selector)
    subrace_menu = tk.OptionMenu(window, 
                                subrace_value_inside, 
                                list()) # The empty list will be update accordingly to which race was selected.
    subrace_menu.config(width=12, anchor='w')
    subrace_menu.grid(row=2, column=3)
    subrace_menu['state'] = 'disabled'
    # Class
    class_label = tk.Label(window, text="Class:")
    class_label.grid(row=3, column=0)
    class_value_inside = tk.StringVar(window)
    class_value_inside.set('Choose')
    class_value_inside.trace('w', class_selector)
    class_menu = tk.OptionMenu(window, class_value_inside, *classes_options)
    class_menu.config(width=12)
    class_menu.grid(row=3, column=1)
    # Level
    level_label = tk.Label(window, text="Level:")
    level_label.grid(row=3, column=2)
    level_value_inside = tk.StringVar(window)
    level_value_inside.set(level_options[0])
    level_value_inside.trace('w', level_selector)
    level_menu = tk.OptionMenu(window, level_value_inside, *level_options)
    level_menu.config(width=3)
    level_menu.grid(row=3, column=3)

    # Armor Class
    armor_class_label = tk.Label(window, text="Armor Class:")
    armor_class_label.grid(row=5, column=0)
    armor_class_display = tk.Label(window)
    armor_class_display.config(text='10', font=standard_display_font)
    armor_class_display.grid(row=5, column=1)
    # Speed
    speed_label = tk.Label(window, text="Speed:")
    speed_label.grid(row=5, column=2)
    speed_display = tk.Label(window)
    speed_display.config(text=standard_text, font=standard_display_font)
    speed_display.grid(row=5, column=3)
    # Proficiency Bonus
    proficiency_bonus_label = tk.Label(window, text="Proficiency Bonus:")
    proficiency_bonus_label.grid(row=6, column=0)
    proficiency_bonus_display = tk.Label(window)
    proficiency_bonus_display.config(text='2', font=standard_display_font)
    proficiency_bonus_display.grid(row=6, column=1)
    # Initiative
    initiative_label = tk.Label(window, text="Initiative:")
    initiative_label.grid(row=6, column=2)
    initiative_display = tk.Label(window)
    initiative_display.config(text=standard_text, font=standard_display_font)
    initiative_display.grid(row=6, column=3)
    # Hit Points
    hit_points_label = tk.Label(window, text="Hit Points:")
    hit_points_label.grid(row=7, column=0)
    hit_points_display = tk.Label(window)
    hit_points_display.config(text=standard_text, font=standard_display_font)
    hit_points_display.grid(row=7, column=1)
    # Dice
    dice_label = tk.Label(window, text="Hit Dice:")
    dice_label.grid(row=7, column=2)
    dice_display = tk.Label(window)
    dice_display.config(text='1d0', font=standard_display_font)
    dice_display.grid(row=7, column=3)

    # ATTRIBUTES
    # Distribution Points
    modifiers_label_height = 1
    modifiers_label_width = 2
    distribution_points_label = tk.Label(window, text="Modifier points\nfor distribution:")
    distribution_points_label.grid(row=13, column=0)
    optional_points_display = tk.Label(window)
    optional_points_display.config(text=standard_text, font=standard_display_font)
    optional_points_display.grid(row=14, column=0)
    # Reset Attributes
    reset_attributes_button = tk.Button(window,
                                        text='Reset Attributes',
                                        command=attributes_reseter)
    reset_attributes_button.grid(row=9, column=0)
    # Labels
    ability_score_label = tk.Label(window, text="Ability Score:")
    ability_score_label.grid(row=10, column=0)
    mod_label = tk.Label(window, text="Modifier:")
    mod_label.grid(row=11, column=0)
    st_label = tk.Label(window, text="Saving Throws:")
    st_label.grid(row=12, column=0)
    # Strength
    str_modifier_label = tk.Label(window, text="STRENGTH")
    str_modifier_label.grid(row=9, column=1)
    str_attributes_inside = tk.StringVar(window)
    str_attributes_inside.set("Choose")
    str_attributes_inside.trace('w', attributes_selector)
    str_attributes_option_menu = tk.OptionMenu(window, 
                                            str_attributes_inside, 
                                            *attributes_available_options_list)
    str_attributes_option_menu.config(width=5)
    str_attributes_option_menu.grid(row=10, column=1)
    str_modifier_display = tk.Label(window)
    str_modifier_display.config(text=standard_text, font=standard_display_font)
    str_modifier_display.grid(row=11, column=1)
    str_saving_throw_display = tk.Label(window)
    str_saving_throw_display.config(text=standard_text, font=standard_display_font)
    str_saving_throw_display.grid(row=12, column=1)
    str_plus_button = tk.Button(window, 
                                text="+",
                                image=plus_button_img, 
                                command=partial(optional_points_updater, 
                                                attribute_name='strength', 
                                                operation='+'))
    str_plus_button.grid(row=13, column=1)
    str_plus_button['state'] = 'disabled' 
    str_minus_button = tk.Button(window, 
                                text="-",
                                image=minus_button_img, 
                                command=partial(optional_points_updater, 
                                                attribute_name='strength', 
                                                operation='-'))
    str_minus_button.grid(row=14, column=1)
    str_minus_button['state'] = 'disabled' 
    # Dexterity
    dex_modifier_label = tk.Label(window, text="DEXTERITY")
    dex_modifier_label.grid(row=9, column=2)
    dex_attributes_inside = tk.StringVar(window)
    dex_attributes_inside.set("Choose")
    dex_attributes_inside.trace('w', attributes_selector)
    dex_attributes_option_menu = tk.OptionMenu(window, 
                                            dex_attributes_inside, 
                                            *attributes_available_options_list)
    dex_attributes_option_menu.config(width=5)
    dex_attributes_option_menu.grid(row=10, column=2)
    dex_modifier_display = tk.Label(window)
    dex_modifier_display.config(text=standard_text, font=standard_display_font)
    dex_modifier_display.grid(row=11, column=2)
    dex_saving_throw_display = tk.Label(window)
    dex_saving_throw_display.grid(row=12, column=2)
    dex_saving_throw_display.config(text=standard_text, font=standard_display_font)
    dex_plus_button = tk.Button(window, 
                                text="+",
                                image=plus_button_img, 
                                command=partial(optional_points_updater, 
                                                attribute_name='dexterity', 
                                                operation='+'))
    dex_plus_button.grid(row=13, column=2)
    dex_plus_button['state'] = 'disabled' 
    dex_minus_button = tk.Button(window, 
                                text="-",
                                image=minus_button_img, 
                                command=partial(optional_points_updater, 
                                                attribute_name='dexterity', 
                                                operation='-'))
    dex_minus_button.grid(row=14, column=2)
    dex_minus_button['state'] = 'disabled' 
    # Constitution
    con_modifier_label = tk.Label(window, text="CONSTITUTION")
    con_modifier_label.grid(row=9, column=3)
    con_attributes_inside = tk.StringVar(window)
    con_attributes_inside.set("Choose")
    con_attributes_inside.trace('w', attributes_selector)
    con_attributes_option_menu = tk.OptionMenu(window, 
                                            con_attributes_inside, 
                                            *attributes_available_options_list)
    con_attributes_option_menu.config(width=5)
    con_attributes_option_menu.grid(row=10, column=3)
    con_modifier_display = tk.Label(window)
    con_modifier_display.config(text=standard_text, font=standard_display_font)
    con_modifier_display.grid(row=11, column=3)
    con_saving_throw_display = tk.Label(window)
    con_saving_throw_display.grid(row=12, column=3)
    con_saving_throw_display.config(text=standard_text, font=standard_display_font)
    con_plus_button = tk.Button(window, 
                                text="+",
                                image=plus_button_img, 
                                command=partial(optional_points_updater, 
                                                attribute_name='constitution',
                                                operation='+'))
    con_plus_button.grid(row=13, column=3)
    con_plus_button['state'] = 'disabled' 
    con_minus_button = tk.Button(window, 
                                text="-",
                                image=minus_button_img, 
                                command=partial(optional_points_updater, 
                                                attribute_name='constitution',
                                                operation='-'))
    con_minus_button.grid(row=14, column=3)
    con_minus_button['state'] = 'disabled' 
    # Intelligence
    int_modifier_label = tk.Label(window, text="INTELLIGENCE")
    int_modifier_label.grid(row=9, column=4)

    int_attributes_inside = tk.StringVar(window)
    int_attributes_inside.set("Choose")
    int_attributes_inside.trace('w', attributes_selector)
    int_attributes_option_menu = tk.OptionMenu(window, 
                                            int_attributes_inside, 
                                            *attributes_available_options_list)
    int_attributes_option_menu.config(width=5)
    int_attributes_option_menu.grid(row=10, column=4)
    int_modifier_display = tk.Label(window)
    int_modifier_display.config(text=standard_text, font=standard_display_font)
    int_modifier_display.grid(row=11, column=4)
    int_saving_throw_display = tk.Label(window)
    int_saving_throw_display.grid(row=12, column=4)
    int_saving_throw_display.config(text=standard_text, font=standard_display_font)
    int_plus_button = tk.Button(window, 
                                text="+",
                                image=plus_button_img, 
                                command=partial(optional_points_updater, 
                                                attribute_name='intelligence',
                                                operation='+'))
    int_plus_button.grid(row=13, column=4)
    int_plus_button['state'] = 'disabled' 
    int_minus_button = tk.Button(window, 
                                text="-",
                                image=minus_button_img, 
                                command=partial(optional_points_updater, 
                                                attribute_name='intelligence',
                                                operation='-'))
    int_minus_button.grid(row=14, column=4)
    int_minus_button['state'] = 'disabled' 
    # Wisdom
    wis_modifier_label = tk.Label(window, text="WISDOM")
    wis_modifier_label.grid(row=9, column=5)
    wis_attributes_inside = tk.StringVar(window)
    wis_attributes_inside.set("Choose")
    wis_attributes_inside.trace('w', attributes_selector)
    wis_attributes_option_menu = tk.OptionMenu(window, 
                                            wis_attributes_inside, 
                                            *attributes_available_options_list)
    wis_attributes_option_menu.config(width=5)
    wis_attributes_option_menu.grid(row=10, column=5)
    wis_modifier_display = tk.Label(window)
    wis_modifier_display.config(text=standard_text, font=standard_display_font)
    wis_modifier_display.grid(row=11, column=5)
    wis_saving_throw_display = tk.Label(window)
    wis_saving_throw_display.config(text=standard_text, font=standard_display_font)
    wis_saving_throw_display.grid(row=12, column=5)
    wis_plus_button = tk.Button(window, 
                                text="+",
                                image=plus_button_img, 
                                command=partial(optional_points_updater, 
                                                attribute_name='wisdom',
                                                operation='+'))
    wis_plus_button.grid(row=13, column=5)
    wis_plus_button['state'] = 'disabled' 
    wis_minus_button = tk.Button(window, 
                                text="-",
                                image=minus_button_img, 
                                command=partial(optional_points_updater, 
                                                attribute_name='wisdom',
                                                operation='-'))
    wis_minus_button.grid(row=14, column=5)
    wis_minus_button['state'] = 'disabled' 
    # Charisma
    cha_modifier_label = tk.Label(window, text="CHARISMA")
    cha_modifier_label.grid(row=9, column=6)
    cha_attributes_inside = tk.StringVar(window)
    cha_attributes_inside.set("Choose")
    cha_attributes_inside.trace('w', attributes_selector)
    cha_attributes_option_menu = tk.OptionMenu(window, 
                                            cha_attributes_inside, 
                                            *attributes_available_options_list)
    cha_attributes_option_menu.config(width=5)
    cha_attributes_option_menu.grid(row=10, column=6)
    cha_modifier_display = tk.Label(window)
    cha_modifier_display.config(text=standard_text, font=standard_display_font)
    cha_modifier_display.grid(row=11, column=6)
    cha_saving_throw_display = tk.Label(window)
    cha_saving_throw_display.grid(row=12, column=6)
    cha_saving_throw_display.config(text=standard_text, font=standard_display_font)
    cha_plus_button = tk.Button(window, 
                                text="+",
                                image=plus_button_img, 
                                command=partial(optional_points_updater, 
                                                attribute_name='charisma',
                                                operation='+'))
    cha_plus_button.grid(row=13, column=6)
    cha_plus_button['state'] = 'disabled' 
    cha_minus_button = tk.Button(window, 
                                text="-",
                                image=minus_button_img, 
                                command=partial(optional_points_updater, 
                                                attribute_name='charisma',
                                                operation='-'))
    cha_minus_button.grid(row=14, column=6)
    cha_minus_button['state'] = 'disabled' 

    # SKILLS
    # Skills
    skills_label = tk.Label(window, text="SKILLS")
    skills_label.grid(row=0, column=7, columnspan=3)
    # Skills Modifiers
    number_of_skills_label = tk.Label(window, text="Number of Skills")
    number_of_skills_label.grid(row=2, column=9)
    number_of_skills_display = tk.Label(window)
    number_of_skills_display.config(text=standard_text, font=standard_display_font)
    number_of_skills_display.grid(row=3, column=9)
    # Choose skill
    choose_skills_label = tk.Label(window, text="Available Skills")
    choose_skills_label.grid(row=6, column=9)
    choose_skills_value_inside = tk.StringVar(window)
    choose_skills_value_inside.set('Choose')
    choose_skills_value_inside.trace('w', proficiency_skills_selector)
    choose_skills_menu = tk.OptionMenu(window, 
                                    choose_skills_value_inside, 
                                    [])
    choose_skills_menu.config(width=12)
    choose_skills_menu.grid(row=7, column=9)
    choose_skills_menu['state'] = 'disabled'
    # Remove skill
    restore_skills_label = tk.Label(window, text="Restore Skills")
    restore_skills_label.grid(row=10, column=9)
    restore_skills_value_inside = tk.StringVar(window)
    restore_skills_value_inside.set('Choose')
    restore_skills_value_inside.trace('w', restore_proficiency_skills_selector)
    restore_skills_menu = tk.OptionMenu(window, 
                                    restore_skills_value_inside, 
                                    [])
    restore_skills_menu.config(width=12)
    restore_skills_menu.grid(row=11, column=9)
    restore_skills_menu['state'] = 'disabled'
    # Acrobatics
    acrobatics_label = tk.Label(window, text="Acrobatics")
    acrobatics_label.grid(row=1, column=7)
    acrobatics_display = tk.Label(window)
    acrobatics_display.config(text=standard_text, font=standard_display_font)
    acrobatics_display.grid(row=1, column=8)
    # Animal Handling
    animal_handling_label = tk.Label(window, text="Animal Handling")
    animal_handling_label.grid(row=2, column=7)
    animal_handling_display = tk.Label(window)
    animal_handling_display.config(text=standard_text, font=standard_display_font)
    animal_handling_display.grid(row=2, column=8)
    # Arcana
    arcana_label = tk.Label(window, text="Arcana")
    arcana_label.grid(row=3, column=7)
    arcana_display = tk.Label(window)
    arcana_display.config(text=standard_text, font=standard_display_font)
    arcana_display.grid(row=3, column=8)
    # Athletics
    athletics_label = tk.Label(window, text="Athletics")
    athletics_label.grid(row=4, column=7)
    athletics_display = tk.Label(window, height=modifiers_label_height, width=modifiers_label_width)
    athletics_display.config(text=standard_text, font=standard_display_font)
    athletics_display.grid(row=4, column=8)
    # Deception
    deception_label = tk.Label(window, text="Deception")
    deception_label.grid(row=5, column=7)
    deception_display = tk.Label(window)
    deception_display.config(text=standard_text, font=standard_display_font)
    deception_display.grid(row=5, column=8)
    # History
    history_label = tk.Label(window, text="History")
    history_label.grid(row=6, column=7)
    history_display = tk.Label(window)
    history_display.config(text=standard_text, font=standard_display_font)
    history_display.grid(row=6, column=8)
    # Insight
    insight_label = tk.Label(window, text="Insight")
    insight_label.grid(row=7, column=7)
    insight_display = tk.Label(window)
    insight_display.config(text=standard_text, font=standard_display_font)
    insight_display.grid(row=7, column=8)
    # Intimidation
    intimidation_label = tk.Label(window, text="Intimidation")
    intimidation_label.grid(row=8, column=7)
    intimidation_display = tk.Label(window)
    intimidation_display.config(text=standard_text, font=standard_display_font)
    intimidation_display.grid(row=8, column=8)
    # Investigation
    investigation_label = tk.Label(window, text="Investigation")
    investigation_label.grid(row=9, column=7)
    investigation_display = tk.Label(window)
    investigation_display.config(text=standard_text, font=standard_display_font)
    investigation_display.grid(row=9, column=8)
    # Medicine
    medicine_label = tk.Label(window, text="Medicine")
    medicine_label.grid(row=10, column=7)
    medicine_display = tk.Label(window)
    medicine_display.config(text=standard_text, font=standard_display_font)
    medicine_display.grid(row=10, column=8)
    # Nature
    nature_label = tk.Label(window, text="Nature")
    nature_label.grid(row=11, column=7)
    nature_display = tk.Label(window)
    nature_display.config(text=standard_text, font=standard_display_font)
    nature_display.grid(row=11, column=8)
    # Perception
    perception_label = tk.Label(window, text="Perception")
    perception_label.grid(row=12, column=7)
    perception_display = tk.Label(window)
    perception_display.config(text=standard_text, font=standard_display_font)
    perception_display.grid(row=12, column=8)
    # Performance
    performance_label = tk.Label(window, text="Performance")
    performance_label.grid(row=13, column=7)
    performance_display = tk.Label(window)
    performance_display.config(text=standard_text, font=standard_display_font)
    performance_display.grid(row=13, column=8)
    # Persuasion
    persuasion_label = tk.Label(window, text="Persuasion")
    persuasion_label.grid(row=14, column=7)
    persuasion_display = tk.Label(window)
    persuasion_display.config(text=standard_text, font=standard_display_font)
    persuasion_display.grid(row=14, column=8)
    # Religion
    religion_label = tk.Label(window, text="Religion")
    religion_label.grid(row=15, column=7)
    religion_display = tk.Label(window)
    religion_display.config(text=standard_text, font=standard_display_font)
    religion_display.grid(row=15, column=8)
    # Sleight of Hand
    sleight_of_hand_label = tk.Label(window, text="Sleight of Hand")
    sleight_of_hand_label.grid(row=16, column=7)
    sleight_of_hand_display = tk.Label(window)
    sleight_of_hand_display.config(text=standard_text, font=standard_display_font)
    sleight_of_hand_display.grid(row=16, column=8)
    # Stealth
    stealth_label = tk.Label(window, text="Stealth")
    stealth_label.grid(row=17, column=7)
    stealth_display = tk.Label(window)
    stealth_display.config(text=standard_text, font=standard_display_font)
    stealth_display.grid(row=17, column=8)
    # Survival
    survival_label = tk.Label(window, text="Survival")
    survival_label.grid(row=18, column=7)
    survival_display = tk.Label(window)
    survival_display.config(text=standard_text, font=standard_display_font)
    survival_display.grid(row=18, column=8)

    # Declarations for global variables
    attributes_list = ['strength', 
                        'dexterity', 
                        'constitution', 
                        'intelligence', 
                        'wisdom', 
                        'charisma']
    attributes_inside_list = [str_attributes_inside,
                            dex_attributes_inside,
                            con_attributes_inside,
                            int_attributes_inside,
                            wis_attributes_inside,
                            cha_attributes_inside]
    attributes_modifiers_display_variables_list = [str_modifier_display, 
                                                    dex_modifier_display, 
                                                    con_modifier_display, 
                                                    int_modifier_display,
                                                    wis_modifier_display, 
                                                    cha_modifier_display]
    saving_throws_variables_display_list = [str_saving_throw_display, 
                                            dex_saving_throw_display,
                                            con_saving_throw_display,
                                            int_saving_throw_display,
                                            wis_saving_throw_display,
                                            cha_saving_throw_display]
    saving_throws_dict = {attribute:0 for attribute in attributes_list}
    selected_race_modifiers_dict = saving_throws_dict.copy()
    selected_subrace_modifiers_dict = saving_throws_dict.copy()
    proficiencies_skills_attribute_type_dict = {'acrobatics':'dexterity', 
                                        'animal_handling':'wisdom', 
                                        'arcana':'intelligence', 
                                        'athletics':'strength', 
                                        'deception':'charisma', 
                                        'history':'intelligence', 
                                        'insight':'wisdom', 
                                        'intimidation':'charisma', 
                                        'investigation':'intelligence', 
                                        'medicine':'wisdom', 
                                        'nature':'intelligence', 
                                        'perception':'wisdom', 
                                        'performance':'charisma', 
                                        'persuasion':'charisma', 
                                        'religion':'intelligence', 
                                        'sleight_of_hand':'dexterity', 
                                        'stealth':'dexterity',
                                        'survival':'wisdom'}
    proficiencies_skills_dict = {skill:0 for skill in proficiencies_skills_attribute_type_dict.keys()}
    background_skill_proficiencies_dict = proficiencies_skills_dict.copy()
    class_skill_proficiencies_dict = proficiencies_skills_dict.copy()
    proficiencies_skills_variables_display_list = [acrobatics_display, 
                                                animal_handling_display, 
                                                arcana_display, 
                                                athletics_display, 
                                                deception_display, 
                                                history_display, 
                                                insight_display, 
                                                intimidation_display, 
                                                investigation_display, 
                                                medicine_display, 
                                                nature_display, 
                                                perception_display, 
                                                performance_display, 
                                                persuasion_display, 
                                                religion_display, 
                                                sleight_of_hand_display, 
                                                stealth_display,
                                                survival_display]
    selected_class_dict = {'hit_die':0,
                            'mean_hit_die':0,
                            'armor_proficiencies':0,
                            'weapon_proficiencies':0,
                            'tools_proficiencies':0,
                            'saving_throws_proficies':0,
                            'choose_skills_number':0,
                            'choose_skills_list':0,
                            'features':0,
                            'spells_known':0,
                            'invocations_known':0,
                            'cantrips':0,
                            'spell_slot_level_1':0,
                            'spell_slot_level_2':0,
                            'spell_slot_level_3':0,
                            'spell_slot_level_4':0,
                            'spell_slot_level_5':0,
                            'spell_slot_level_6':0,
                            'spell_slot_level_7':0,
                            'spell_slot_level_8':0,
                            'spell_slot_level_9':0,
                            'spell_save_dc':0,
                            'ki_save_dc':0,
                            'spell_attack_modifier':0,
                            'equipment':0,
                            'rage':0,
                            'rage_damage':0,
                            'martial_arts':0,
                            'ki_points':0,
                            'unarmored_movement':0,
                            'sneak_attack':0}
    available_skills_list = list()
    restore_skills_list = list()
    removed_background_skill_from_class_list_memory = list()
    window.mainloop()
