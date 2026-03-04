"""
Fix Skills section in registration.py to use paginated multiselect.
"""
import pathlib

def fix_skills_section(filepath):
    content = filepath.read_text(encoding='utf-8')
    lines = content.split('\n')
    
    # 1. Update the process_about handler to jump straight to paginated skill_items
    start_about = None
    end_about = None
    
    for i, line in enumerate(lines):
        if 'async def process_about' in line:
            start_about = i
        if start_about is not None and 'await state.set_state(Registration.skill_category)' in line:
            end_about = i + 1
            break
            
    if start_about is None or end_about is None:
        print("Could not find process_about")
        return False
        
    print(f"process_about found at {start_about} to {end_about}")
    
    about_replacement = [
        '        "• create or deliver a clear final result\\n\\n"',
        '        "Select your areas of expertise:"',
        '    )',
        '',
        '    data = await state.get_data()',
        '    selected = set(data.get("selected_skill_items", []))',
        '    page = 0',
        '    await state.update_data(skills_page=page)',
        '',
        '    await message.answer(',
        '        skills_intro,',
        '        reply_markup=get_paginated_multiselect_keyboard(',
        '            items=ALL_SKILLS,',
        '            selected=selected,',
        '            page=page,',
        '            items_per_page=10,',
        '            prefix="q_item",',
        '            done_callback="q_item_done",',
        '            back_callback="skill_back_to_about",',
        '            page_callback_prefix="skill_page"',
        '        )',
        '    )',
        '    await state.set_state(Registration.skill_items)'
    ]
    
    replace_start = None
    for i in range(start_about, end_about):
        if '"• create or deliver a clear final result\\n\\n"' in lines[i]:
            replace_start = i
            break
            
    if replace_start is None:
        print("Could not find replacement point in process_about")
        return False
        
    lines[replace_start:end_about] = about_replacement
    
    # 2. Add back_to_about handler
    new_handlers = [
        '',
        '@router.callback_query(Registration.skill_items, F.data == "skill_back_to_about")',
        'async def back_to_about(callback: CallbackQuery, state: FSMContext):',
        '    await callback.message.delete()',
        '    await callback.message.answer(',
        '        "Tell us a bit about yourself\\nDescribe it shortly — just a few words.\\nIn one of the next questions, you\'ll be able to share more details.\\n\\nExamples:\\nArtist · Community creator\\nFounder · Creative entrepreneur\\nDJ · Music curator",',
        '        reply_markup=get_cancel_keyboard()',
        '    )',
        '    await state.set_state(Registration.about)',
        '    await callback.answer()'
    ]
    
    cat_handlers_start = None
    cat_handlers_end = None
    
    for i, line in enumerate(lines):
        if '@router.callback_query(Registration.skill_category, F.data == "skill_cat_back")' in line:
            cat_handlers_start = i
            break
            
    for i in range(cat_handlers_start, len(lines)):
        if '@router.callback_query(Registration.skill_items, F.data.startswith("q_item:"))' in line:
            cat_handlers_end = i
            break
            
    if cat_handlers_start and cat_handlers_end:
        lines[cat_handlers_start:cat_handlers_end] = new_handlers
    
    # 3. Update skill item toggle handler and add pagination handler
    toggle_start = None
    toggle_end = None
    for i, line in enumerate(lines):
        if '@router.callback_query(Registration.skill_items, F.data.startswith("q_item:"))' in line:
            toggle_start = i
            break
            
    for i in range(toggle_start, len(lines)):
        if '@router.callback_query(Registration.skill_items, F.data == "q_item_done")' in lines[i]:
            toggle_end = i
            break
            
    if toggle_start and toggle_end:
        toggle_replacement = [
            '@router.callback_query(Registration.skill_items, F.data.startswith("skill_page:"))',
            'async def process_skill_page(callback: CallbackQuery, state: FSMContext):',
            '    page = int(callback.data.split(":")[1])',
            '    await state.update_data(skills_page=page)',
            '    data = await state.get_data()',
            '    selected = set(data.get("selected_skill_items", []))',
            '    await callback.message.edit_reply_markup(',
            '        reply_markup=get_paginated_multiselect_keyboard(',
            '            items=ALL_SKILLS,',
            '            selected=selected,',
            '            page=page,',
            '            items_per_page=10,',
            '            prefix="q_item",',
            '            done_callback="q_item_done",',
            '            back_callback="skill_back_to_about",',
            '            page_callback_prefix="skill_page"',
            '        )',
            '    )',
            '    await callback.answer()',
            '',
            '@router.callback_query(Registration.skill_items, F.data.startswith("q_item:"))',
            'async def process_skill_item_toggle(callback: CallbackQuery, state: FSMContext):',
            '    item_hash = callback.data.split(":")[1]',
            '    data = await state.get_data()',
            '    ',
            '    target_item = find_item_by_hash(ALL_SKILLS, item_hash)',
            '    ',
            '    if target_item:',
            '        selected_items = set(data.get("selected_skill_items", []))',
            '        if target_item in selected_items:',
            '            selected_items.remove(target_item)',
            '        else:',
            '            selected_items.add(target_item)',
            '            ',
            '        await state.update_data(selected_skill_items=list(selected_items))',
            '        ',
            '        page = data.get("skills_page", 0)',
            '        await callback.message.edit_reply_markup(',
            '            reply_markup=get_paginated_multiselect_keyboard(',
            '                items=ALL_SKILLS,',
            '                selected=selected_items,',
            '                page=page,',
            '                items_per_page=10,',
            '                prefix="q_item",',
            '                done_callback="q_item_done",',
            '                back_callback="skill_back_to_about",',
            '                page_callback_prefix="skill_page"',
            '            )',
            '        )',
            '    await callback.answer()'
        ]
        lines[toggle_start:toggle_end] = toggle_replacement
        
    # 4. Fix back from offer_formats
    for i, line in enumerate(lines):
        if '@router.callback_query(Registration.offer_formats, F.data == "q_fmt_back")' in line:
            for j in range(i, len(lines)):
                if 'await callback.message.edit_text(' in lines[j] and 'get_category_keyboard' in lines[j+3]:
                    lines[j:j+5] = [
                        '    data = await state.get_data()',
                        '    selected = set(data.get("selected_skill_items", []))',
                        '    page = data.get("skills_page", 0)',
                        '    await callback.message.edit_text(',
                        '        "Select your areas of expertise:",',
                        '        reply_markup=get_paginated_multiselect_keyboard(',
                        '            items=ALL_SKILLS,',
                        '            selected=selected,',
                        '            page=page,',
                        '            items_per_page=10,',
                        '            prefix="q_item",',
                        '            done_callback="q_item_done",',
                        '            back_callback="skill_back_to_about",',
                        '            page_callback_prefix="skill_page"',
                        '        )',
                        '    )',
                        '    await state.set_state(Registration.skill_items)'
                    ]
                    break
            break

    # Add import
    import_idx = None
    for i, line in enumerate(lines):
        if 'get_multiselect_keyboard' in line and ('from bot.keyboards import' in lines[i-3] or 'from bot.keyboards import' in lines[i-4]):
            import_idx = i
            break
            
    if import_idx and 'get_paginated_multiselect_keyboard' not in lines[import_idx] and 'get_paginated_multiselect_keyboard' not in lines[import_idx+1] and 'get_paginated_multiselect_keyboard' not in lines[import_idx+2]:
        lines[import_idx] = lines[import_idx] + '    get_paginated_multiselect_keyboard,'
        
    filepath.write_text('\\n'.join(lines), encoding='utf-8')
    print("Done Skills!")

fix_skills_section(pathlib.Path(r'd:\\telegrambot1\\bot\\handlers\\registration.py'))
