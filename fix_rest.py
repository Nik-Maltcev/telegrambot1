"""
Fix Intros and Specialists section in registration.py to use paginated multiselect.
"""
import pathlib

def fix_other_sections(filepath):
    content = filepath.read_text(encoding='utf-8')
    lines = content.split('\n')
    
    # 1. INTRODUCTIONS
    # Find start of intros
    intro_start = None
    intro_end = None
    for i, line in enumerate(lines):
        if 'async def start_intro_section' in line:
            intro_start = i
            break
            
    for i in range(intro_start, len(lines)):
        if 'async def finish_intro_items' in lines[i]:
            intro_end = i
            break
            
    if intro_start and intro_end:
        intro_replacement = [
            '@router.callback_query(Registration.intro_section, F.data == "intro_start")',
            'async def start_intro_section(callback: CallbackQuery, state: FSMContext):',
            '    data = await state.get_data()',
            '    selected = set(data.get("selected_intro_items", []))',
            '    page = 0',
            '    await state.update_data(intro_page=page)',
            '    ',
            '    from bot.form_data import INTRO_CATEGORIES',
            '    ALL_INTROS = []',
            '    for cat in INTRO_CATEGORIES.values():',
            '        ALL_INTROS.extend(cat["items"])',
            '        ',
            '    await callback.message.edit_text(',
            '        "Select the people you can introduce:",',
            '        reply_markup=get_paginated_multiselect_keyboard(',
            '            items=ALL_INTROS,',
            '            selected=selected,',
            '            page=page,',
            '            items_per_page=10,',
            '            prefix="intro_item",',
            '            done_callback="intro_item_done",',
            '            back_callback="intro_back_to_sec",',
            '            page_callback_prefix="intro_page"',
            '        )',
            '    )',
            '    await state.set_state(Registration.intro_items)',
            '    await callback.answer()',
            '',
            '@router.callback_query(Registration.intro_items, F.data == "intro_back_to_sec")',
            'async def back_to_intro_section(callback: CallbackQuery, state: FSMContext):',
            '    intro_text = (',
            '        "2|10 🤝🏻 Personal Introduction\\n\\n"',
            '        "In almost every life story, there is a moment when someone opened a door for us.\\n\\n"',
            '        "Here, you can describe the key people in your orbit — founders, creators, innovators, "',
            '        "curators, thinkers, leaders whom you are willing to introduce to other community members.\\n\\n"',
            '        "Sharing information about them does not commit you to making an introduction."',
            '    )',
            '    await callback.message.edit_text(intro_text, reply_markup=get_section_intro_keyboard("intro_start", "intro_skip", "intro_sec_back"))',
            '    await state.set_state(Registration.intro_section)',
            '    await callback.answer()',
            '',
            '@router.callback_query(Registration.intro_items, F.data.startswith("intro_page:"))',
            'async def process_intro_page(callback: CallbackQuery, state: FSMContext):',
            '    page = int(callback.data.split(":")[1])',
            '    await state.update_data(intro_page=page)',
            '    data = await state.get_data()',
            '    selected = set(data.get("selected_intro_items", []))',
            '    ',
            '    from bot.form_data import INTRO_CATEGORIES',
            '    ALL_INTROS = []',
            '    for cat in INTRO_CATEGORIES.values():',
            '        ALL_INTROS.extend(cat["items"])',
            '        ',
            '    await callback.message.edit_reply_markup(',
            '        reply_markup=get_paginated_multiselect_keyboard(',
            '            items=ALL_INTROS,',
            '            selected=selected,',
            '            page=page,',
            '            items_per_page=10,',
            '            prefix="intro_item",',
            '            done_callback="intro_item_done",',
            '            back_callback="intro_back_to_sec",',
            '            page_callback_prefix="intro_page"',
            '        )',
            '    )',
            '    await callback.answer()',
            '',
            '@router.callback_query(Registration.intro_items, F.data.startswith("intro_item:"))',
            'async def toggle_intro_item(callback: CallbackQuery, state: FSMContext):',
            '    item_hash = callback.data.split(":")[1]',
            '    data = await state.get_data()',
            '    ',
            '    from bot.form_data import INTRO_CATEGORIES',
            '    ALL_INTROS = []',
            '    for cat in INTRO_CATEGORIES.values():',
            '        ALL_INTROS.extend(cat["items"])',
            '        ',
            '    target_item = find_item_by_hash(ALL_INTROS, item_hash)',
            '    if target_item:',
            '        selected = set(data.get("selected_intro_items", []))',
            '        if target_item in selected:',
            '            selected.remove(target_item)',
            '        else:',
            '            selected.add(target_item)',
            '        await state.update_data(selected_intro_items=list(selected))',
            '        ',
            '        page = data.get("intro_page", 0)',
            '        await callback.message.edit_reply_markup(',
            '            reply_markup=get_paginated_multiselect_keyboard(',
            '                items=ALL_INTROS,',
            '                selected=selected,',
            '                page=page,',
            '                items_per_page=10,',
            '                prefix="intro_item",',
            '                done_callback="intro_item_done",',
            '                back_callback="intro_back_to_sec",',
            '                page_callback_prefix="intro_page"',
            '            )',
            '        )',
            '    await callback.answer()',
            ''
        ]
        # find where finish_intro_items starts (the decorator)
        dec_start = intro_end - 1
        lines[intro_start-1:dec_start] = intro_replacement

    # 2. SPECIALISTS
    spec_start = None
    spec_end = None
    for i, line in enumerate(lines):
        if 'async def start_specialist_section' in line:
            spec_start = i
            break
            
    for i in range(spec_start, len(lines)):
        if 'async def finish_specialist_items' in lines[i]:
            spec_end = i
            break
            
    if spec_start and spec_end:
        spec_replacement = [
            '@router.callback_query(Registration.specialist_section, F.data == "specialist_start")',
            'async def start_specialist_section(callback: CallbackQuery, state: FSMContext):',
            '    data = await state.get_data()',
            '    selected = set(data.get("selected_specialist_items", []))',
            '    page = 0',
            '    await state.update_data(spec_page=page)',
            '    ',
            '    from bot.form_data import SPECIALIST_CATEGORIES',
            '    ALL_SPECIALISTS = []',
            '    for cat in SPECIALIST_CATEGORIES.values():',
            '        ALL_SPECIALISTS.extend(cat["items"])',
            '        ',
            '    await callback.message.edit_text(',
            '        "Select the specialists you can recommend:",',
            '        reply_markup=get_paginated_multiselect_keyboard(',
            '            items=ALL_SPECIALISTS,',
            '            selected=selected,',
            '            page=page,',
            '            items_per_page=10,',
            '            prefix="spec_item",',
            '            done_callback="spec_item_done",',
            '            back_callback="spec_back_to_sec",',
            '            page_callback_prefix="spec_page"',
            '        )',
            '    )',
            '    await state.set_state(Registration.specialist_items)',
            '    await callback.answer()',
            '',
            '@router.callback_query(Registration.specialist_items, F.data == "spec_back_to_sec")',
            'async def back_to_spec_section(callback: CallbackQuery, state: FSMContext):',
            '    specialist_text = (',
            '        "8|10 🩵 Specialists\\n\\n"',
            '        "Each of us has our own \\\"super-people\\\" — specialists who once saved the day, guided us through a challenge, "',
            '        "brought clarity, or simply made life easier.\\n\\n"',
            '        "Please list only those specialists you have personally worked with and can genuinely vouch for."',
            '    )',
            '    await callback.message.edit_text(specialist_text, reply_markup=get_section_intro_keyboard("specialist_start", "specialist_skip", "spec_sec_back"))',
            '    await state.set_state(Registration.specialist_section)',
            '    await callback.answer()',
            '',
            '@router.callback_query(Registration.specialist_items, F.data.startswith("spec_page:"))',
            'async def process_specialist_page(callback: CallbackQuery, state: FSMContext):',
            '    page = int(callback.data.split(":")[1])',
            '    await state.update_data(spec_page=page)',
            '    data = await state.get_data()',
            '    selected = set(data.get("selected_specialist_items", []))',
            '    ',
            '    from bot.form_data import SPECIALIST_CATEGORIES',
            '    ALL_SPECIALISTS = []',
            '    for cat in SPECIALIST_CATEGORIES.values():',
            '        ALL_SPECIALISTS.extend(cat["items"])',
            '        ',
            '    await callback.message.edit_reply_markup(',
            '        reply_markup=get_paginated_multiselect_keyboard(',
            '            items=ALL_SPECIALISTS,',
            '            selected=selected,',
            '            page=page,',
            '            items_per_page=10,',
            '            prefix="spec_item",',
            '            done_callback="spec_item_done",',
            '            back_callback="spec_back_to_sec",',
            '            page_callback_prefix="spec_page"',
            '        )',
            '    )',
            '    await callback.answer()',
            '',
            '@router.callback_query(Registration.specialist_items, F.data.startswith("spec_item:"))',
            'async def toggle_specialist_item(callback: CallbackQuery, state: FSMContext):',
            '    item_hash = callback.data.split(":")[1]',
            '    data = await state.get_data()',
            '    ',
            '    from bot.form_data import SPECIALIST_CATEGORIES',
            '    ALL_SPECIALISTS = []',
            '    for cat in SPECIALIST_CATEGORIES.values():',
            '        ALL_SPECIALISTS.extend(cat["items"])',
            '        ',
            '    target_item = find_item_by_hash(ALL_SPECIALISTS, item_hash)',
            '    if target_item:',
            '        selected = set(data.get("selected_specialist_items", []))',
            '        if target_item in selected:',
            '            selected.remove(target_item)',
            '        else:',
            '            selected.add(target_item)',
            '        await state.update_data(selected_specialist_items=list(selected))',
            '        ',
            '        page = data.get("spec_page", 0)',
            '        await callback.message.edit_reply_markup(',
            '            reply_markup=get_paginated_multiselect_keyboard(',
            '                items=ALL_SPECIALISTS,',
            '                selected=selected,',
            '                page=page,',
            '                items_per_page=10,',
            '                prefix="spec_item",',
            '                done_callback="spec_item_done",',
            '                back_callback="spec_back_to_sec",',
            '                page_callback_prefix="spec_page"',
            '            )',
            '        )',
            '    await callback.answer()',
            ''
        ]
        dec_start = spec_end - 1
        lines[spec_start-1:dec_start] = spec_replacement

    # 3. SPECIALIST LOOP
    loop_start = None
    loop_end = None
    for i, line in enumerate(lines):
        if 'async def add_another_specialist' in line:
            loop_start = i
            break
            
    for i in range(loop_start, len(lines)):
        if 'await callback.answer()' in lines[i]:
            loop_end = i + 1
            break
            
    if loop_start and loop_end:
        loop_replacement = [
            '@router.callback_query(Registration.specialist_loop_confirm, F.data.startswith("confirm:add_spec:"))',
            'async def add_another_specialist(callback: CallbackQuery, state: FSMContext):',
            '    data = await state.get_data()',
            '    selected = set()',
            '    page = 0',
            '    await state.update_data(spec_page=page, selected_specialist_items=[])',
            '    ',
            '    from bot.form_data import SPECIALIST_CATEGORIES',
            '    ALL_SPECIALISTS = []',
            '    for cat in SPECIALIST_CATEGORIES.values():',
            '        ALL_SPECIALISTS.extend(cat["items"])',
            '        ',
            '    await callback.message.edit_text(',
            '        "Select the specialists you can recommend:",',
            '        reply_markup=get_paginated_multiselect_keyboard(',
            '            items=ALL_SPECIALISTS,',
            '            selected=selected,',
            '            page=page,',
            '            items_per_page=10,',
            '            prefix="spec_item",',
            '            done_callback="spec_item_done",',
            '            back_callback="spec_back_to_sec",',
            '            page_callback_prefix="spec_page"',
            '        )',
            '    )',
            '    await state.set_state(Registration.specialist_items)',
            '    await callback.answer()'
        ]
        lines[loop_start-1:loop_end] = loop_replacement
        
    filepath.write_text('\\n'.join(lines), encoding='utf-8')
    print("Done Intros and Specialists!")

fix_other_sections(pathlib.Path(r'd:\\telegrambot1\\bot\\handlers\\registration.py'))
